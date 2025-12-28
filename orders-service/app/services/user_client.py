import httpx

from fastapi import HTTPException

from app.core.config import settings


async def get_user(user_id: int) -> dict:
    url = f"{settings.USER_SERVICE_URL}/users/{user_id}/"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, timeout=5.0)
    if resp.status_code == 404:
        raise HTTPException(status_code=400, detail="Owner user not found")
    if resp.status_code >= 400:
        raise HTTPException(status_code=503, detail="User service unavailable")
    return resp.json()
