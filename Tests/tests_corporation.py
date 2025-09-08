from http.client import responses
from urllib import response

from Utils.logger import Logger
from API.users_api import UsersAPI
from API.corporation_api import  CorporationAPI

def test_create_corporation(created_corporation, logger):
    logger.info("Запущен тест по созданию корпорации")
    assert "Корпорация успешно создана" in created_corporation["message"]

def test_get_corporations(created_corporation, logger):
    logger.info("Запущен тест по получению всех корпораций")
    api = CorporationAPI()
    response = api.get_corporations()
    assert response.status_code == 200
    if response.status_code != 200:
        logger.error(f"Статус запроса вернул не 200, а: {response.status_code}")
    corporation_info = response.json()["corporations"]
    found_corporation = None
    for corporation in corporation_info:
        if corporation["id"] == created_corporation["corporation_id"]:
            found_corporation = corporation
            break
    if found_corporation is None:
        logger.info(f"Корпорация с id: {corporation['id']} не найден")

    assert found_corporation is not None, f"Корпорация не найдена среди всех корпораций"
    assert found_corporation["id"] == created_corporation["corporation_id"]
    logger.info(f"Корпорация с id: {found_corporation['id']} найдена")
    logger.info("Тест на получение корпорации завершён")


