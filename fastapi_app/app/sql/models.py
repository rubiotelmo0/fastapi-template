# -*- coding: utf-8 -*-
"""Database models definitions. Table representations as class."""
from sqlalchemy import Boolean, Column, DateTime, Integer, String, TEXT
from sqlalchemy.sql import func

from .database import Base


class BaseModel(Base):
    """Base database table representation to reuse."""

    __abstract__ = True
    id = Column(Integer, primary_key=True)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    update_date = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        fields = ""
        for column in self.__table__.columns:
            if fields == "":
                fields = f"{column.name}='{getattr(self, column.name)}'"
            else:
                fields = f"{fields}, {column.name}='{getattr(self, column.name)}'"
        return f"<{self.__class__.__name__}({fields})>"

    @staticmethod
    def list_as_dict(items):
        """Return a list of items as dictionaries."""
        return [item.as_dict() for item in items]

    def as_dict(self):
        """Return the item as dict."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Item(BaseModel):
    """Example entity for the template."""

    __tablename__ = "item"
    name = Column(String(120), nullable=False, unique=True)
    description = Column(TEXT, nullable=False, default="")
    is_active = Column(Boolean, nullable=False, default=True)
