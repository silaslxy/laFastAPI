from fastapi import APIRouter
from ping.api.ping import router
ping_router = APIRouter()

# prefix有正则校验 不允许为空
ping_router.include_router(router, prefix="/ping", tags=["ping模块"])