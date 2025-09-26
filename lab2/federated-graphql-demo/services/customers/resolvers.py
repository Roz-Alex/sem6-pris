from typing import List, Optional

from db import get_customer_by_id, get_all_customers, create_customer, update_customer, delete_customer


async def get_customer_resolver(id: int) -> Optional['Customer']:
    from schema import Customer

    db_customer = await get_customer_by_id(id)
    if db_customer:
        return Customer(id=db_customer['id'], name=db_customer['name'], description=db_customer['description'], inn=db_customer['inn'])
    return None

async def get_all_customers_resolver() -> List['Customer']:
    from schema import Customer

    db_customers = await get_all_customers()
    return [Customer(id=customer['id'], name=customer['name'], description=customer['description'], inn=customer['inn']) for customer in db_customers]

async def create_customer_resolver(customer_data: 'CustomerInput') -> 'Customer':
    from schema import Customer

    db_customer = await create_customer(customer_data.name, customer_data.description, customer_data.inn)
    return Customer(id=db_customer['id'], name=db_customer['name'], description=db_customer['description'], inn=db_customer['inn'])

async def update_customer_resolver(customer_data: 'CustomerUpdateInput') -> Optional['Customer']:
    from schema import Customer

    db_customer = await update_customer(customer_data.id, customer_data.name, customer_data.description, customer_data.inn)
    if db_customer:
        return Customer(id=db_customer['id'], name=db_customer['name'], description=db_customer['description'], inn=db_customer['inn'])
    return None

async def delete_customer_resolver(id: int) -> bool:
    return await delete_customer(id)
