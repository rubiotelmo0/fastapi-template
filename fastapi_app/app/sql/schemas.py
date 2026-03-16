# -*- coding: utf-8 -*-
"""Classes for request and response schema definitions."""
# pylint: disable=too-few-public-methods
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field  # pylint: disable=no-name-in-module


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
