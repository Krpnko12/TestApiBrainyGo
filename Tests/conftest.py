import re
from datetime import datetime, timedelta
import pytest
from Utils.logger import Logger
from API.users_api import UsersAPI
from API.corporation_api import CorporationAPI
from API.destination_api import DestinationAPI
from API.route_api import RouteAPI
import string
import random
from Utils.logger import Logger
from API.trip_api import TripAPI
from API.route_api import RouteAPI
from API.ship_api import ShipAPI


def get_random_city():
    cities = ["Minsk", "Moscow", "Berlin", "Warsaw", "Paris", "London"]
    return random.choice(cities)

def generate_random_email():
    #Генерация уникального email
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"user_{suffix}@test.com"

@pytest.fixture
def logger(request):
    test_name = request.node.name
    return Logger(test_name)

@pytest.fixture
def created_user(logger):
    #Фикстура для создания нового пользователя
    logger.info("Запущена фикстура по созданию пользователя")
    api = UsersAPI()

    random_username = "user_" + ''.join(random.choices(string.ascii_lowercase, k=4))
    random_email = generate_random_email()

    user_data = {
        "avatar_url": "https://brainy.run/wp-content/uploads/2024/05/candidate2.png",
        "email": random_email,
        "name": "Тестовый Пользователь",
        "password": "testPassword123",
        "role": "owner",
        "username": random_username
    }

    response = api.create_user(user_data)
    assert response.status_code == 201
    logger.info(f"Запрос вернул статус код:{response.status_code}")
    if response.status_code != 201:
        logger.error(f"Статус запроса вернул не 201, а: {response.status_code}")
    logger.info(f"Пользователь создан name: {random_username}, email: {random_email} ")
    created_user_info = {
        "user_id": response.json()["user_id"],
        "username": random_username,
        "email": random_email
    }

    yield created_user_info
    logger.info("Запущено постусловие по удалению пользователя")
    # После выполнения теста — удалить пользователя
    try:
        delete_response = api.delete_user(created_user_info["user_id"])
        if delete_response.status_code != 200:
            logger.warning(f"Пользователь {created_user_info['user_id']} не был удалён корректно. Код: {delete_response.status_code}")
        if delete_response.status_code == 200:
            logger.info(f"Пользователь успешно удалён: {delete_response.status_code}")
    except Exception as e:
        logger.warning(f"Ошибка при удалении пользователя {created_user_info['user_id']}: {str(e)}")


@pytest.fixture
def created_corporation(logger, created_user):
    #Фикстура по созданию корпорации
    logger.info("Запущена фикстура по созданию корпорации")
    api = CorporationAPI()

    corporation_data = {
            "description": "Ешь свои фрукты, Спортакус. Мы уже победили!",
            "logo_url": "https://brainy.run/wp-content/uploads/2025/01/robbie.jpg",
            "name": "RobbiZlo Inc.",
            "owner_id": created_user["user_id"]
        }

    response = api.create_corporation(corporation_data)
    assert response.status_code == 201

    logger.info(f"Запрос вернул статус код:{response.status_code}")
    if response.status_code != 201:
        logger.error(f"Статус запроса вернул не 201, а: {response.status_code}")



    created_corporation_info = {
        "corporation_id": response.json()["corporation_id"],
        "message": response.json()["message"],
    }
    logger.info(f"Корпорация создана с id: {created_corporation_info['corporation_id']}")

    yield created_corporation_info
    logger.info("Запущенно постусловие по удалению корпрорации")

    try:
        delete_response = api.delete_corporation(response.json()["corporation_id"])
        if delete_response.status_code != 200:
            logger.error(f"Корпорация не была удалена успешно: {delete_response.status_code}")
        if delete_response.status_code == 200:
            logger.info(f"Корпорация была удалена успешно: {delete_response.status_code}")

    except Exception as e:
        logger.warning(f"Ошибка при удалении корпорации {response.json('corporation_id')}: {str(e)}")


@pytest.fixture
def add_destination(logger):
    #Фикстура для создания направления
    logger.info("Запущена фикстура по созданию направления")
    api = DestinationAPI()
    destination_data = {
        "name": get_random_city()
    }
    response = api.add_destination(destination_data)
    assert response.status_code == 201

    logger.info(f"Запрос вернул статус код:{response.status_code}")
    if response.status_code != 201:
        logger.error(f"Статус запроса вернул не 201, а: {response.status_code}")

    created_destination_info = {
        "destination_id": response.json()["destination_id"]
    }
    logger.info(f"Id Пункта назначения : {created_destination_info['destination_id']}")

    yield created_destination_info
    logger.info("Запущенно постусловие по удалению пункта назначения")

    try:
        delete_response = api.delete_destination(response.json()["destination_id"])
        if delete_response.status_code != 200:
            logger.error(f"Пункт назначения не был удалён: {delete_response.status_code}")
        if delete_response.status_code == 200:
            logger.info(f"Пункт назначения был удалён: {delete_response.status_code}")

    except Exception as e:
        logger.warning(f"Ошибка при удалении пункта назначения {response.json('corporation_id')}: {str(e)}")


@pytest.fixture
def create_route(logger):
    #Фикстура к созданию маршрута
    logger.info("Запущена фикстура по созданию маршрута")

    # 1. Создаём два пункта назначения
    dest_api = DestinationAPI()

    # первый пункт
    dest1 = {
        "name": get_random_city()
    }

    response1 = dest_api.add_destination(dest1)
    assert response1.status_code == 201
    from_id = response1.json()["destination_id"]
    logger.info(f"Создан пункт назначения (from_id): {from_id}")

    # второй пункт
    dest2 = {
        "name": get_random_city()
    }
    response2 = dest_api.add_destination(dest2)
    assert response2.status_code == 201
    to_id = response2.json()["destination_id"]
    logger.info(f"Создан пункт назначения (to_id): {to_id}")

    # 2. Создаём маршрут
    api = RouteAPI()
    route_data = {
        "distance": round(random.uniform(100, 1000), 1),  # случайная дистанция
        "from_id": from_id,
        "to_id": to_id
    }
    response_route = api.create_route(route_data)
    assert response_route.status_code == 201
    logger.info(f"Запрос на создание маршрута, отдал код: {response_route.status_code}")

    route_info = {
        "route_id": response_route.json()["route_id"],
        "from_id": from_id,
        "to_id": to_id,
        "distance": route_data["distance"]
    }

    logger.info(f"Инфа по маршруту: {route_info}")
    logger.info(f"Маршрут создан с id: {route_info['route_id']}")

    # 3. Возвращаем данные маршрута в тест
    yield route_info

    # 4. Постусловие — удаление маршрута и пунктов назначения
    try:
        delete_response = api.delete_route(route_info["route_id"])
        if delete_response.status_code == 200:
            logger.info(f"Маршрут {route_info['route_id']} успешно удалён")
        else:
            logger.warning(f"Маршрут {route_info['route_id']} не удалён. Код: {delete_response.status_code}")
    except Exception as e:
        logger.error(f"Ошибка при удалении маршрута {route_info['route_id']}: {str(e)}")

    try:
        dest_api.delete_destination(from_id)
        dest_api.delete_destination(to_id)
        logger.info(f"Пункты назначения {from_id}, {to_id} удалены")
    except Exception as e:
        logger.warning(f"Ошибка при удалении пунктов назначения {from_id}, {to_id}: {str(e)}")



@pytest.fixture
def create_trip(logger, create_route, created_corporation):
    trip_api = TripAPI()
    ship_api = ShipAPI()

    ship_name = "Ship" + ''.join(random.choices(string.ascii_letters, k=5))
    ship_data = {
        "corporation_id": created_corporation["corporation_id"],
        "custom_photo_url": "http://example.com/enterprise.jpg",
        "description": "Тестовый корабль",
        "name": ship_name,
        "type_id": 1
    }
    ship_response = ship_api.add_ship(ship_data)
    logger.info(f"Создан корабль {ship_response.json()}, код {ship_response.status_code}")
    assert ship_response.status_code == 201, f"Ошибка создания корабля: {ship_response.text}"
    ship_id = ship_response.json()["ship_id"]

    test_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    test_trip = {
        "date": test_date,
        "route_id": create_route["route_id"],
        "ship_id": ship_id
    }
    response = trip_api.add_trip(test_trip)

    if response.status_code == 400:
        msg = response.json().get("message", "")
        match = re.search(r"\d{4}", msg)
        if match:
            server_year = int(match.group())
            # используем год сервера + 1, чтобы гарантированно будущее
            future_date = datetime(server_year + 1, 1, 1).strftime("%Y-%m-%d")
            logger.info(f"Определили серверный год: {server_year}, пробуем с датой {future_date}")

            trip_data = {
                "date": future_date,
                "route_id": create_route["route_id"],
                "ship_id": ship_id
            }
            response = trip_api.add_trip(trip_data)

    assert response.status_code == 201, f"Ошибка создания рейса: {response.text}"
    trip_id = response.json()["trip_id"]
    logger.info(f"Рейс создан с id: {trip_id}")

    yield {
        "trip_id": trip_id,
        "route_id": create_route["route_id"],
        "ship_id": ship_id,
        "corporation_id": created_corporation["corporation_id"]
    }

    try:
        trip_api.delete_trip(trip_id)
        logger.info(f"Рейс {trip_id} удалён")
    except Exception as e:
        logger.warning(f"Ошибка при удалении рейса {trip_id}: {e}")

    try:
        ship_api.delete_ship(ship_id)
        logger.info(f"Корабль {ship_id} удалён")
    except Exception as e:
        logger.warning(f"Ошибка при удалении корабля {ship_id}: {e}")