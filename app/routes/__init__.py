from fastapi import APIRouter
from app.routes.user import router as user_router
from app.routes.stock import router as stock_router
from app.routes.order import router as order_router

main_router = APIRouter()

main_router.include_router(user_router)
main_router.include_router(stock_router)
main_router.include_router(order_router)
