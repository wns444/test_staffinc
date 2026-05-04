"""
tasks/controller.py
TasksController — HTTP-слой, маршруты и обработка запросов.
Аналог NestJS @Controller() с @Get / @Post декораторами.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.dto import CreateTaskDto, TaskResponseDto
from app.service import TasksService

router = APIRouter(prefix="/tasks", tags=["Tasks"])
_tasks_service = TasksService()


def get_tasks_service() -> TasksService:
    """FastAPI-зависимость, возвращающая singleton-сервис."""
    return _tasks_service


@router.post(
    "",
    response_model=TaskResponseDto,
    status_code=status.HTTP_201_CREATED,
    summary="Создать задачу",
)
def create_task(
    dto: CreateTaskDto,
    service: TasksService = Depends(get_tasks_service),
) -> TaskResponseDto:
    """
    Создаёт новую задачу.

    - **title**: обязательное, непустая строка (1–255 символов)
    - **description**: необязательное (до 1000 символов)
    - **status**: `new` | `in_progress` | `done`
    """
    return service.create(dto)


@router.get(
    "",
    response_model=List[TaskResponseDto],
    status_code=status.HTTP_200_OK,
    summary="Получить все задачи",
)
def get_tasks(
    service: TasksService = Depends(get_tasks_service),
) -> List[TaskResponseDto]:
    """Возвращает список всех созданных задач."""
    return service.find_all()


@router.get(
    "/{task_id}",
    response_model=TaskResponseDto,
    status_code=status.HTTP_200_OK,
    summary="Получить задачу по ID",
    responses={404: {"description": "Задача не найдена"}},
)
def get_task(
    task_id: int,
    service: TasksService = Depends(get_tasks_service),
) -> TaskResponseDto:
    """
    Возвращает задачу по её **id**.

    Если задача не найдена — возвращает `404 Not Found`.
    """
    task = service.find_one(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с id={task_id} не найдена",
        )
    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    summary="Удалить задачу по ID",
    responses={404: {"description": "Задача не найдена"}},
)
def delete_task(
    task_id: int,
    service: TasksService = Depends(get_tasks_service),
) -> None:
    """
    Удаляет задачу по её **id**.

    Если задача не найдена — возвращает `404 Not Found`.
    """
    if not service.delete(task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с id={task_id} не найдена",
        )
    return None

