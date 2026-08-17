from unittest.mock import Mock, call

import pytest
import requests

from API.base_api import BaseAPI
from API.trip_api import TripAPI
from API.users_api import UsersAPI


def test_base_api_requires_base_url():
    with pytest.raises(ValueError, match="BRAINYGO_BASE_URL"):
        BaseAPI(base_url="")


def test_base_api_rejects_invalid_url():
    with pytest.raises(ValueError, match="complete http or https"):
        BaseAPI(base_url="api.example.test")

    with pytest.raises(ValueError, match="complete http or https"):
        BaseAPI(base_url="https://")


def test_base_api_requires_complete_credentials():
    with pytest.raises(ValueError, match="configured together"):
        BaseAPI(base_url="https://api.example.test", username="user", password="")


def test_base_api_requires_https_for_basic_auth():
    with pytest.raises(ValueError, match="HTTPS"):
        BaseAPI(base_url="http://api.example.test", username="user", password="secret")


def test_base_api_builds_request_with_timeout():
    session = Mock(spec=requests.Session)
    api = BaseAPI(base_url="https://api.example.test/", timeout=3.5, session=session)

    api.get("/users", params={"role": "owner"})

    session.request.assert_called_once_with(
        "GET",
        "https://api.example.test/users",
        params={"role": "owner"},
        timeout=3.5,
    )


def test_base_api_supports_all_mutating_methods():
    session = Mock(spec=requests.Session)
    api = BaseAPI(base_url="https://api.example.test", timeout=10, session=session)
    payload = {"value": 42}

    api.post("/resource", payload)
    api.put("/resource/1", payload)
    api.patch("/resource/1", payload)
    api.delete("/resource/1", payload)

    assert session.request.call_args_list == [
        call("POST", "https://api.example.test/resource", json=payload, timeout=10),
        call("PUT", "https://api.example.test/resource/1", json=payload, timeout=10),
        call("PATCH", "https://api.example.test/resource/1", json=payload, timeout=10),
        call("DELETE", "https://api.example.test/resource/1", json=payload, timeout=10),
    ]


def test_base_api_rejects_endpoint_without_leading_slash():
    api = BaseAPI(
        base_url="https://api.example.test", session=Mock(spec=requests.Session)
    )

    with pytest.raises(ValueError, match="must start"):
        api.get("users")


def test_users_api_passes_filters_as_query_parameters():
    session = Mock(spec=requests.Session)
    api = UsersAPI(base_url="https://api.example.test", timeout=10, session=session)

    api.get_users(role="owner", name="Alice")

    session.request.assert_called_once_with(
        "GET",
        "https://api.example.test/get_users",
        params={"role": "owner", "name": "Alice"},
        timeout=10,
    )


def test_trip_cost_uses_patch():
    session = Mock(spec=requests.Session)
    api = TripAPI(base_url="https://api.example.test", timeout=10, session=session)

    api.edit_trip_cost({"trip_id": 7, "cost": 1500})

    session.request.assert_called_once_with(
        "PATCH",
        "https://api.example.test/edit_trip_cost",
        json={"trip_id": 7, "cost": 1500},
        timeout=10,
    )
