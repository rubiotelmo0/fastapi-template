# -*- coding: utf-8 -*-
"""Application dependency injector."""
import logging
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.business_logic.item_service import ItemService
from app.sql.database import SessionLocal

logger = logging.getLogger(__name__)

ITEM_SERVICE = ItemService()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield a database session for a single request."""
    logger.debug("Opening database session")
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


def get_item_service() -> ItemService:
    """Return the shared service layer instance."""
    return ITEM_SERVICE
