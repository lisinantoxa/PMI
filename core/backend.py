from requests import Session

from api import (
    ClientApi, DevicesApi, ProfCleansApi, CheckupApi
)


class Backend:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = Session()
        self.client_api = ClientApi(self.session, self.base_url)
        self.devices_api = DevicesApi(self.session, self.base_url)
        self.prof_cleans_api = ProfCleansApi(self.session, self.base_url)
        self.checkup_api = CheckupApi(self.session, self.base_url)
