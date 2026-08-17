import pytest

from API.destination_api import DestinationAPI

pytestmark = pytest.mark.integration


def test_add_destination(created_destination, logger):
    logger.info("Проверяем данные созданного пункта назначения")
    assert created_destination["destination_id"] > 0


def test_get_destinations(created_destination, logger):
    response = DestinationAPI().get_destinations()
    assert response.status_code == 200, response.text

    destination_id = created_destination["destination_id"]
    found_destination = next(
        (
            destination
            for destination in response.json()["destinations"]
            if destination["id"] == destination_id
        ),
        None,
    )
    assert found_destination is not None, (
        f"Пункт назначения id={destination_id} не найден среди всех"
    )
    logger.info(
        f"Найден пункт назначения id={found_destination['id']}, "
        f"name={found_destination['name']}"
    )
