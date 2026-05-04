
"""
main.py
Точка входа приложения — создание FastAPI-приложения и подключение роутеров.
Аналог app.module.ts в NestJS.
"""
 
from fastapi import FastAPI
from fastapi.responses import JSONResponse
 
from app.controller import router as tasks_router
 
app = FastAPI(
    title="Tasks API",
    description="Мини REST API для управления списком задач",
    version="1.0.0",
)

app.include_router(tasks_router)

@app.get("/", include_in_schema=False)
def root():
    return JSONResponse({"status": "ok", "docs": "/docs"})
 