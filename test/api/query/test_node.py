import pytest
from graphql_relay import to_global_id

pytestmark = pytest.mark.django_db


def test_service(snapshot, call_api, service_factory):
    service_factory(
        id=10,
        owner="bradltwat",
        name="allen-nobles",
        lifecycle="fixed",
        impact="sales",
        slack_channel="https://gitlab.slack",
        pagerduty_service="sales/P019873X9",
        docs_url="https://docs/skypicker/docs/",
    )
    id = to_global_id("Service", 10)
    query = f"""
    query {{
        node (id:"{id}") {{
            ... on Service {{
                id
                owner
                name
                lifecycle
                impact
                slackChannel
                pagerdutyService
                docsUrl
            }}
        }}
    }}
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_issue(snapshot, call_api, issue_factory):
    issue_factory(
        id=10,
        comment="Mars",
        kind_key="harris:reyes",
        remote_issue_id=234,
        last_check="2018-08-22T11:36:48Z",
        details={"lunch": "good", "money": True, "balance": 0},
    )
    id = to_global_id("Issue", 10)
    query = f"""
    query {{
      node (id: "{id}") {{
        ... on Issue {{
            id
            kindKey
            status
            details
            remoteIssueId
            comment
            lastCheck
            }}
        }}
    }}
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_repository(snapshot, call_api, repository_factory):
    repository_factory(
        id=10,
        name="james-rivera",
        owner="sharon54",
        url="https://gitlab.com/sharon54/jones-rivera",
        remote_id=2783,
    )
    id = to_global_id("Repository", 10)
    query = f"""
    query {{
      node (id: "{id}") {{
        ... on Repository {{
            id
            owner
            name
            url
            remoteId
            }}
        }}
    }}
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_dependency(snapshot, call_api, dependency_factory):
    dependency_factory(id=10, name="Python", type="Language")
    id = to_global_id("Dependency", 10)
    query = f"""
    query {{
      node (id: "{id}") {{
        ... on Dependency {{
            id
            name
            type
            }}
        }}
    }}
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_dependency_usage(snapshot, call_api, dependency_usage_factory):
    dependency_usage_factory(
        id=10,
        major_version=3,
        minor_version=2,
        patch_version=4,
        version="3.2.4",
        for_production="f",
    )
    id = to_global_id("DependencyUsage", 10)
    query = f"""
    query {{
      node (id: "{id}") {{
        ... on DependencyUsage {{
            id
            majorVersion
            minorVersion
            patchVersion
            forProduction
            version
            }}
        }}
    }}
    """
    response = call_api(query)
    snapshot.assert_match(response)
