"""
tasks/service.py
TasksService — бизнес-логика и хранение данных в памяти.
Аналог NestJS @Injectable() Service.
"""

from typing import List, Optional

from app.dto import CreateTaskDto, TaskResponseDto


class TasksService:
    """
    Хранит задачи в памяти (in-memory список).
    В реальном проекте здесь был бы SQLAlchemy-репозиторий.
    """

    def __init__(self) -> None:
        self._tasks: List[TaskResponseDto] = []
        self._counter: int = 0

    def create(self, dto: CreateTaskDto) -> TaskResponseDto:
        """Создаёт задачу и возвращает её с присвоенным id."""
        self._counter += 1
        task = TaskResponseDto(
            id=self._counter,
            title=dto.title,
            description=dto.description,
            status=dto.status,
        )
        self._tasks.append(task)
        return task

    def find_all(self) -> List[TaskResponseDto]:
        """Возвращает список всех задач."""
        return list(self._tasks)

    def find_one(self, task_id: int) -> Optional[TaskResponseDto]:
        """Возвращает задачу по id или None, если не найдена."""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def delete(self, task_id: int) -> bool:
        """Удаляет задачу по id и возвращает True, если удаление было успешным."""
        for task in self._tasks:
            if task.id == task_id:
                self._tasks.remove(task)
                return True
        return False