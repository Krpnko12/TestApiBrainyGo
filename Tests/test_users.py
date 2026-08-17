import pytest

from API.users_api import UsersAPI

pytestmark = pytest.mark.integration


def test_create_user(created_user, logger):
    logger.info("Проверяем данные созданного пользователя")
    assert created_user["user_id"] > 0
    assert created_user["username"].startswith("user_")
    assert created_user["email"].endswith("@test.com")


def test_get_user(created_user, logger):
    response = UsersAPI().get_user(created_user["user_id"])
    assert response.status_code == 200, response.text

    user = response.json()["user"]
    assert user["id"] == created_user["user_id"]
    assert user["username"] == created_user["username"]
    assert user["email"] == created_user["email"]
    logger.info(f"Найден пользователь id={user['id']}")


def test_get_users(created_user, logger):
    response = UsersAPI().get_users()
    assert response.status_code == 200, response.text

    found_user = next(
        (
            user
            for user in response.json()["users"]
            if user["id"] == created_user["user_id"]
        ),
        None,
    )
    assert found_user is not None, (
        f"Пользователь id={created_user['user_id']} не найден среди всех пользователей"
    )
    assert found_user["username"] == created_user["username"]
    assert found_user["email"] == created_user["email"]
    logger.info(f"Найден пользователь id={found_user['id']}")
