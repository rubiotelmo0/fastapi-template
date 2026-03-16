# -*- coding: utf-8 -*-
"""Main file to start FastAPI application."""
import logging.config
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers import main_router
from app.sql import database, models

# Configure logging ################################################################################
logging.config.fileConfig(os.path.join(os.path.dirname(__file__), "logging.ini"))
logger = logging.getLogger(__name__)


# App Lifespan #####################################################################################
@asynccontextmanager
async def lifespan(__app: FastAPI):
    """Lifespan context manager."""
    try:
        logger.info("Starting up")
        try:
            async with database.engine.begin() as conn:
                await conn.run_sync(models.Base.metadata.create_all)
        except Exception:
            logger.exception("Could not initialize the application")
        yield
    finally:
        logger.info("Shutting down database")
        await database.engine.dispose()


# OpenAPI Documentation ############################################################################
APP_NAME = os.getenv("APP_NAME", "FastAPI Template")
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
logger.info("Running app version %s", APP_VERSION)

DESCRIPTION = """
Starter FastAPI project with routers, dependencies, business logic, and async SQLAlchemy.
"""

tag_metadata = [
    {
        "name": "Health",
        "description": "Basic readiness endpoints for the API.",
    },
    {
        "name": "Items",
        "description": "Example CRUD endpoints you can replace with your own domain.",
    },
]

app = FastAPI(
    redoc_url=None,
    title=APP_NAME,
    description=DESCRIPTION,
    version=APP_VERSION,
    servers=[{"url": "/", "description": "Development"}],
    license_info={
        "name": "MIT License",
        "url": "https://choosealicense.com/licenses/mit/",
    },
    openapi_tags=tag_metadata,
    lifespan=lifespan,
)

app.include_router(main_router.router)
