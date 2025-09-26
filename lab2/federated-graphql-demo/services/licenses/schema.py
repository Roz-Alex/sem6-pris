import strawberry
import strawberry.schema

from typing import List, Optional
from datetime import datetime


@strawberry.federation.type(keys=['id'])
class License:
    id: int
    name: str
    issued_date: datetime
    expiry_date: Optional[datetime]
    type: str
    users_count: Optional[int]
    servers_count: Optional[int]

    @classmethod
    def resolve_reference(cls, id: int) -> "License":
        import resolvers

        return resolvers.get_license_resolver(id)

# Определяем аргументы для мутаций
@strawberry.input
class LicenseInput:
    name: str
    issued_date: datetime
    expiry_date: Optional[datetime] = None
    type: str # 'server' или 'user'
    users_count: Optional[int] = None
    servers_count: Optional[int] = None

@strawberry.input
class LicenseUpdateInput:
    id: int
    name: Optional[str] = None
    issued_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    type: Optional[str] = None # 'server' или 'user'
    users_count: Optional[int] = None
    servers_count: Optional[int] = None

@strawberry.type
class Query:
    @strawberry.field
    def get_license(self, id: int) -> Optional['License']:
        import resolvers

        return resolvers.get_license_resolver(id)


# Определяем Mutation (изменения)
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_license(self, license_data: 'LicenseInput') -> 'License':
        import resolvers

        return resolvers.create_license_resolver(license_data)

    @strawberry.mutation
    def update_license(self, license_data: 'LicenseUpdateInput') -> Optional['License']:
        import resolvers
        return resolvers.update_license_resolver(license_data)

    @strawberry.mutation
    def delete_license(self, id: int) -> bool:
        import resolvers
        return resolvers.delete_license_resolver(id)


schema = strawberry.federation.Schema(query=Query, mutation=Mutation)
