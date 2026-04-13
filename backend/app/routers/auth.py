import secrets
from datetime import datetime
from urllib.parse import urlencode
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
import httpx

from app.config import settings
from app.database import get_session
from app.dependencies import get_current_user
from app.models import User, RefreshToken
from app.services.auth_service import (
    create_access_token,
    create_refresh_token,
    get_refresh_token_expiry,
    verify_access_token,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"


@router.get("/login")
async def login(request: Request):
    state = secrets.token_urlsafe(16)
    request.session["oauth_state"] = state

    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "access_type": "offline",
        "prompt": "consent",
    }
    return RedirectResponse(f"{GOOGLE_AUTH_URL}?{urlencode(params)}")


@router.get("/callback")
async def callback(
    code: str,
    state: str,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    stored_state = request.session.get("oauth_state")
    if stored_state != state:
        raise HTTPException(status_code=400, detail="Invalid state parameter")

    # Google에서 토큰 교환
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            GOOGLE_TOKEN_URL,
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )
        token_data = token_resp.json()

        userinfo_resp = await client.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {token_data['access_token']}"},
        )
        userinfo = userinfo_resp.json()

    # DB에 사용자 생성/조회
    result = await session.exec(select(User).where(User.email == userinfo["email"]))
    user = result.first()

    if not user:
        user = User(
            email=userinfo["email"],
            name=userinfo.get("name", ""),
            picture_url=userinfo.get("picture"),
        )
        session.add(user)
    else:
        user.name = userinfo.get("name", user.name)
        user.picture_url = userinfo.get("picture", user.picture_url)
        user.updated_at = datetime.utcnow()
        session.add(user)

    # Refresh Token 생성 및 저장
    refresh_token_str = create_refresh_token()
    refresh_token = RefreshToken(
        user_id=user.id,
        token=refresh_token_str,
        expires_at=get_refresh_token_expiry(),
    )
    session.add(refresh_token)
    await session.commit()
    await session.refresh(user)

    # JWT Access Token 생성
    access_token = create_access_token(user.id)

    response = RedirectResponse(f"{settings.FRONTEND_URL}/login/callback")
    response.set_cookie(
        "access_token", access_token,
        httponly=True, samesite="lax", secure=False, max_age=1800
    )
    response.set_cookie(
        "refresh_token", refresh_token_str,
        httponly=True, samesite="lax", secure=False, max_age=604800
    )
    return response


@router.post("/refresh")
async def refresh(request: Request, response: Response, session: AsyncSession = Depends(get_session)):
    refresh_token_str = request.cookies.get("refresh_token")
    if not refresh_token_str:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    result = await session.exec(
        select(RefreshToken).where(RefreshToken.token == refresh_token_str)
    )
    token_record = result.first()

    if not token_record or token_record.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Refresh token expired or invalid")

    access_token = create_access_token(token_record.user_id)
    response.set_cookie(
        "access_token", access_token,
        httponly=True, samesite="lax", secure=False, max_age=1800
    )
    return {"success": True, "data": {"message": "Token refreshed"}}


@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    refresh_token_str = request.cookies.get("refresh_token")
    if refresh_token_str:
        result = await session.exec(
            select(RefreshToken).where(RefreshToken.token == refresh_token_str)
        )
        token_record = result.first()
        if token_record:
            await session.delete(token_record)
            await session.commit()

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"success": True, "data": {"message": "로그아웃 완료"}}


@router.get("/me")
async def me(current_user: User = Depends(get_current_user)):
    return {
        "success": True,
        "data": {
            "id": current_user.id,
            "email": current_user.email,
            "name": current_user.name,
            "picture_url": current_user.picture_url,
        },
    }
