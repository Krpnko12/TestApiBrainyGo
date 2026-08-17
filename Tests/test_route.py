import pytest

from API.route_api import RouteAPI

pytestmark = pytest.mark.integration


def test_create_route(created_route, logger):
    logger.info("Проверяем данные созданного маршрута")
    assert created_route["route_id"] > 0
    assert created_route["from_id"] != created_route["to_id"]


def test_get_routes(created_route, logger):
    response = RouteAPI().get_routes()
    assert response.status_code == 200, response.text

    route_id = created_route["route_id"]
    found_route = next(
        (route for route in response.json()["routes"] if route["id"] == route_id),
        None,
    )
    assert found_route is not None, f"Маршрут id={route_id} не найден среди всех"
    assert found_route["from_id"] == created_route["from_id"]
    assert found_route["to_id"] == created_route["to_id"]
    assert found_route["distance"] == pytest.approx(created_route["distance"], abs=0.01)
    logger.info(f"Найден маршрут id={found_route['id']}")
