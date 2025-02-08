from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api import routers
from database import session_manager


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Some logic, at the beginning of the application
        yield
        # Some logic, at the end of the application
        await session_manager.dispose()

    app = FastAPI(
        title="Notification API",
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
        description="API for sending generated notifications",
        version="1.0.0",
    )
    app.include_router(routers)

    return app
