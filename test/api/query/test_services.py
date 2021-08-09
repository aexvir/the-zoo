import pytest

pytestmark = pytest.mark.django_db


@pytest.fixture
def generate_services(service_factory):
    service_factory(
        id=1,
        name="martinez",
        owner="michaelbennett",
        impact="profit",
        docs_url="https://docsurl",
        pagerduty_service="/services",
        slack_channel="https://slackchannel",
        lifecycle="fixed",
        repository__id=78,
        repository__remote_id=239,
        repository__owner="jasckson",
        repository__name="thiwer",
        repository__url="https://gitlab.com/thiwer/thiwer",
    )
    service_factory(
        id=2,
        name="alex",
        owner="amstrong",
        impact="profit",
        docs_url="https://docsurl",
        pagerduty_service="/services",
        slack_channel="https://slackchannel",
        lifecycle="fixed",
        repository__id=48,
        repository__remote_id=99,
        repository__owner="colisn",
        repository__name="farel",
        repository__url="https://gitlab.com/farel/colins",
    )
    service_factory(
        id=3,
        name="artinez",
        owner="bennett",
        impact="profit",
        docs_url="https://docsurl",
        pagerduty_service="/services",
        slack_channel="https://slackchannel",
        lifecycle="fixed",
        repository__id=234,
        repository__remote_id=9234,
        repository__owner="Daniel",
        repository__name="Amstrong",
        repository__url="https://gitlab.com/daniel/amstrong",
    )
    service_factory(
        id=4,
        name="john",
        owner="benneto",
        impact="profit",
        docs_url="https://docsurl",
        pagerduty_service="/services",
        slack_channel="https://slackchannel",
        lifecycle="fixed",
        repository__id=3434,
        repository__remote_id=349,
        repository__owner="josh",
        repository__name="blanc",
        repository__url="https://gitlab.com/josh/blanc",
    )

    service_factory(
        id=12,
        name="simmons-mitchell",
        owner="dedward",
        impact="profit",
        docs_url="https://docsurl",
        pagerduty_service="/services",
        slack_channel="https://slackchannel",
        lifecycle="fixed",
        repository__id=4543,
        repository__remote_id=990,
        repository__owner="imosley",
        repository__name="leblanc",
        repository__url="https://gitlab.com/schultzcarolyn/leblanc",
    )


@pytest.fixture
def generate_services_with_environments(service_factory, environment_factory):
    service = service_factory(
        id=1,
        name="martinez",
        owner="michaelbennett",
        impact="profit",
        docs_url="https://docsurl",
        pagerduty_service="/services",
        slack_channel="https://slackchannel",
        lifecycle="fixed",
        repository__id=78,
        repository__remote_id=239,
        repository__owner="jasckson",
        repository__name="thiwer",
        repository__url="https://gitlab.com/thiwer/thiwer",
    )
    environment_factory(
        id=1,
        service=service,
        name="production",
        service_urls=["https://serviceurl1", "https://serviceurl2"],
        dashboard_url="https://dashboardurl",
        health_check_url="https://healthcheckurl",
    )
    environment_factory(
        id=2,
        service=service,
        name="staging",
        service_urls=["https://serviceurl1", "https://serviceurl2"],
        dashboard_url="https://dashboardurl",
        health_check_url="https://healthcheckurl",
    )


def test_empty(snapshot, call_api):
    query = """
    query {
      allServices {
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


def test_all(snapshot, call_api, generate_services):
    query = """
    query {
      allServices {
        totalCount
        edges {
          node {
            id
            owner
            name
            lifecycle
            impact
            slackChannel
            pagerdutyService
            docsUrl
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


def test_with_repository(snapshot, call_api, generate_services):
    query = """
    query {
      allServices {
        totalCount
        edges {
          node {
            id
            name
            owner
            lifecycle
            impact
            slackChannel
            pagerdutyService
            docsUrl
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


def test_with_environment(snapshot, call_api, generate_services_with_environments):
    query = """
    query {
      allServices {
        totalCount
        edges {
          node {
            id
            name
            owner
            lifecycle
            impact
            slackChannel
            pagerdutyService
            docsUrl
            allEnvironments {
              totalCount
              edges {
                node {
                  name
                  serviceUrls
                  dashboardUrl
                  healthCheckUrl
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


def test_first(snapshot, call_api, generate_services):
    query = """
    query {
      allServices(first: 3) {
        totalCount
        edges {
          node {
            id
            owner
            lifecycle
            impact
            slackChannel
            pagerdutyService
            docsUrl
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


def test_first_after(snapshot, call_api, generate_services):
    query = """
    query {
      allServices(first: 2, after: "MQ==") {
        totalCount
        edges {
          node {
            id
            owner
            lifecycle
            impact
            slackChannel
            pagerdutyService
            docsUrl
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


def test_last(snapshot, call_api, generate_services):
    query = """
    query {
      allServices(last: 3) {
        totalCount
        edges {
          node {
            id
            owner
            lifecycle
            impact
            slackChannel
            pagerdutyService
            docsUrl
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


def test_last_before(snapshot, call_api, generate_services):
    query = """
    query {
      allServices(last: 1, before: "MQ==") {
        totalCount
        edges {
          node {
            id
            owner
            lifecycle
            impact
            slackChannel
            pagerdutyService
            docsUrl
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
