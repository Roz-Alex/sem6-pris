import strawberry

from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI
from contextlib import asynccontextmanager

from db import database, init_db
import schema

# Определяем lifespan функцию для управления жизненным циклом приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код, выполняющийся при запуске приложения
    print("Подключение к базе данных licenses...")
    await database.connect()
    print("Инициализация базы данных licenses...")
    await init_db() # Инициализируем БД при запуске
    yield # Приложение запущено
    # Код, выполняющийся при остановке приложения
    print("Отключение от базы данных licenses...")
    await database.disconnect()

# Создаем экземпляр FastAPI приложения с lifespan
app = FastAPI(
    title="License Service GraphQL API",
    description="GraphQL API for managing licenses.",
    version="0.1.0",
    lifespan=lifespan # Передаем lifespan функцию
)

# Создаем GraphQLRouter, передав ему схему из schema.py
graphql_app = GraphQLRouter(schema.schema)

# Монтируем GraphQL endpoint к основному приложению FastAPI
# Теперь GraphQL API будет доступен по адресу http://localhost:4002/graphql
app.include_router(graphql_app, prefix="/graphql")

# Простой маршрут для проверки состояния сервиса
@app.get("/")
def read_root():
    return {"message": "License Service GraphQL API is running!"}

# Точка входа для запуска сервера uvicorn
# Запуск: uvicorn services.licenses.main:app --host 0.0.0.0 --port 4002
if __name__ == "__main__":
    import uvicorn
    # Запускаем сервер на localhost:4002
    uvicorn.run(app, host="0.0.0.0", port=4002)
