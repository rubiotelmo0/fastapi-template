# -*- coding: utf-8 -*-
"""Additional business logic for the example item resource."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.sql import crud, models, schemas

logger = logging.getLogger(__name__)


class ItemSummaryService:
    """Build derived responses from stored item models."""

    @staticmethod
    def _build_summary(items: list[models.Item]) -> schemas.ItemSummary:
        """Convert stored items into a simple catalog summary."""
        active_items = [item for item in items if item.is_active]
        return schemas.ItemSummary(
            total_items=len(items),
            active_items=len(active_items),
            inactive_items=len(items) - len(active_items),
            item_names=[item.name for item in items],
        )

    async def get_item_summary(self, db: AsyncSession) -> schemas.ItemSummary:
        """Load items from the database and return a derived summary."""
        logger.debug("Building item summary")
        items = await crud.get_item_list(db)
        return self._build_summary(items)
