from API.base_api import BaseAPI

class RouteAPI(BaseAPI):

    def create_route(self, route_data):
        return self.post("/create_route", route_data)

    def get_routes(self):
        return self.get("/get_routes")

    def delete_route(self, route_id):
        return self.delete(f"/delete_route/{route_id}")

