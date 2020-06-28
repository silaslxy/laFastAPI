from fastapi import APIRouter
from demo.api.item import item_router
from demo.api.user import user_router

demo_router = APIRouter()

demo_router.include_router(item_router, prefix="/items", tags=["项目模块"])
demo_router.include_router(user_router, prefix="/users", tags=["用户模块"])
