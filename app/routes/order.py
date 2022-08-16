from fastapi import APIRouter, HTTPException
from ..models.order import Order, OrderBaseModel

router = APIRouter()


@router.get("/order/{user_id}", response_model=list[OrderBaseModel])
async def user_orders(user_id: int):
    return Order.orders_for_user(user_id)


@router.post("/order/{order_id}/cancel/", response_model=OrderBaseModel)
async def cancel_order(order_id: int):
    order = Order.get(order_id)
    if not order:
        raise HTTPException(404, "User not found!")
    if order.succeed:
        raise HTTPException(403, "Order is already succeeded")
    elif order.cancelled:
        raise HTTPException(403, "Order is already cancelled")
    order.cancelled = True
    return order
