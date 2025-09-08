from http.client import responses
from Utils.logger import Logger
from API.users_api import UsersAPI


def test_create_user(created_user, logger):
    #Тест просто проверяет, что пользователь создался
    logger.info(f"Тест на создание пользователя запущен.")
    assert "user_id" in created_user
    logger.info(f"Тест на создание пользователя успешно завершён.")


def test_get_user(created_user, logger):
    #Тест получает созданного пользователя
    logger.info(f"Тест на получение созданного пользователя запущен.")
    api = UsersAPI()
    user_id = created_user["user_id"]

    response = api.get_user(user_id)
    assert response.status_code == 200
    if response.status_code != 200:
        logger.error(f"Статус запроса вернул не 200, а: {response.status_code}")
    user_info = response.json()["user"]

    assert user_info["username"] == created_user["username"]
    assert user_info["email"] == created_user["email"]

    logger.info(f"Пользователь найден, id: {created_user['username']}, email: {created_user['email']}")
    logger.info(f"Тест на создание пользователя успешно завершён.")


def test_get_users(created_user, logger):
    #Тест получает всех созданных пользователей
    logger.info(f"Тест на получение всех пользователей и нахождение среди него созданного.")
    api = UsersAPI()
    print(api.get_users)
    response = api.get_users()
    assert response.status_code == 200
    if response.status_code != 200:
        logger.error(f"Статус запроса вернул не 200, а: {response.status_code}")
    users_info = response.json()["users"]
    found_user = None
    for user in users_info:
        if user["id"] == created_user["user_id"]:
            found_user = user
            break
    if found_user is None:
        logger.info(f"Пользователь с user_id: {user['id']}, не найден")

    assert found_user is not None, "Пользователь не найден среди всех пользователей"
    assert found_user["username"] == created_user["username"]
    assert found_user["email"] == created_user["email"]
    logger.info(f"Пользователь с user_id: {user['id']}, найден")
    logger.info(f"Тест на создание пользователя успешно завершён.")
