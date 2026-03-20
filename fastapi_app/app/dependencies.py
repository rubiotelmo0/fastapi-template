# -*- coding: utf-8 -*-
"""Application dependency injector."""
import logging
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.business_logic.item_summary import ItemSummaryService
from app.sql.database import SessionLocal

logger = logging.getLogger(__name__)

ITEM_SUMMARY_SERVICE = ItemSummaryService()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield a database session for a single request."""
    logger.debug("Opening database session")
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


def get_item_summary_service() -> ItemSummaryService:
    """Return the shared business logic service instance."""
    return ITEM_SUMMARY_SERVICE
