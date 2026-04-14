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
from app.models import User
from app.services.auth_service import create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"


@router.get("/login")
async def login():
    state = secrets.token_urlsafe(16)
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
    session: AsyncSession = Depends(get_session),
):
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
        if "access_token" not in token_data:
            err = token_data.get("error", "unknown")
            return RedirectResponse(f"{settings.FRONTEND_URL}/?error={err}")

        userinfo_resp = await client.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {token_data['access_token']}"},
        )
        userinfo = userinfo_resp.json()
        if "email" not in userinfo:
            return RedirectResponse(f"{settings.FRONTEND_URL}/?error=userinfo_failed")

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

    await session.commit()
    await session.refresh(user)

    access_token = create_access_token(user.id)
    return RedirectResponse(f"{settings.FRONTEND_URL}/login/callback?token={access_token}")


@router.post("/logout")
async def logout():
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
