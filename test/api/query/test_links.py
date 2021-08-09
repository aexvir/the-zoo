import pytest

pytestmark = pytest.mark.django_db


@pytest.fixture
def generate_links(component_base_factory, link_factory):
    component = component_base_factory(
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
    link_factory(
        id=1, name="link", entity=component, icon="smile", url="https://some.url.com"
    )
    link_factory(
        id=2, name="link", entity=component, icon="smile", url="https://some.url.com"
    )
    link_factory(
        id=3, name="link", entity=component, icon="smile", url="https://some.url.com"
    )
    link_factory(
        id=4, name="link", entity=component, icon="smile", url="https://some.url.com"
    )
    link_factory(
        id=5, name="link", entity=component, icon="smile", url="https://some.url.com"
    )


def test_empty(snapshot, call_api):
    query = """
    query {
      allLinks {
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


def test_all(snapshot, call_api, generate_links):
    query = """
    query {
      allLinks {
        totalCount
        edges {
          node {
            id
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
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_with_entity(snapshot, call_api, generate_links):
    query = """
    query {
      allLinks {
        totalCount
        edges {
          node {
            id
            name
            icon
            url
            entity {
              name
              label
              kind
              type
              owner
              description
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


def test_first(snapshot, call_api, generate_links):
    query = """
    query {
      allLinks(first: 3) {
        totalCount
        edges {
          node {
            id
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
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_first_after(snapshot, call_api, generate_links):
    query = """
    query {
      allLinks(first: 2, after: "MQ==") {
        totalCount
        edges {
          node {
            id
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
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_last(snapshot, call_api, generate_links):
    query = """
    query {
      allLinks(last: 3) {
        totalCount
        edges {
          node {
            id
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
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_last_before(snapshot, call_api, generate_links):
    query = """
    query {
      allLinks(last: 1, before: "MQ==") {
        totalCount
        edges {
          node {
            id
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
    """
    response = call_api(query)
    snapshot.assert_match(response)
