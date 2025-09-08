from API.trip_api import TripAPI

def test_create_trip(create_trip, logger):
    logger.info("Тест на создание рейса запущен")
    assert "trip_id" in create_trip
    assert "ship_id" in create_trip
    assert "route_id" in create_trip
    logger.info(f"Рейс создан: {create_trip}")

def test_get_trips(create_trip, created_corporation, logger):
    logger.info("Тест на получение рейсов корпорации запущен")
    api = TripAPI()
    response = api.get_trips(created_corporation["corporation_id"])
    assert response.status_code == 200
    trips = response.json()["trips"]

    found = None
    for trip in trips:
        if trip["id"] == create_trip["trip_id"]:
            found = trip
            break

    assert found is not None, "Рейс не найден среди рейсов корпорации"
    logger.info(f"Рейс найден: {found}")