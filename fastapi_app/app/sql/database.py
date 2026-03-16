# -*- coding: utf-8 -*-
"""Database session configuration."""
import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = os.getenv(
    "SQLALCHEMY_DATABASE_URL",
    os.getenv("SQLALCHEMY_SQLITE_DATABASE_URI", "sqlite+aiosqlite:///./app.db"),
)

engine_args = {"echo": False}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine_args["connect_args"] = {"check_same_thread": False}

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    **engine_args,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    future=True,
)

Base = declarative_base()
