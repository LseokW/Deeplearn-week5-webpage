import hmac
import hashlib
import httpx
from app.config import settings

POLAR_API_BASE = "https://sandbox-api.polar.sh/v1"


async def create_checkout_session(user_id: str, user_email: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{POLAR_API_BASE}/checkouts/",
            headers={"Authorization": f"Bearer {settings.POLAR_ACCESS_TOKEN}"},
            json={
                "product_id": settings.POLAR_PRODUCT_ID,
                "success_url": settings.POLAR_SUCCESS_URL + "?checkout_id={CHECKOUT_ID}",
                "customer_email": user_email,
                "metadata": {"user_id": user_id, "week_id": "week5"},
            },
        )
        response.raise_for_status()
        return response.json()


async def get_checkout_status(checkout_id: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{POLAR_API_BASE}/checkouts/{checkout_id}",
            headers={"Authorization": f"Bearer {settings.POLAR_ACCESS_TOKEN}"},
        )
        response.raise_for_status()
        return response.json()


def verify_webhook_signature(payload: bytes, webhook_id: str) -> bool:
    if not settings.POLAR_WEBHOOK_SECRET:
        return False
    expected = hmac.new(
        settings.POLAR_WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, webhook_id)
