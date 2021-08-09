import pytest

pytestmark = pytest.mark.django_db


@pytest.fixture
def generate_components(
    component_base_factory,
    service_factory,
    repository_factory,
    link_factory,
    library_factory,
):
    c1 = component_base_factory(
        id=1,
        name="base",
        label="Base",
        type="database",
        description="This is my fancy component",
        kind="component",
        owner="platform",
        service=None,
        library=None,
        source__id=1,
        source__remote_id=1,
        source__owner="jasckson",
        source__name="thiwer",
        source__url="https://gitlab.com/thiwer/thiwer",
    )

    c2 = component_base_factory(
        id=2,
        name="base_2",
        label="Base 2",
        type="database 2",
        description="This is my fancy component 2",
        kind="component",
        owner="platformm2",
        service=None,
        library=None,
        source__id=12,
        source__remote_id=13,
        source__owner="peter",
        source__name="parker",
        source__url="https://gitlab.com/peter/parker",
    )

    component_base_factory(
        id=32,
        name="base_3",
        label="Base 3",
        type="database 3",
        description="This is my fancy component 3",
        kind="component",
        owner="platformm3",
        service=None,
        library=None,
        source__id=23,
        source__remote_id=234,
        source__owner="clark",
        source__name="kent",
        source__url="https://gitlab.com/clark/kent",
    )

    repository = repository_factory(
        id=22,
        remote_id=22,
        name="test_proj1",
        owner="john_doe1",
        url="https://github.com/john_doe1/test_proj1",
        provider="github",
    )

    service = service_factory(
        owner="platform",
        name="my-service",
        lifecycle="production",
        impact="employees",
        repository=repository,
        slack_channel="#platform-software",
        docs_url="https://docs.com",
    )

    component_base_factory(
        id=1245,
        name="service",
        label="Service",
        type="service",
        description="This is my fancy service",
        kind="component",
        owner="platform",
        service=service,
        library=None,
        source=repository,
    )

    link_factory(
        id=1,
        name="Datadog",
        url="https://dashboard.datadog.com",
        icon="poop",
        entity=c1,
    )
    link_factory(
        id=2,
        name="Sentry",
        url="https://sentry.skypicker.com",
        entity=c2,
    )

    library = library_factory(repository=repository)

    component_base_factory(
        id=15545,
        name="library",
        label="Library",
        type="library",
        description="This is my fancy library",
        kind="component",
        owner="platform",
        service=None,
        library=library,
        source=repository,
    )


def test_empty(snapshot, call_api):
    query = """
    query {
      allEntities {
        totalCount
        edges {
          node {
            id
          }
        }
      }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_all(snapshot, call_api, generate_components):
    query = """
    query {
      allEntities {
        totalCount
        edges {
          node {
            id
            name
            label
            kind
            type
            owner
            description
          }
        }
        pageInfo {
            hasPreviousPage
            hasNextPage
            startCursor
            endCursor
        }
      }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_with_source(snapshot, call_api, generate_components):
    query = """
    query {
      allEntities {
        totalCount
        edges {
          node {
            id
            name
            label
            kind
            type
            owner
            description
            source {
              remoteId
              owner
              name
              url
            }
          }
        }
        pageInfo {
            hasPreviousPage
            hasNextPage
            startCursor
            endCursor
        }
      }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_with_service(snapshot, call_api, generate_components):
    query = """
    query {
      allEntities {
        totalCount
        edges {
          node {
            id
            name
            label
            kind
            type
            owner
            description
            service {
              id
              owner
              lifecycle
              impact
              slackChannel
              pagerdutyService
              docsUrl
            }
          }
        }
        pageInfo {
            hasPreviousPage
            hasNextPage
            startCursor
            endCursor
        }
      }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_with_group(snapshot, call_api, generate_components):
    query = """
    query {
      allEntities {
        totalCount
        edges {
          node {
            id
            name
            label
            kind
            type
            owner
            description
            group {
              productOwner
              projectOwner
              maintainers
            }
          }
        }
        pageInfo {
            hasPreviousPage
            hasNextPage
            startCursor
            endCursor
        }
      }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_with_library(snapshot, call_api, generate_components):
    query = """
    query {
      allEntities {
        totalCount
        edges {
          node {
            id
            name
            label
            kind
            type
            owner
            description
            library {
                owner
                name
                lifecycle
                impact
                slackChannel
                sonarqubeProject
                docsUrl
                libraryUrl
            }
          }
        }
        pageInfo {
            hasPreviousPage
            hasNextPage
            startCursor
            endCursor
        }
      }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_with_links(snapshot, call_api, generate_components):
    query = """
    query {
      allEntities {
        totalCount
        edges {
          node {
            id
            name
            label
            kind
            type
            owner
            description
            allLinks {
              totalCount
              edges {
                node {
                  name
                  icon
                  url
                }
              }
              pageInfo {
                  hasPreviousPage
                  hasNextPage
                  startCursor
                  endCursor
              }
            }
          }
        }
        pageInfo {
            hasPreviousPage
            hasNextPage
            startCursor
            endCursor
        }
      }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_first(snapshot, call_api, generate_components):
    query = """
    query {
      allEntities(first: 3) {
        totalCount
        edges {
          node {
            id
            name
            label
            kind
            type
            owner
            description
          }
        }
        pageInfo {
            hasPreviousPage
            hasNextPage
            startCursor
            endCursor
        }
      }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_first_after(snapshot, call_api, generate_components):
    query = """
    query {
      allEntities(first: 2, after: "MQ==") {
        totalCount
        edges {
          node {
            id
            name
            label
            kind
            type
            owner
            description
          }
        }
        pageInfo {
            hasPreviousPage
            hasNextPage
            startCursor
            endCursor
        }
      }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_last(snapshot, call_api, generate_components):
    query = """
    query {
      allEntities(last: 3) {
        totalCount
        edges {
          node {
            id
            name
            label
            kind
            type
            owner
            description
          }
        }
        pageInfo {
            hasPreviousPage
            hasNextPage
            startCursor
            endCursor
        }
      }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_last_before(snapshot, call_api, generate_components):
    query = """
    query {
      allEntities(last: 1, before: "MQ==") {
        totalCount
        edges {
          node {
            id
            name
            label
            kind
            type
            owner
            description
          }
        }
        pageInfo {
            hasPreviousPage
            hasNextPage
            startCursor
            endCursor
        }
      }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)
