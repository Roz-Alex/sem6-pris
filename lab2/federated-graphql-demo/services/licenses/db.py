import databases
import sqlalchemy
import os

from sqlalchemy import MetaData, create_engine, Table, Column, Integer, String, TIMESTAMP, ForeignKey, CheckConstraint
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://service_user:pgpassword@postgres:5432/graphql_demo")

database = databases.Database(DATABASE_URL)

engine = create_engine(DATABASE_URL.replace("postgresql+asyncpg", "postgresql"))

metadata = MetaData()

licenses_table = Table(
    "licenses",
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('name', String, index=True, nullable=False),
    Column('issued_date', TIMESTAMP(timezone=True), nullable=False),
    Column('expiry_date', TIMESTAMP(timezone=True), nullable=True),
    Column('type', String, nullable=False), # 'server' или 'user'
    Column('users_count', Integer, nullable=True),
    Column('servers_count', Integer, nullable=True),

    CheckConstraint(
        "(users_count IS NOT NULL AND servers_count IS NULL) OR "
        "(users_count IS NULL AND servers_count IS NOT NULL) OR "
        "(users_count IS NOT NULL AND servers_count IS NOT NULL)",
        name="check_users_or_servers"
    ),
    CheckConstraint(
        "type IN ('server', 'user')",
        name="check_license_type"
    )
)

async def init_db():
    # Создаем таблицы (если они не существуют)
    # ВАЖНО: Таблица customers должна существовать до создания licenses_table из-за внешнего ключа
    # Это может потребовать координации при первом запуске всех сервисов или создания общей схемы
    # Пока предположим, что таблица customers уже создана (например, сервис customers запускается первым)
    metadata.create_all(engine)

# Функции для CRUD операций (примеры)

async def get_license_by_id(license_id: int):
    query = licenses_table.select().where(licenses_table.c.id == license_id)
    result = await database.fetch_one(query)
    if result:
        return dict(result)
    return None


async def create_license(name: str, issued_date: TIMESTAMP, expiry_date: Optional[TIMESTAMP],
                         license_type: str, users_count: Optional[int], servers_count: Optional[int]):
    query = licenses_table.insert().values(
        name=name,
        issued_date=issued_date,
        expiry_date=expiry_date,
        type=license_type,
        users_count=users_count,
        servers_count=servers_count,
    )
    license_id = await database.execute(query)
    return await get_license_by_id(license_id)

async def update_license(license_id: int, name: Optional[str] = None, issued_date: Optional[datetime] = None,
                         expiry_date: Optional[datetime] = None, license_type: Optional[str] = None,
                         users_count: Optional[int] = None, servers_count: Optional[int] = None):
    updates = {}
    if name is not None:
        updates['name'] = name
    if issued_date is not None:
        updates['issued_date'] = issued_date
    if expiry_date is not None:
        updates['expiry_date'] = expiry_date
    if license_type is not None:
        updates['type'] = license_type
    if users_count is not None:
        updates['users_count'] = users_count
    if servers_count is not None:
        updates['servers_count'] = servers_count

    if not updates:
        return await get_license_by_id(license_id) # Нечего обновлять

    query = licenses_table.update().where(licenses_table.c.id == license_id).values(**updates)
    await database.execute(query)
    return await get_license_by_id(license_id)

async def delete_license(license_id: int):
    query = licenses_table.delete().where(licenses_table.c.id == license_id)
    result = await database.execute(query)
    # result - количество затронутых строк
    return result > 0 # True если строка была удалена