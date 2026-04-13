from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.dependencies import get_current_user
from app.models import User, Purchase
from app.services.content_service import get_sections_metadata, get_section_content, get_image_path

router = APIRouter(prefix="/api/content", tags=["content"])


async def check_purchase(user: User, session: AsyncSession) -> bool:
    result = await session.exec(
        select(Purchase).where(
            Purchase.user_id == user.id,
            Purchase.week_id == "week5",
            Purchase.status == "completed",
        )
    )
    return result.first() is not None


@router.get("/week5")
async def get_week5_sections(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    sections = get_sections_metadata()
    purchased = await check_purchase(current_user, session)
    for s in sections:
        s["locked"] = not purchased
    return {"success": True, "data": {"sections": sections, "purchased": purchased}}


@router.get("/week5/{section_id}")
async def get_section(
    section_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    purchased = await check_purchase(current_user, session)
    if not purchased:
        raise HTTPException(
            status_code=403,
            detail={"code": "PAYMENT_REQUIRED", "message": "콘텐츠 열람을 위해 구매가 필요합니다."},
        )

    content = get_section_content(section_id)
    if content is None:
        raise HTTPException(status_code=404, detail="섹션을 찾을 수 없습니다.")

    return {"success": True, "data": {"section_id": section_id, "content": content}}


@router.get("/week5/images/{filename}")
async def get_image(
    filename: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    purchased = await check_purchase(current_user, session)
    if not purchased:
        raise HTTPException(status_code=403, detail="구매가 필요합니다.")

    image_path = get_image_path(filename)
    if image_path is None:
        raise HTTPException(status_code=404, detail="이미지를 찾을 수 없습니다.")

    return FileResponse(image_path)
