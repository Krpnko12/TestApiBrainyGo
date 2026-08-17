import pytest

from API.trip_api import TripAPI

pytestmark = pytest.mark.integration


def test_create_trip(created_trip, logger):
    logger.info("Проверяем данные созданного рейса")
    assert created_trip["trip_id"] > 0
    assert created_trip["ship_id"] > 0
    assert created_trip["route_id"] > 0


def test_get_trips(created_trip, created_corporation, logger):
    response = TripAPI().get_trips(created_corporation["corporation_id"])
    assert response.status_code == 200, response.text

    trip_id = created_trip["trip_id"]
    found_trip = next(
        (trip for trip in response.json()["trips"] if trip["id"] == trip_id),
        None,
    )
    assert found_trip is not None, (
        f"Рейс id={trip_id} не найден среди рейсов корпорации"
    )
    assert found_trip["ship_id"] == created_trip["ship_id"]
    assert found_trip["route_id"] == created_trip["route_id"]
    logger.info(f"Найден рейс id={found_trip['id']}")
