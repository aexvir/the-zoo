import pytest

pytestmark = pytest.mark.django_db


@pytest.fixture
def generate_groups(group_factory):
    group_factory(
        id=1, product_owner="john", project_owner="doe", maintainers=["clark", "kent"]
    )
    group_factory(
        id=24,
        product_owner="black",
        project_owner="smith",
        maintainers=["black", "smith"],
    )
    group_factory(
        id=244,
        product_owner="vanguard",
        project_owner="shield",
        maintainers=["vanguard", "shield"],
    )
    group_factory(
        id=246, product_owner="lich", project_owner="king", maintainers=["lich", "king"]
    )


def test_empty(snapshot, call_api):
    query = """
    query {
      allGroups {
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


def test_all(snapshot, call_api, generate_groups):
    query = """
    query {
      allGroups {
        totalCount
        edges {
          node {
            id
            productOwner
            projectOwner
            maintainers
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


def test_first(snapshot, call_api, generate_groups):
    query = """
    query {
      allGroups(first: 3) {
        totalCount
        edges {
          node {
            id
            productOwner
            projectOwner
            maintainers
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


def test_first_after(snapshot, call_api, generate_groups):
    query = """
    query {
      allGroups(first: 2, after: "MQ==") {
        totalCount
        edges {
          node {
            id
            productOwner
            projectOwner
            maintainers
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


def test_last(snapshot, call_api, generate_groups):
    query = """
    query {
      allGroups(last: 3) {
        totalCount
        edges {
          node {
            id
            productOwner
            projectOwner
            maintainers
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


def test_last_before(snapshot, call_api, generate_groups):
    query = """
    query {
      allGroups(last: 1, before: "MQ==") {
        totalCount
        edges {
          node {
            id
            productOwner
            projectOwner
            maintainers
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
