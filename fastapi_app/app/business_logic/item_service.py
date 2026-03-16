# -*- coding: utf-8 -*-
"""Service layer for the example item resource."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.sql import crud, models, schemas

logger = logging.getLogger(__name__)


class ItemService:
    """Encapsulate item business rules."""

    @staticmethod
    def _normalize_name(name: str) -> str:
        """Trim and validate an item name."""
        normalized_name = name.strip()
        if not normalized_name:
            raise ValueError("Item name cannot be blank.")
        return normalized_name

    async def create_item(self, db: AsyncSession, item_data: schemas.ItemCreate) -> models.Item:
        """Create a new item."""
        logger.debug("Creating item %s", item_data.name)
        return await crud.create_item(
            db,
            name=self._normalize_name(item_data.name),
            description=item_data.description.strip(),
            is_active=item_data.is_active,
        )

    async def list_items(self, db: AsyncSession) -> list[models.Item]:
        """Return all items."""
        return await crud.get_item_list(db)

    async def get_item(self, db: AsyncSession, item_id: int) -> models.Item | None:
        """Return one item by id."""
        return await crud.get_item(db, item_id)

    async def update_item(
        self,
        db: AsyncSession,
        item: models.Item,
        item_data: schemas.ItemUpdate,
    ) -> models.Item:
        """Update an existing item."""
        update_data = item_data.model_dump(exclude_unset=True)
        if "name" in update_data and update_data["name"] is not None:
            update_data["name"] = self._normalize_name(update_data["name"])
        if "description" in update_data and update_data["description"] is not None:
            update_data["description"] = update_data["description"].strip()
        return await crud.update_item(db, item, update_data)

    async def delete_item(self, db: AsyncSession, item: models.Item) -> None:
        """Delete an item."""
        await crud.delete_item(db, item)
