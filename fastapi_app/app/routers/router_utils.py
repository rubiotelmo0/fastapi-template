# -*- coding: utf-8 -*-
"""Util/Helper functions for router definitions."""
import logging
from typing import NoReturn

from fastapi import HTTPException

def raise_and_log_error(my_logger: logging.Logger, status_code: int, message: str) -> NoReturn:
    """Raise an HTTPException and log the error."""
    my_logger.error(message)
    raise HTTPException(status_code, message)
