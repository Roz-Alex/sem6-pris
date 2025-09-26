from db import get_access_record_by_id, get_access_records_for_customer, get_access_records_for_license, create_access_record, update_access_record, delete_access_record
from typing import List, Optional


async def get_access_record_resolver(id: str) -> Optional['AccessRecord']:
    from schema import AccessRecord

    db_record = await get_access_record_by_id(id)
    if db_record:
        return AccessRecord(
            id=db_record['id'],
            license_id=db_record['license_id'],
            customer_id=db_record['customer_id'],
            repo_uname=db_record['repo_uname'],
            repo_password=db_record['repo_password'],
            access_info=db_record['access_info']
        )
    return None

async def get_access_records_for_customer_resolver(customer_id: int) -> List['AccessRecord']:
    from schema import AccessRecord

    db_records = await get_access_records_for_customer(customer_id)
    return [
        AccessRecord(
            id=record['id'],
            license_id=record['license_id'],
            customer_id=record['customer_id'],
            repo_uname=record['repo_uname'],
            repo_password=record['repo_password'],
            access_info=record['access_info']
        ) for record in db_records
    ]


async def get_access_records_for_license_resolver(license_id: int) -> List['AccessRecord']:
    from schema import AccessRecord

    db_records = await get_access_records_for_license(license_id)
    return [
        AccessRecord(
            id=record['id'],
            license_id=record['license_id'],
            customer_id=record['customer_id'],
            repo_uname=record['repo_uname'],
            repo_password=record['repo_password'],
            access_info=record['access_info']
        ) for record in db_records
    ]

async def create_access_record_resolver(record_data: 'AccessRecordInput') -> 'AccessRecord':
    from schema import AccessRecord, AccessRecordInput # Импортируем внутри функции

    db_record = await create_access_record(
        license_id=record_data.license_id,
        customer_id=record_data.customer_id,
        repo_uname=record_data.repo_uname,
        repo_password=record_data.repo_password,
        access_info=record_data.access_info
    )
    return AccessRecord(
        id=db_record['id'],
        license_id=db_record['license_id'],
        customer_id=db_record['customer_id'],
        repo_uname=db_record['repo_uname'],
        repo_password=db_record['repo_password'],
        access_info=db_record['access_info']
    )

async def update_access_record_resolver(record_data: 'AccessRecordUpdateInput') -> Optional['AccessRecord']:
    from schema import AccessRecord, AccessRecordUpdateInput
    db_record = await update_access_record(
        access_id=record_data.id,
        license_id=record_data.license_id,
        customer_id=record_data.customer_id,
        repo_uname=record_data.repo_uname,
        repo_password=record_data.repo_password,
        access_info=record_data.access_info
    )
    return AccessRecord(
        id=db_record['id'],
        license_id=db_record['license_id'],
        customer_id=db_record['customer_id'],
        repo_uname=db_record['repo_uname'],
        repo_password=db_record['repo_password'],
        access_info=db_record['access_info']
    )

async def delete_access_record_resolver(id: str) -> bool:
    return await delete_access_record(id)
