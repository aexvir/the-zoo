from math import ceil

import graphene
from django.apps import apps
from graphene import relay

from ..analytics.models import Dependency, DependencyType, DependencyUsage
from ..auditing.models import Issue
from ..entities.models import Entity, Group, Link
from ..globalsearch.indexer import IndexType
from ..globalsearch.meili_client import meili_client
from ..libraries.models import Library
from ..repos.models import Repository
from ..services.models import Service
from . import types
from .paginator import Paginator

DependencyTypeEnum = graphene.Enum.from_enum(DependencyType)
SearchTypeEnum = graphene.Enum.from_enum(IndexType)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_issues = relay.ConnectionField(
        types.IssueConnection,
        description="List of issues. Returns first 10 nodes if pagination is not specified.",
    )
    all_services = relay.ConnectionField(
        types.ServiceConnection,
        description="List of services. Returns first 10 nodes if pagination is not specified.",
    )
    all_repositories = relay.ConnectionField(
        types.RepositoryConnection,
        description="List of repositories. Returns first 10 nodes if pagination is not specified.",
    )
    all_dependencies = relay.ConnectionField(
        types.DependencyConnection,
        dependency_type=DependencyTypeEnum(),
        name=graphene.String(),
        description="List of dependency usages. Returns first 10 nodes if pagination is not specified.",
    )
    all_dependency_usages = relay.ConnectionField(
        types.DependencyUsageConnection,
        description="List of dependency usages. Returns first 10 nodes if pagination is not specified.",
    )

    all_search_results = relay.ConnectionField(
        types.SearchResultsConnection,
        description="List of search results. Returns first 10 nodes if pagination is not specified.",
        search_query=graphene.String(),
        search_type=SearchTypeEnum(),
    )
    all_entities = relay.ConnectionField(
        types.EntityConnection,
        description="List of entities. Returns first 10 nodes if pagination is not specified.",
    )
    all_libraries = relay.ConnectionField(
        types.LibraryConnection,
        description="List of libraries. Returns first 10 nodes if pagination is not specified.",
    )
    all_links = relay.ConnectionField(
        types.LinkConnection,
        description="List of links. Returns first 10 nodes if pagination is not specified.",
    )
    all_groups = relay.ConnectionField(
        types.GroupConnection,
        description="List of groups. Returns first 10 nodes if pagination is not specified.",
    )

    def resolve_all_issues(self, info, **kwargs):
        paginator = Paginator(**kwargs)
        total = Issue.objects.all().count()
        page_info = paginator.get_page_info(total)
        edges = []

        for i, issue in enumerate(
            Issue.objects.all()[
                paginator.slice_from : paginator.slice_to  # Ignore PEP8Bear
            ]
        ):
            cursor = paginator.get_edge_cursor(i + 1)
            node = types.Issue.from_db(issue)
            edges.append(types.IssueConnection.Edge(node=node, cursor=cursor))

        return types.IssueConnection(
            page_info=page_info, edges=edges, total_count=total
        )

    def resolve_all_services(self, info, **kwargs):
        paginator = Paginator(**kwargs)
        total = Service.objects.all().count()
        page_info = paginator.get_page_info(total)
        edges = []

        for i, service in enumerate(
            Service.objects.all()[
                paginator.slice_from : paginator.slice_to  # Ignore PEP8Bear
            ]
        ):
            cursor = paginator.get_edge_cursor(i + 1)
            node = types.Service.from_db(service)
            edges.append(types.ServiceConnection.Edge(node=node, cursor=cursor))

        return types.ServiceConnection(
            page_info=page_info, edges=edges, total_count=total
        )

    def resolve_all_repositories(self, info, **kwargs):
        paginator = Paginator(**kwargs)
        total = Repository.objects.all().count()
        page_info = paginator.get_page_info(total)
        edges = []

        for i, repo in enumerate(
            Repository.objects.all()[
                paginator.slice_from : paginator.slice_to  # Ignore PEP8Bear
            ]
        ):
            cursor = paginator.get_edge_cursor(i + 1)
            node = types.Repository.from_db(repo)
            edges.append(types.RepositoryConnection.Edge(node=node, cursor=cursor))

        return types.RepositoryConnection(
            page_info=page_info, edges=edges, total_count=total
        )

    def resolve_all_dependencies(self, info, **kwargs):
        paginator = Paginator(**kwargs)
        filtered_dependencies = Dependency.objects.all()

        if "name" in kwargs:
            filtered_dependencies = filtered_dependencies.filter(
                name__icontains=kwargs["name"]
            )

        if "dependency_type" in kwargs:
            filtered_dependencies = filtered_dependencies.filter(
                type=kwargs["dependency_type"]
            )

        total = filtered_dependencies.count()
        page_info = paginator.get_page_info(total)
        edges = []

        for i, dependency in enumerate(
            filtered_dependencies[
                paginator.slice_from : paginator.slice_to  # Ignore PEP8Bear
            ]
        ):
            cursor = paginator.get_edge_cursor(i + 1)
            node = types.Dependency.from_db(dependency)
            edges.append(types.DependencyConnection.Edge(node=node, cursor=cursor))

        return types.DependencyConnection(
            page_info=page_info, edges=edges, total_count=total
        )

    def resolve_all_dependency_usages(self, info, **kwargs):
        paginator = Paginator(**kwargs)
        total = DependencyUsage.objects.all().count()
        page_info = paginator.get_page_info(total)
        edges = []

        for i, dependency_usage in enumerate(
            DependencyUsage.objects.all()[
                paginator.slice_from : paginator.slice_to  # Ignore PEP8Bear
            ]
        ):
            cursor = paginator.get_edge_cursor(i + 1)
            node = types.DependencyUsage.from_db(dependency_usage)
            edges.append(types.DependencyUsageConnection.Edge(node=node, cursor=cursor))

        return types.DependencyUsageConnection(
            page_info=page_info, edges=edges, total_count=total
        )

    def resolve_all_entites(self, info, **kwargs):
        paginator = Paginator(**kwargs)
        total = Entity.objects.all().count()
        page_info = paginator.get_page_info(total)
        edges = []

        for i, entity in enumerate(
            Entity.objects.all()[
                paginator.slice_from : paginator.slice_to  # Ignore PEP8Bear
            ]
        ):
            cursor = paginator.get_edge_cursor(i + 1)
            node = types.Entity.from_db(entity)
            edges.append(types.EntityConnection.Edge(node=node, cursor=cursor))

        return types.EntityConnection(
            page_info=page_info, edges=edges, total_count=total
        )

    def resolve_all_links(self, info, **kwargs):
        paginator = Paginator(**kwargs)
        total = Link.objects.all().count()
        page_info = paginator.get_page_info(total)
        edges = []

        for i, link in enumerate(
            Link.objects.all()[
                paginator.slice_from : paginator.slice_to  # Ignore PEP8Bear
            ]
        ):
            cursor = paginator.get_edge_cursor(i + 1)
            node = types.Link.from_db(link)
            edges.append(types.LinkConnection.Edge(node=node, cursor=cursor))

        return types.LinkConnection(page_info=page_info, edges=edges, total_count=total)

    def resolve_all_libraries(self, info, **kwargs):
        paginator = Paginator(**kwargs)
        total = Library.objects.all().count()
        page_info = paginator.get_page_info(total)
        edges = []

        for i, library in enumerate(
            Library.objects.all()[
                paginator.slice_from : paginator.slice_to  # Ignore PEP8Bear
            ]
        ):
            cursor = paginator.get_edge_cursor(i + 1)
            node = types.Library.from_db(library)
            edges.append(types.LibraryConnection.Edge(node=node, cursor=cursor))

        return types.LibraryConnection(
            page_info=page_info, edges=edges, total_count=total
        )

    def resolve_all_groups(self, info, **kwargs):
        paginator = Paginator(**kwargs)
        total = Group.objects.all().count()
        page_info = paginator.get_page_info(total)
        edges = []

        for i, group in enumerate(
            Group.objects.all()[
                paginator.slice_from : paginator.slice_to  # Ignore PEP8Bear
            ]
        ):
            cursor = paginator.get_edge_cursor(i + 1)
            node = types.Group.from_db(group)
            edges.append(types.GroupConnection.Edge(node=node, cursor=cursor))

        return types.GroupConnection(
            page_info=page_info, edges=edges, total_count=total
        )

    def resolve_all_search_results(self, info, **kwargs):
        paginator = Paginator(**kwargs)
        query_param = kwargs.get("search_query", "")
        search_type = kwargs.get("search_type", IndexType.Service.value)

        indexes = meili_client.get_indexes()
        # get all total counts for each meili index
        search_index = None
        total_count = {}
        for index in indexes:
            total_count[index["uid"]] = meili_client.get_index(index["uid"]).search(
                query=query_param, opt_params={"offset": 0, "limit": 1}
            )["nbHits"]

            if index["uid"] == search_type:
                search_index = index

        # get all results for requested index
        search_results = Query._get_all_for_index(
            query_param, search_index, total_count.get(search_index["uid"])
        )
        edges = []
        for i, search_result in enumerate(
            search_results[paginator.slice_from : paginator.slice_to]
        ):
            cursor = paginator.get_edge_cursor(i + 1)
            edges.append(
                types.SearchResultsConnection.Edge(node=search_result, cursor=cursor)
            )

        return types.SearchResultsConnection(
            page_info=paginator.get_page_info(total_count[search_type]),
            edges=edges,
            total_services_count=total_count[IndexType.Service.value],
            total_analytics_count=total_count[IndexType.Dependency.value],
        )

    @staticmethod
    def _get_all_for_index(query_param, search_index, total_count):
        limit, search_results = 100, []

        if not any([total_count, search_index]):
            return search_results

        pages = ceil(total_count / limit)
        for page in range(pages):
            results = meili_client.get_index(search_index["uid"]).search(
                query=query_param, opt_params={"offset": page * limit, "limit": limit}
            )
            search_results.extend(
                Query._objects_from_result(results["hits"], search_index)
            )

        return search_results

    @staticmethod
    def _objects_from_result(search_results, index):
        result_objects = []
        try:
            model = apps.get_model(index["uid"], index["name"])
            for i, result in enumerate(search_results):
                model_object = model.objects.get(pk=result["id"])
                if index["name"] == IndexType.Dependency.name:
                    dependency = types.Dependency.from_db(model_object)
                    node = types.SearchResult(id=i, dependency=dependency)
                if index["name"] == IndexType.Service.name:
                    service = types.Service.from_db(model_object)
                    node = types.SearchResult(id=i, service=service)
                result_objects.append(node)
        except LookupError:
            pass

        return result_objects
