import graphene

from . import types
from .mutations import Mutation as ZooMutation
from .query import Query as ZooQuery


class Query(ZooQuery, graphene.ObjectType):
    pass


class Mutation(ZooMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    types=[
        types.CheckResult,
        types.Dependency,
        types.DependencyUsage,
        types.Entity,
        types.Group,
        types.Issue,
        types.Library,
        types.Link,
        types.Repository,
        types.Service,
    ],
)
