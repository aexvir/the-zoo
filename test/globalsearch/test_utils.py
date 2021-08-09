import pytest

from zoo.services.models import Service
from zoo.utils import model_instance_to_json_object

pytestmark = pytest.mark.django_db


def test_model_instance_serialization():
    service = Service.objects.create(id=123123, owner="zoo", name="jungle")

    expected_result = {
        "model": "services.service",
        "pk": 123123,
        "fields": {
            "owner": "zoo",
            "name": "jungle",
            "description": "",
            "lifecycle": None,
            "impact": None,
            "tier": None,
            "slack_channel": None,
            "sentry_project": None,
            "sonarqube_project": None,
            "rating_grade": None,
            "rating_reason": None,
            "repository": None,
            "pagerduty_service": None,
            "docs_url": None,
            "owner_slug": "zoo",
            "name_slug": "jungle",
            "tags": "[]",
        },
    }

    serialized = model_instance_to_json_object(service)
    assert serialized == expected_result
