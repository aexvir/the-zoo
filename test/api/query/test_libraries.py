import pytest

pytestmark = pytest.mark.django_db


@pytest.fixture
def generate_libraries(library_factory):
    library_factory(
        id=1,
        owner="platform",
        name="fancy one",
        lifecycle="fixed",
        impact="employees",
        slack_channel="#slack",
        sonarqube_project="sonar",
        repository__id=124,
        repository__remote_id=125,
        repository__owner="jasckson",
        repository__name="thiwer",
        repository__url="https://gitlab.com/thiwer/thiwer",
    )
    library_factory(
        id=2,
        owner="platform soft",
        name="fancy second",
        lifecycle="fixed",
        impact="employees",
        slack_channel="#slack-second",
        sonarqube_project="sonar-qub",
        repository__id=22,
        repository__remote_id=234,
        repository__owner="peter",
        repository__name="parker",
        repository__url="https://gitlab.com/peter/parker",
    )
    library_factory(
        id=3,
        owner="platform software",
        name="fancy third",
        lifecycle="fixed",
        impact="employees",
        slack_channel="#slack-third",
        sonarqube_project="sonar-qube",
        repository__id=455,
        repository__remote_id=2134539,
        repository__owner="black",
        repository__name="smith",
        repository__url="https://gitlab.com/black/smith",
    )
    library_factory(
        id=4,
        owner="platform software plus",
        name="fancy fourth",
        lifecycle="fixed",
        impact="employees",
        slack_channel="#slack-fourth",
        sonarqube_project="sonar-qubeee",
        repository__id=467,
        repository__remote_id=124,
        repository__owner="clark",
        repository__name="kent",
        repository__url="https://gitlab.com/clark/kent",
    )


def test_empty(snapshot, call_api):
    query = """
    query {
      allLibraries {
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


def test_all(snapshot, call_api, generate_libraries):
    query = """
    query {
      allLibraries {
        totalCount
        edges {
          node {
            id
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


def test_with_repository(snapshot, call_api, generate_libraries):
    query = """
    query {
      allLibraries {
        totalCount
        edges {
          node {
            id
            owner
            name
            lifecycle
            impact
            slackChannel
            sonarqubeProject
            docsUrl
            libraryUrl
            repository {
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


def test_first(snapshot, call_api, generate_libraries):
    query = """
    query {
      allLibraries(first: 3) {
        totalCount
        edges {
          node {
            id
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


def test_first_after(snapshot, call_api, generate_libraries):
    query = """
    query {
      allLibraries(first: 2, after: "MQ==") {
        totalCount
        edges {
          node {
            id
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


def test_last(snapshot, call_api, generate_libraries):
    query = """
    query {
      allLibraries(last: 3) {
        totalCount
        edges {
          node {
            id
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


def test_last_before(snapshot, call_api, generate_libraries):
    query = """
    query {
      allLibraries(last: 1, before: "MQ==") {
        totalCount
        edges {
          node {
            id
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
