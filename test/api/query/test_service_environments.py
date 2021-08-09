import pytest

from zoo.repos.models import Repository
from zoo.services.models import Service

pytestmark = pytest.mark.django_db


@pytest.fixture
def generate_environments(service_factory, environment_factory):
    service = service_factory(
        id=1,
        name="martinez",
        owner="michaelbennett",
        impact="profit",
        docs_url="https://docsurl",
        pagerduty_service="sales/P019873X9",
        slack_channel="https://slackchannel",
        lifecycle="fixed",
    )
    environment_factory(
        id=1,
        service=service,
        name="production",
        service_urls=["https://serviceurlA1", "https://serviceurlA2"],
        dashboard_url="https://dashboardurlA",
        health_check_url="https://healthcheckurlA",
    )
    environment_factory(
        id=2,
        service=service,
        name="staging",
        service_urls=["https://serviceurlB1", "https://serviceurlB2"],
        dashboard_url="https://dashboardurlB",
        health_check_url="https://healthcheckurlB",
    )
    environment_factory(
        id=3,
        service=service,
        name="staging2",
        service_urls=["https://serviceurlC1", "https://serviceurlC2"],
        dashboard_url="https://dashboardurlC",
        health_check_url="https://healthcheckurlC",
    )
    environment_factory(
        id=4,
        service=service,
        name="staging3",
        service_urls=["https://serviceurlD1", "https://serviceurlD2"],
        dashboard_url="https://dashboardurlD",
        health_check_url="https://healthcheckurlD",
    )


def test_empty(snapshot, call_api):
    query = """
    query {
      allServices {
        totalCount
        edges {
          node {
            allEnvironments {
              totalCount
              edges {
                node {
                  id
                }
              }
            }
          }
        }
      }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_all(snapshot, call_api, generate_environments):
    query = """
    query {
      allServices {
        totalCount
        edges {
          node {
            allEnvironments {
              totalCount
              edges {
                node {
                  id
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
      }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_first(snapshot, call_api, generate_environments):
    query = """
    query {
      allServices {
        totalCount
        edges {
          node {
            allEnvironments(first: 2) {
              totalCount
              edges {
                node {
                  id
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
      }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_last(snapshot, call_api, generate_environments):
    query = """
    query {
      allServices {
        totalCount
        edges {
          node {
            allEnvironments(last: 2, before: "Mg==") {
              totalCount
              edges {
                node {
                  id
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
      }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)
