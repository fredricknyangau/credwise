"""
Standard API response envelope.
All endpoints return a consistent shape for easy frontend parsing.
"""
from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "OK"
    data: T | None = None

    @classmethod
    def ok(cls, data: T, message: str = "OK") -> "APIResponse[T]":
        return cls(success=True, message=message, data=data)

    @classmethod
    def created(cls, data: T) -> "APIResponse[T]":
        return cls(success=True, message="Created successfully", data=data)

    @classmethod
    def no_content(cls, message: str = "Operation successful") -> "APIResponse[None]":
        return APIResponse(success=True, message=message, data=None)


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    detail: Any = None
