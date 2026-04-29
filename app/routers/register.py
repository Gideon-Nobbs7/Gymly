from fastapi import APIRouter

from app.routers.members import router as member_router
from app.routers.payments import router as payment_router

routers = [member_router, payment_router]

v1_router = APIRouter(prefix="/api/v1")

for router in routers:
    v1_router.include_router(router)
