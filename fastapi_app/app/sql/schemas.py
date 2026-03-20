# -*- coding: utf-8 -*-
"""Classes for request and response schema definitions."""
# pylint: disable=too-few-public-methods
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator  # pylint: disable=no-name-in-module


def _normalize_item_name(value: str | None) -> str | None:
    """Trim item names and reject blank values."""
    if value is None:
        return None
    normalized_name = value.strip()
    if not normalized_name:
        raise ValueError("Item name cannot be blank.")
    return normalized_name


def _normalize_description(value: str | None) -> str | None:
    """Trim item descriptions when provided."""
    if value is None:
        return None
    return value.strip()


class Message(BaseModel):
    """Message schema definition."""

    detail: Optional[str] = Field(default=None, examples=["Error or success message"])


class HealthCheck(BaseModel):
    """Health check payload."""

    status: str = Field(default="ok", examples=["ok"])
    app_name: str = Field(examples=["FastAPI Template"])
    version: str = Field(examples=["0.1.0"])


class ItemBase(BaseModel):
    """Shared item schema fields."""

    name: str = Field(
        min_length=1,
        max_length=120,
        description="Short unique item name.",
        examples=["starter-item"],
    )
    description: str = Field(
        default="",
        description="Human readable description for the item.",
        examples=["Replace this example entity with your own domain model."],
    )
    is_active: bool = Field(default=True, description="Whether the item is active.", examples=[True])

    @field_validator("name", mode="before")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        """Trim and validate item names before persistence."""
        normalized_name = _normalize_item_name(value)
        if normalized_name is None:
            raise ValueError("Item name cannot be null.")
        return normalized_name

    @field_validator("description", mode="before")
    @classmethod
    def normalize_description(cls, value: str) -> str:
        """Trim item descriptions before persistence."""
        normalized_description = _normalize_description(value)
        if normalized_description is None:
            return ""
        return normalized_description


class Item(ItemBase):
    """Item schema definition."""

    model_config = ConfigDict(from_attributes=True)
    id: int = Field(description="Primary key/identifier of the item.", examples=[1])
    creation_date: Optional[datetime] = Field(
        default=None,
        description="Creation timestamp.",
        examples=["2026-03-16T10:15:00Z"],
    )
    update_date: Optional[datetime] = Field(
        default=None,
        description="Last update timestamp.",
        examples=["2026-03-16T10:15:00Z"],
    )


class ItemCreate(ItemBase):
    """Payload to create a new item."""


class ItemUpdate(BaseModel):
    """Payload to partially update an item."""

    name: Optional[str] = Field(default=None, min_length=1, max_length=120, examples=["starter-item"])
    description: Optional[str] = Field(
        default=None,
        examples=["Updated description for the starter item."],
    )
    is_active: Optional[bool] = Field(default=None, examples=[False])

    @field_validator("name", mode="before")
    @classmethod
    def normalize_name(cls, value: str | None) -> str | None:
        """Trim and validate item names before persistence."""
        return _normalize_item_name(value)

    @field_validator("description", mode="before")
    @classmethod
    def normalize_description(cls, value: str | None) -> str | None:
        """Trim item descriptions before persistence."""
        return _normalize_description(value)


class ItemSummary(BaseModel):
    """Derived summary for the example item catalog."""

    total_items: int = Field(description="Total number of stored items.", examples=[3])
    active_items: int = Field(description="Number of active items.", examples=[2])
    inactive_items: int = Field(description="Number of inactive items.", examples=[1])
    item_names: list[str] = Field(
        description="Ordered list of item names currently stored.",
        examples=[["starter-item", "inactive-item", "reportable-item"]],
    )
