from API.route_api import RouteAPI

def test_create_route(create_route, logger):
    logger.info("Запущен тест по созданию маршрута")
    assert "route_id" in create_route

from API.route_api import RouteAPI

def test_get_routes(create_route, logger):
    #Тест проверяет, что созданный маршрут есть в списке всех маршрутов
    logger.info("Запущен тест на получение всех маршрутов")

    api = RouteAPI()
    response = api.get_routes()

    assert response.status_code == 200
    routes = response.json()["routes"]

    found_route = None
    for route in routes:
        if route["id"] == create_route["route_id"]:
            found_route = route
            break

    assert found_route is not None, "Созданный маршрут не найден среди всех маршрутов"
    assert found_route["from_id"] == create_route["from_id"]
    assert found_route["to_id"] == create_route["to_id"]
    assert abs(found_route["distance"] - create_route["distance"]) < 0.01  # сравниваем с погрешностью

    logger.info(f"Маршрут найден: id={found_route['id']}, from={found_route['from_id']} → to={found_route['to_id']}")
