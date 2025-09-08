from API.destination_api import DestinationAPI


def test_add_destination(add_destination, logger):
    logger.info("Запущен тест по созданию пункта назначения")
    assert add_destination["destination_id"] > 0

def test_get_destinations(add_destination, logger):
    """Тест проверяет, что созданный пункт назначения есть среди всех"""
    logger.info("Запущен тест на получение всех пунктов назначения")
    api = DestinationAPI()

    # Делаем запрос на список всех направлений
    response = api.get_destinations()
    assert response.status_code == 200, f"Статус код не 200, а {response.status_code}"

    destinations_info = response.json()["destinations"]

    # Ищем наш пункт назначения по id
    found_destination = None
    for destination in destinations_info:
        if destination["id"] == add_destination["destination_id"]:
            found_destination = destination
            break

    if found_destination is None:
        logger.error(
            f"Пункт назначения с id={add_destination['destination_id']} не найден"
        )
    else:
        logger.info(
            f"Пункт назначения найден: id={found_destination['id']}, name={found_destination['name']}"
        )

    # Проверка что пункт назначения найден
    assert found_destination is not None, "Пункт назначения не найден среди всех"