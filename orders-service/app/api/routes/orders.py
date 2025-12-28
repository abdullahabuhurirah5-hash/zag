from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import provide_session
from app.schemas.order import OrderCreateSchema, OrderResponse
from app.services.order_service import crud_order
from app.services.user_client import get_user


orders_router = APIRouter(prefix="/orders", tags=["Orders"])


@orders_router.get("/health", status_code=204)
async def health() -> None:
    return None


@orders_router.post("/", response_model=OrderResponse)
async def create_order(order_in: OrderCreateSchema, session: AsyncSession = Depends(provide_session)):
    # Validate owner exists in user-service
    await get_user(order_in.owner_id)
    new_order = await crud_order.create(session, order_in)
    return new_order


@orders_router.get("/", response_model=List[OrderResponse])
async def list_orders(offset: int = 0, limit: int = 100, session: AsyncSession = Depends(provide_session)):
    orders = await crud_order.get_all(session, offset=offset, limit=limit)
    return orders


@orders_router.get("/{order_id}/", response_model=OrderResponse)
async def get_order(order_id: int, session: AsyncSession = Depends(provide_session)):
    order = await crud_order.get(session, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
