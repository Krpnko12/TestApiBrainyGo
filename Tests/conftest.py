import secrets
from datetime import date, timedelta
from uuid import uuid4

import pytest

from API.corporation_api import CorporationAPI
from API.destination_api import DestinationAPI
from API.route_api import RouteAPI
from API.ship_api import ShipAPI
from API.trip_api import TripAPI
from API.users_api import UsersAPI
from Utils import config
from Utils.logger import Logger

SUCCESSFUL_DELETE_CODES = {200, 204}


def pytest_collection_modifyitems(items):
    """Skip live API tests when the service URL is not configured."""
    if config.BASE_URL:
        return

    skip_live_api = pytest.mark.skip(
        reason="Set BRAINYGO_BASE_URL to run integration tests against the live API."
    )
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_live_api)


def _assert_status(response, expected_status: int, action: str) -> None:
    assert response.status_code == expected_status, (
        f"{action}: expected HTTP {expected_status}, got {response.status_code}. "
        f"Response: {response.text[:500]}"
    )


def _cleanup(logger: Logger, resource_name: str, delete_call) -> None:
    response = delete_call()
    assert response.status_code in SUCCESSFUL_DELETE_CODES, (
        f"Не удалось удалить ресурс {resource_name}: "
        f"HTTP {response.status_code}, {response.text[:300]}"
    )
    logger.info(f"Удалён ресурс {resource_name}")


@pytest.fixture
def logger(request):
    test_logger = Logger(request.node.name)
    yield test_logger
    test_logger.close()


@pytest.fixture
def created_user(logger, request):
    api = UsersAPI()
    unique_id = uuid4().hex[:8]
    user_data = {
        "avatar_url": "https://brainy.run/wp-content/uploads/2024/05/candidate2.png",
        "email": f"user_{unique_id}@test.com",
        "name": "Тестовый Пользователь",
        "password": secrets.token_urlsafe(32),
        "role": "owner",
        "username": f"user_{unique_id}",
    }

    response = api.create_user(user_data)
    _assert_status(response, 201, "Создание пользователя")
    user_id = response.json()["user_id"]
    request.addfinalizer(
        lambda: _cleanup(logger, f"user {user_id}", lambda: api.delete_user(user_id))
    )

    logger.info(f"Создан пользователь {user_data['username']} с id={user_id}")
    return {
        "user_id": user_id,
        "username": user_data["username"],
        "email": user_data["email"],
    }


@pytest.fixture
def created_corporation(logger, request, created_user):
    api = CorporationAPI()
    corporation_data = {
        "description": "Корпорация для автоматизированного API-теста",
        "logo_url": "https://brainy.run/wp-content/uploads/2025/01/robbie.jpg",
        "name": f"Test Corporation {uuid4().hex[:8]}",
        "owner_id": created_user["user_id"],
    }

    response = api.create_corporation(corporation_data)
    _assert_status(response, 201, "Создание корпорации")
    response_data = response.json()
    corporation_id = response_data["corporation_id"]
    request.addfinalizer(
        lambda: _cleanup(
            logger,
            f"corporation {corporation_id}",
            lambda: api.delete_corporation(corporation_id),
        )
    )

    logger.info(f"Создана корпорация id={corporation_id}")
    return {
        "corporation_id": corporation_id,
        "message": response_data.get("message", ""),
    }


@pytest.fixture
def created_destination(logger, request):
    api = DestinationAPI()
    response = api.add_destination({"name": f"Test City {uuid4().hex[:8]}"})
    _assert_status(response, 201, "Создание пункта назначения")
    destination_id = response.json()["destination_id"]
    request.addfinalizer(
        lambda: _cleanup(
            logger,
            f"destination {destination_id}",
            lambda: api.delete_destination(destination_id),
        )
    )

    logger.info(f"Создан пункт назначения id={destination_id}")
    return {"destination_id": destination_id}


@pytest.fixture
def created_route(logger, request):
    destination_api = DestinationAPI()
    destination_ids = []

    for label in ("From", "To"):
        response = destination_api.add_destination(
            {"name": f"Test {label} City {uuid4().hex[:8]}"}
        )
        _assert_status(response, 201, f"Создание пункта {label}")
        destination_id = response.json()["destination_id"]
        destination_ids.append(destination_id)
        request.addfinalizer(
            lambda destination_id=destination_id: _cleanup(
                logger,
                f"destination {destination_id}",
                lambda: destination_api.delete_destination(destination_id),
            )
        )

    route_api = RouteAPI()
    route_data = {
        "distance": 750.5,
        "from_id": destination_ids[0],
        "to_id": destination_ids[1],
    }
    response = route_api.create_route(route_data)
    _assert_status(response, 201, "Создание маршрута")
    route_id = response.json()["route_id"]
    request.addfinalizer(
        lambda: _cleanup(
            logger, f"route {route_id}", lambda: route_api.delete_route(route_id)
        )
    )

    logger.info(f"Создан маршрут id={route_id}")
    return {"route_id": route_id, **route_data}


@pytest.fixture
def created_trip(logger, request, created_route, created_corporation):
    ship_api = ShipAPI()
    ship_types_response = ship_api.get_ship_types()
    _assert_status(ship_types_response, 200, "Получение типов кораблей")
    ship_types = ship_types_response.json().get("ship_types", [])
    assert ship_types, "API не вернул ни одного типа корабля"

    ship_data = {
        "corporation_id": created_corporation["corporation_id"],
        "custom_photo_url": "https://example.com/enterprise.jpg",
        "description": "Корабль для автоматизированного API-теста",
        "name": f"Test Ship {uuid4().hex[:8]}",
        "type_id": ship_types[0]["id"],
    }
    ship_response = ship_api.add_ship(ship_data)
    _assert_status(ship_response, 201, "Создание корабля")
    ship_id = ship_response.json()["ship_id"]
    request.addfinalizer(
        lambda: _cleanup(
            logger, f"ship {ship_id}", lambda: ship_api.delete_ship(ship_id)
        )
    )

    trip_api = TripAPI()
    trip_data = {
        "date": (date.today() + timedelta(days=365)).isoformat(),
        "route_id": created_route["route_id"],
        "ship_id": ship_id,
    }
    response = trip_api.add_trip(trip_data)
    _assert_status(response, 201, "Создание рейса")
    trip_id = response.json()["trip_id"]
    request.addfinalizer(
        lambda: _cleanup(
            logger, f"trip {trip_id}", lambda: trip_api.delete_trip(trip_id)
        )
    )

    logger.info(f"Создан рейс id={trip_id}")
    return {
        "trip_id": trip_id,
        "route_id": created_route["route_id"],
        "ship_id": ship_id,
        "corporation_id": created_corporation["corporation_id"],
    }
