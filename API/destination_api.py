from API.base_api import BaseAPI


class DestinationAPI(BaseAPI):
    def add_destination(self, destination_data: dict):
        return self.post("/add_destination", destination_data)

    def delete_destination(self, destination_id):
        return self.delete(f"/delete_destination/{destination_id}")

    def get_destinations(self):
        return self.get("/get_destinations")
