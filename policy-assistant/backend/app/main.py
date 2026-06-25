
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import api_router
from app.core.config import get_settings
from app.core.app_logging import configure_logging, get_logger

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator:

    configure_logging()
    settings = get_settings()
    logger = get_logger(__name__)

    settings.upload_dir.mkdir(parents=True,exist_ok=True)

    logger.info(
        "Application Started..",
        app_name=settings.app_name,
        app_env=settings.app_env
    )

    yield

    logger.info(
        "Application Stopped.."
    )

def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.api_prefix)

    return app

app = create_app()



