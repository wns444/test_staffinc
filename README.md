# Task manager

Backend-приложение для управления задачами.

Ожидаемое время выполнения: 1 час

## Структура проекта

```text
tasks_api/
├── main.py              ← точка входа (аналог AppModule)
├── requirements.txt
└── tasks/
    ├── dto.py           ← Pydantic-схемы (аналог *.dto.ts)
    ├── service.py       ← бизнес-логика, хранение в памяти
    └── controller.py    ← HTTP-роутер (аналог *.controller.ts)
```

## Ключевые решения

- `dto.py` — Pydantic v2 с аналогом class-validator:
- `Field(..., min_length=1, max_length=255)` — декларативные ограничения прямо в схеме
- `@field_validator("title")` — кастомный валидатор на пустые строки из пробелов
- `TaskStatus(str, Enum)` — строгое перечисление для поля status
- `service.py` — чистый слой логики без HTTP:
- In-memory хранилище (`List[TaskResponseDto]`) с автоинкрементным счётчиком
- `find_one()` возвращает Optional — контроллер сам решает, как обработать None
- `controller.py` — только HTTP-слой:
- `Depends(get_tasks_service)` — dependency injection (аналог NestJS DI)
- `HTTPException(404)` с человекочитаемым сообщением при ненайденной задаче
- Реализован GET/DELETE `/tasks/{id}`

## Запуск

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Swagger UI → `http://127.0.0.1:8000/docs`