import strawberry

from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI
from contextlib import asynccontextmanager

from db import init_db
import schema


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Подключение к базе данных access (MongoDB)...")
    print("Инициализация базы данных access (MongoDB)...")

    await init_db()
    yield # Приложение запущено

    print("Отключение от базы данных access (MongoDB)...")
    from db import client

    client.close()

app = FastAPI(
    title="Access Service GraphQL API",
    description="GraphQL API for managing customer access records.",
    version="0.1.0",
    lifespan=lifespan
)

graphql_app = GraphQLRouter(schema.schema)

app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
def read_root():
    return {"message": "Access Service GraphQL API is running!"}

# Точка входа для запуска сервера uvicorn
# Запуск: uvicorn services.access.main:app --host 0.0.0.0 --port 4003
if __name__ == "__main__":
    import uvicorn
    # Запускаем сервер на localhost:4003
    uvicorn.run(app, host="0.0.0.0", port=4003)
