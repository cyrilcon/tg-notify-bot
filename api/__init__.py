from fastapi import APIRouter

from config import config
from .api_v1.routers import routers as routers_api_v1

routers = APIRouter(
    prefix=config.api.prefix,
)
routers.include_router(routers_api_v1)
