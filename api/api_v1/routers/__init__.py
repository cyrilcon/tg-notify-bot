from fastapi import APIRouter

from config import config
from .notification import router as notification_router

routers_list = [
    notification_router,
]

routers = APIRouter(
    prefix=config.api.v1.prefix,
)
for router in routers_list:
    routers.include_router(router)
