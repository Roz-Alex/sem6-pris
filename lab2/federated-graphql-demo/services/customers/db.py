import databases
import sqlalchemy
import os

from sqlalchemy import MetaData, create_engine, Table, Column, Integer, String
from contextlib import asynccontextmanager
from typing import List, Optional


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://service_user:pgpassword@postgres:5432/graphql_demo")

database = databases.Database(DATABASE_URL)

engine = create_engine(DATABASE_URL.replace("postgresql+asyncpg", "postgresql"))

metadata = MetaData()

customers_table = Table(
    "customers",
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('name', String),
    Column('description', String),
    Column('inn', Integer, unique=True, index=True),
)

async def init_db():
    metadata.create_all(engine)


# Функции для CRUD операций

async def get_customer_by_id(customer_id: int):
    query = customers_table.select().where(customers_table.c.id == customer_id)
    result = await database.fetch_one(query)
    if result:
        return dict(result)
    return None

async def get_all_customers():
    query = customers_table.select()
    result = await database.fetch_all(query)
    return [dict(row) for row in result]

async def create_customer(name: str, description: str, inn: int):
    query = customers_table.insert().values(name=name, description=description, inn=inn)
    customer_id = await database.execute(query)
    # Получаем созданный объект
    return await get_customer_by_id(customer_id)

async def update_customer(customer_id: int, name: Optional[str] = None, description: Optional[str] = None, inn: Optional[int] = None):
    # Формируем словарь обновлений
    updates = {}
    if name is not None:
        updates['name'] = name
    if description is not None:
        updates['description'] = description
    if inn is not None:
        updates['inn'] = inn

    if not updates:
        return await get_customer_by_id(customer_id)

    query = customers_table.update().where(customers_table.c.id == customer_id).values(**updates)
    await database.execute(query)
    return await get_customer_by_id(customer_id)

async def delete_customer(customer_id: int):
    query = customers_table.delete().where(customers_table.c.id == customer_id)
    result = await database.execute(query)
    return result > 0
