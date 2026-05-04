"""
tasks/dto.py
Data Transfer Objects — входящие и исходящие схемы данных задачи.
Аналог NestJS DTO + class-validator.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class TaskStatus(str, Enum):
    new = "new"
    in_progress = "in_progress"
    done = "done"


class CreateTaskDto(BaseModel):
    """Схема для создания задачи (POST /tasks)."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Название задачи (обязательное)",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Описание задачи (необязательное)",
    )
    status: TaskStatus = Field(
        ...,
        description="Статус: new | in_progress | done",
    )

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("title не может состоять только из пробелов")
        return v.strip()


class TaskResponseDto(BaseModel):
    """Схема ответа — задача с id."""

    id: int
    title: str
    description: Optional[str]
    status: TaskStatus

    model_config = {"from_attributes": True}
