from API.base_api import BaseAPI

class UsersAPI(BaseAPI):

    def create_user(self,user_data: dict):
        return self.post("/create_user", user_data)

    def get_user(self, user_id):
        return self.get(f"/get_user/{user_id}")

    def get_users(self, role=None, name=None):
        return self.get("/get_users")

    def delete_user(self, user_id):
        return self.delete(f"/delete_user/{user_id}")