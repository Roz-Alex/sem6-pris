from typing import List, Optional
from datetime import datetime

from db import get_license_by_id, create_license, update_license, delete_license


async def get_license_resolver(id: int) -> Optional['License']:
    from schema import License

    db_license = await get_license_by_id(id)
    if db_license:
        return License(
            id=db_license['id'],
            name=db_license['name'],
            issued_date=db_license['issued_date'],
            expiry_date=db_license['expiry_date'],
            type=db_license['type'],
            users_count=db_license['users_count'],
            servers_count=db_license['servers_count'],
        )
    return None


async def create_license_resolver(license_data: 'LicenseInput') -> 'License':
    from schema import License, LicenseInput

    db_license = await create_license(
        name=license_data.name,
        issued_date=license_data.issued_date,
        expiry_date=license_data.expiry_date,
        license_type=license_data.type,
        users_count=license_data.users_count,
        servers_count=license_data.servers_count,
    )
    return License(
        id=db_license['id'],
        name=db_license['name'],
        issued_date=db_license['issued_date'],
        expiry_date=db_license['expiry_date'],
        type=db_license['type'],
        users_count=db_license['users_count'],
        servers_count=db_license['servers_count'],
    )

async def update_license_resolver(license_data: 'LicenseUpdateInput') -> Optional['License']:
    from schema import License, LicenseUpdateInput

    db_license = await update_license(
        license_id=license_data.id,
        name=license_data.name,
        issued_date=license_data.issued_date,
        expiry_date=license_data.expiry_date,
        license_type=license_data.type,
        users_count=license_data.users_count,
        servers_count=license_data.servers_count,
    )
    return License(
        id=db_license['id'],
        name=db_license['name'],
        issued_date=db_license['issued_date'],
        expiry_date=db_license['expiry_date'],
        type=db_license['type'],
        users_count=db_license['users_count'],
        servers_count=db_license['servers_count'],
    )

async def delete_license_resolver(id: int) -> bool:
    return await delete_license(id)
