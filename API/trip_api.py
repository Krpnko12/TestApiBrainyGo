from API.base_api import BaseAPI


class TripAPI(BaseAPI):
    def add_trip(self, trip_data: dict):
        """Добавить новый рейс"""
        return self.post("/add_trip", trip_data)

    def delete_trip(self, trip_id: int):
        """Удалить рейс"""
        return self.delete(f"/delete_trip/{trip_id}")

    def edit_trip_cost(self, cost_data: dict):
        """Изменить стоимость рейса"""
        return self.patch("/edit_trip_cost", cost_data)

    def get_trips(self, corporation_id: int):
        """Получить рейсы по корпорации"""
        return self.get(f"/get_trips/{corporation_id}")
