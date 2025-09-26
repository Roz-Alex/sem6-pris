import databases
import os

from pymongo import MongoClient
from pymongo.errors import PyMongoError
from typing import Optional, List
from bson import ObjectId


MONGO_USER = "mongo_user"
MONGO_PASSWORD = "mongopassword"
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB_NAME = "access_db"

DATABASE_URL = os.getenv("MONGODB_URL", f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB_NAME}?authSource=admin")

client = MongoClient(DATABASE_URL)
db = client[MONGO_DB_NAME]

access_collection = db["customer_access"]

async def init_db():
    access_collection.create_index("license_id")
    access_collection.create_index("customer_id")
    print("Инициализация БД access завершена (индексы).")

# Функции для CRUD операций

async def get_access_record_by_id(access_id: str):
    try:
        object_id = ObjectId(access_id)
        record = access_collection.find_one({"_id": object_id})
        if record:
            record['id'] = str(record['_id'])
            del record['_id']
        return record
    except PyMongoError:
        return None
    except Exception:
        return None

async def get_access_records_for_customer(customer_id: int):
    try:
        records = access_collection.find({"customer_id": customer_id})
        result = []
        for record in records:
            record['id'] = str(record['_id'])
            del record['_id']
            result.append(record)
        return result
    except PyMongoError:
        return []

async def get_access_records_for_license(license_id: int):
    try:
        records = access_collection.find({"license_id": license_id})
        result = []
        for record in records:
            record['id'] = str(record['_id'])
            del record['_id']
            result.append(record)
        return result
    except PyMongoError:
        return []

async def create_access_record(license_id: int, customer_id: int, repo_uname: str, repo_password: str, access_info: Optional[str]):
    record_data = {
        "license_id": license_id,
        "customer_id": customer_id,
        "repo_uname": repo_uname,
        "repo_password": repo_password,
        "access_info": access_info
    }
    result = access_collection.insert_one(record_data)

    return await get_access_record_by_id(str(result.inserted_id))

async def update_access_record(access_id: str, license_id: Optional[int] = None, customer_id: Optional[int] = None,
                               repo_uname: Optional[str] = None, repo_password: Optional[str] = None, access_info: Optional[str] = None):
    try:
        updates = {}
        if license_id is not None:
            updates['license_id'] = license_id
        if customer_id is not None:
            updates['customer_id'] = customer_id
        if repo_uname is not None:
            updates['repo_uname'] = repo_uname
        if repo_password is not None:
            updates['repo_password'] = repo_password
        if access_info is not None:
            updates['access_info'] = access_info

        if not updates:
            return await get_access_record_by_id(access_id)

        object_id = ObjectId(access_id)
        result = access_collection.update_one({"_id": object_id}, {"$set": updates})
        if result.matched_count > 0:
            return await get_access_record_by_id(access_id)
        else:
            return None
    except PyMongoError:
        return None
    except Exception:
        return None

async def delete_access_record(access_id: str):
    try:
        object_id = ObjectId(access_id)
        result = access_collection.delete_one({"_id": object_id})
        return result.deleted_count > 0
    except PyMongoError:
        return False
    except Exception:
        return False
