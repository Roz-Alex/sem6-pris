import strawberry

from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI
from contextlib import asynccontextmanager

from db import database, init_db
import schema

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Подключение к базе данных...")
    await database.connect()
    print("Инициализация базы данных (создание таблиц)...")
    await init_db()
    yield # Приложение запущено
    print("Отключение от базы данных...")
    await database.disconnect()

app = FastAPI(
    title="Customer Service GraphQL API",
    description="GraphQL API for managing customers.",
    version="0.1.0",
    lifespan=lifespan
)

graphql_app = GraphQLRouter(schema.schema)

app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
def read_root():
    return {"message": "Customer Service GraphQL API is running!"}

# Запуск: uvicorn services.customers.main:app --host 0.0.0.0 --port 4001
if __name__ == "__main__":
    import uvicorn
    # Запускаем сервер на localhost:4001
    uvicorn.run(app, host="0.0.0.0", port=4001)
