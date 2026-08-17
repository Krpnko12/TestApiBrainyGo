import pytest

from API.corporation_api import CorporationAPI

pytestmark = pytest.mark.integration


def test_create_corporation(created_corporation, logger):
    logger.info("Проверяем данные созданной корпорации")
    assert created_corporation["corporation_id"] > 0
    assert created_corporation["message"]


def test_get_corporations(created_corporation, logger):
    response = CorporationAPI().get_corporations()
    assert response.status_code == 200, response.text

    corporation_id = created_corporation["corporation_id"]
    found_corporation = next(
        (
            corporation
            for corporation in response.json()["corporations"]
            if corporation["id"] == corporation_id
        ),
        None,
    )
    assert found_corporation is not None, (
        f"Корпорация id={corporation_id} не найдена среди всех корпораций"
    )
    logger.info(f"Найдена корпорация id={found_corporation['id']}")
