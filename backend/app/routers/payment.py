from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.config import settings
from app.database import get_session
from app.dependencies import get_current_user
from app.models import User, Purchase
from app.services.payment_service import (
    create_checkout_session,
    get_checkout_status,
    verify_webhook_signature,
)

router = APIRouter(prefix="/api/payment", tags=["payment"])


@router.post("/checkout")
async def checkout(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    # 이미 구매한 경우 확인
    result = await session.exec(
        select(Purchase).where(
            Purchase.user_id == current_user.id,
            Purchase.week_id == "week5",
            Purchase.status == "completed",
        )
    )
    if result.first():
        raise HTTPException(status_code=400, detail="이미 구매한 콘텐츠입니다.")

    checkout_data = await create_checkout_session(current_user.id, current_user.email)

    purchase = Purchase(
        user_id=current_user.id,
        week_id="week5",
        polar_checkout_id=checkout_data["id"],
        status="pending",
    )
    session.add(purchase)
    await session.commit()

    return {
        "success": True,
        "data": {"checkout_url": checkout_data["url"]},
    }


@router.get("/success")
async def payment_success(
    checkout_id: str,
    session: AsyncSession = Depends(get_session),
):
    checkout_data = await get_checkout_status(checkout_id)

    if checkout_data.get("status") == "succeeded":
        result = await session.exec(
            select(Purchase).where(Purchase.polar_checkout_id == checkout_id)
        )
        purchase = result.first()
        if purchase and purchase.status != "completed":
            purchase.status = "completed"
            purchase.purchased_at = datetime.utcnow()
            session.add(purchase)
            await session.commit()

    return RedirectResponse(f"{settings.FRONTEND_URL}/checkout/success")


@router.post("/webhook")
async def polar_webhook(request: Request, session: AsyncSession = Depends(get_session)):
    payload = await request.body()
    webhook_id = request.headers.get("webhook-id", "")

    if not verify_webhook_signature(payload, webhook_id):
        raise HTTPException(status_code=400, detail="Invalid webhook signature")

    event = await request.json()
    if event.get("type") == "checkout.updated":
        checkout_data = event.get("data", {})
        if checkout_data.get("status") == "succeeded":
            result = await session.exec(
                select(Purchase).where(
                    Purchase.polar_checkout_id == checkout_data["id"]
                )
            )
            purchase = result.first()
            if purchase and purchase.status != "completed":
                purchase.status = "completed"
                purchase.purchased_at = datetime.utcnow()
                session.add(purchase)
                await session.commit()

    return {"success": True}


@router.get("/status")
async def payment_status(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    result = await session.exec(
        select(Purchase).where(
            Purchase.user_id == current_user.id,
            Purchase.week_id == "week5",
        )
    )
    purchase = result.first()

    purchased = purchase is not None and purchase.status == "completed"
    return {
        "success": True,
        "data": {
            "purchased": purchased,
            "purchased_at": purchase.purchased_at.isoformat() if purchase and purchase.purchased_at else None,
        },
    }
