# -*- coding: utf-8 -*-
"""FastAPI router definitions."""
import logging
import os

from fastapi import APIRouter, Depends, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.business_logic.item_summary import ItemSummaryService
from app.dependencies import get_db, get_item_summary_service
from app.sql import crud, schemas

from .router_utils import raise_and_log_error

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    "/",
    summary="Health check endpoint",
    response_model=schemas.HealthCheck,
    tags=["Health"],
)
async def health_check():
    """Endpoint to check if everything started correctly."""
    logger.debug("GET '/' endpoint called.")
    return schemas.HealthCheck(
        status="ok",
        app_name=os.getenv("APP_NAME", "FastAPI Template"),
        version=os.getenv("APP_VERSION", "0.1.0"),
    )


@router.post(
    "/items",
    response_model=schemas.Item,
    summary="Create a new item",
    status_code=status.HTTP_201_CREATED,
    tags=["Items"],
)
async def create_item(
    item_schema: schemas.ItemCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new example resource."""
    logger.debug("POST '/items' endpoint called.")
    try:
        return await crud.create_item(db, item_schema)
    except IntegrityError:
        await db.rollback()
        raise_and_log_error(logger, status.HTTP_409_CONFLICT, "An item with that name already exists.")


@router.get(
    "/items",
    response_model=list[schemas.Item],
    summary="Retrieve the item list",
    tags=["Items"],
)
async def get_item_list(
    db: AsyncSession = Depends(get_db),
):
    """Return all stored items."""
    logger.debug("GET '/items' endpoint called.")
    return await crud.get_item_list(db)


@router.get(
    "/items/summary",
    response_model=schemas.ItemSummary,
    summary="Retrieve an item catalog summary",
    tags=["Items"],
)
async def get_item_summary(
    db: AsyncSession = Depends(get_db),
    item_summary_service: ItemSummaryService = Depends(get_item_summary_service),
):
    """Return a derived summary built from stored items."""
    logger.debug("GET '/items/summary' endpoint called.")
    return await item_summary_service.get_item_summary(db)


@router.get(
    "/items/{item_id}",
    summary="Retrieve a single item by id",
    responses={
        status.HTTP_200_OK: {
            "model": schemas.Item,
            "description": "Requested item.",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": schemas.Message,
            "description": "Item not found",
        },
    },
    tags=["Items"],
)
async def get_single_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Return a single item."""
    logger.debug("GET '/items/%i' endpoint called.", item_id)
    item = await crud.get_item(db, item_id)
    if not item:
        raise_and_log_error(logger, status.HTTP_404_NOT_FOUND, f"Item {item_id} not found.")
    return item


@router.patch(
    "/items/{item_id}",
    response_model=schemas.Item,
    summary="Update an item",
    responses={
        status.HTTP_200_OK: {
            "model": schemas.Item,
            "description": "Updated item.",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": schemas.Message,
            "description": "Item not found",
        },
    },
    tags=["Items"],
)
async def update_item(
    item_id: int,
    item_schema: schemas.ItemUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update the selected item."""
    logger.debug("PATCH '/items/%i' endpoint called.", item_id)
    item = await crud.get_item(db, item_id)
    if not item:
        raise_and_log_error(logger, status.HTTP_404_NOT_FOUND, f"Item {item_id} not found.")
    try:
        return await crud.update_item(db, item, item_schema)
    except IntegrityError:
        await db.rollback()
        raise_and_log_error(logger, status.HTTP_409_CONFLICT, "An item with that name already exists.")


@router.delete(
    "/items/{item_id}",
    response_model=schemas.Message,
    summary="Delete an item",
    responses={
        status.HTTP_200_OK: {
            "model": schemas.Message,
            "description": "Item successfully deleted.",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": schemas.Message,
            "description": "Item not found",
        },
    },
    tags=["Items"],
)
async def delete_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Delete the selected item."""
    logger.debug("DELETE '/items/%i' endpoint called.", item_id)
    item = await crud.get_item(db, item_id)
    if not item:
        raise_and_log_error(logger, status.HTTP_404_NOT_FOUND, f"Item {item_id} not found.")
    await crud.delete_item(db, item)
    return schemas.Message(detail=f"Item {item_id} deleted.")
