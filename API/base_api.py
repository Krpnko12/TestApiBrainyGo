import requests
from requests.auth import HTTPBasicAuth
from Utils import config

class BaseAPI:
    def __init__(self):
        self.base_url = config.BASE_URL
        self.auth = HTTPBasicAuth(config.USERNAME, config.PASSWORD)

    def get(self, enpoint, params=None):
        url = self.base_url + enpoint
        return requests.get(url, auth=self.auth, params=params)

    def post(self, enpoint, params=None):
        url = self.base_url + enpoint
        return requests.post(url, auth=self.auth, json=params)

    def put(self, enpoint, params=None):
        url = self.base_url + enpoint
        return requests.put(url, auth=self.auth, json=params)

    def delete(self, enpoint, params=None):
        url = self.base_url + enpoint
        return requests.delete(url, auth=self.auth, json=params)

