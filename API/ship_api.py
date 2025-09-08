from API.base_api import BaseAPI

class ShipAPI(BaseAPI):
    def add_ship(self, ship_data: dict):
        """Добавить новый корабль"""
        return self.post("/add_ship", ship_data)

    def delete_ship(self, ship_id: int):
        """Удалить корабль"""
        return self.delete(f"/delete_ship/{ship_id}")

    def add_ship_type(self, type_data: dict):
        """Добавить новый тип корабля"""
        return self.post("/add_ship_type", type_data)

    def delete_ship_type(self, ship_type_id: int):
        """Удалить тип корабля"""
        return self.delete(f"/delete_ship_type/{ship_type_id}")

    def get_ship_types(self):
        """Получить все типы кораблей"""
        return self.get("/get_ship_types")

    def get_ships(self, corporation_id: int):
        """Получить корабли по корпорации"""
        return self.get(f"/get_ships/{corporation_id}")