import strawberry

from typing import List, Optional


@strawberry.federation.type(keys=['id'])
class Customer:
    id: int
    name: str
    description: str
    inn: int

    @classmethod
    def resolve_reference(cls, id: int) -> "Customer":
        import resolvers
        return resolvers.get_customer_resolver(id)

@strawberry.input
class CustomerInput:
    name: str
    description: Optional[str] = None
    inn: int

@strawberry.input
class CustomerUpdateInput:
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    inn: Optional[int] = None

@strawberry.type
class Query:
    @strawberry.field
    def get_customer(self, id: int) -> Optional['Customer']:
        import resolvers
        return resolvers.get_customer_resolver(id)

    @strawberry.field
    def get_all_customers(self) -> List['Customer']:
        import resolvers
        return resolvers.get_all_customers_resolver()

    # get_all_customers: List[Customer] = strawberry.field(resolver=resolvers.get_all_customers_resolver)

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_customer(self, customer_data: 'CustomerInput') -> 'Customer':
        import resolvers
        return resolvers.create_customer_resolver(customer_data)

    @strawberry.mutation
    def update_customer(self, customer_data: 'CustomerUpdateInput') -> Optional['Customer']:
        import resolvers
        return resolvers.update_customer_resolver(customer_data)

    @strawberry.mutation
    def delete_customer(self, id: int) -> bool:
        import resolvers
        return resolvers.delete_customer_resolver(id)

schema = strawberry.federation.Schema(query=Query, mutation=Mutation)
