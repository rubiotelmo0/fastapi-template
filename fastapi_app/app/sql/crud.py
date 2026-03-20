# -*- coding: utf-8 -*-
"""Functions that interact with the database."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def create_item(
    db: AsyncSession,
    item_data: schemas.ItemCreate,
) -> models.Item:
    """Persist a new item into the database."""
    db_item = models.Item(
        **item_data.model_dump(),
    )
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


async def get_item_list(db: AsyncSession) -> list[models.Item]:
    """Load all items from the database."""
    stmt = select(models.Item).order_by(models.Item.id)
    return await get_list_statement_result(db, stmt)


async def get_item(db: AsyncSession, item_id: int) -> models.Item | None:
    """Load an item from the database."""
    return await get_element_by_id(db, models.Item, item_id)


async def update_item(
    db: AsyncSession,
    item: models.Item,
    item_data: schemas.ItemUpdate,
) -> models.Item:
    """Persist changes to an existing item."""
    for field, value in item_data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    await db.commit()
    await db.refresh(item)
    return item


async def delete_item(db: AsyncSession, item: models.Item) -> None:
    """Delete the selected item."""
    await db.delete(item)
    await db.commit()


async def get_list_statement_result(db: AsyncSession, stmt):
    """Execute the given statement and return a list of items."""
    result = await db.execute(stmt)
    return result.unique().scalars().all()


async def get_element_by_id(db: AsyncSession, model, element_id):
    """Retrieve any DB element by id."""
    if element_id is None:
        return None
    return await db.get(model, element_id)
