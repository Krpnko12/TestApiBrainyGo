from API.base_api import BaseAPI

class CorporationAPI(BaseAPI):

    def create_corporation(self, corporation_data: dict):
        return self.post("/create_corporation", corporation_data)

    def delete_corporation(self, corporation_id):
        return self.delete(f"/delete_corporation/{corporation_id}")

    def get_corporations(self):
        return self.get(f"/get_corporations")