from requests import Session

from api import (
    ClientApi
)


class Backend:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = Session()
        self.client_api = ClientApi(self.session, self.base_url)
