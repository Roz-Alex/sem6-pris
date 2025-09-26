import strawberry

from typing import List, Optional
import strawberry.schema

import resolvers


@strawberry.federation.type(keys=["id"])
class Customer:
    id: int

@strawberry.federation.type(keys=["id"])
class License:
    id: int


@strawberry.federation.type(keys=['id'])
class AccessRecord:
    id: str
    license_id: int
    customer_id: int
    repo_uname: str
    repo_password: str
    access_info: Optional[str]

    @strawberry.field
    def customer(self) -> Customer:
        return Customer(id=self.customer_id)

    @strawberry.field
    def license(self) -> License:
        return License(id=self.license_id)


# Определяем аргументы для мутаций
@strawberry.input
class AccessRecordInput:
    license_id: int
    customer_id: int
    repo_uname: str
    repo_password: str
    access_info: Optional[str] = None

@strawberry.input
class AccessRecordUpdateInput:
    id: str
    license_id: Optional[int] = None
    customer_id: Optional[int] = None
    repo_uname: Optional[str] = None
    repo_password: Optional[str] = None
    access_info: Optional[str] = None

# Определяем Query (запросы)
@strawberry.type
class Query:
    @strawberry.field
    def get_access_record(self, id: str) -> Optional['AccessRecord']:
        import resolvers

        return resolvers.get_access_record_resolver(id)

    @strawberry.field
    def get_access_records_for_customer(self, customer_id: int) -> List['AccessRecord']:
        import resolvers

        return resolvers.get_access_records_for_customer_resolver(customer_id)

    @strawberry.field
    def get_access_records_for_license(self, license_id: int) -> List['AccessRecord']:
        import resolvers

        return resolvers.get_access_records_for_license_resolver(license_id)

# Определяем Mutation
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_access_record(self, record_data: 'AccessRecordInput') -> 'AccessRecord':
        import resolvers

        return resolvers.create_access_record_resolver(record_data)

    @strawberry.mutation
    def update_access_record(self, record_data: 'AccessRecordUpdateInput') -> Optional['AccessRecord']:
        import resolvers

        return resolvers.update_access_record_resolver(record_data)

    @strawberry.mutation
    def delete_access_record(self, id: str) -> bool:
        import resolvers
        return resolvers.delete_access_record_resolver(id)


schema = strawberry.federation.Schema(query=Query, mutation=Mutation, types=[Customer, License])
# --- АЖНО ---
