from requests import Session
from typing import Union
from api import ClientApi, DevicesApi, ProfCleansApi, CheckupApi


class Backend:
    def __init__(self, base_url: str, auth_headers: Union[dict, None] = None, *, verify: bool = True):
        self.base_url = base_url
        self.session = Session()
        if auth_headers:
            self.session.headers.update(auth_headers)
        self.client_api = ClientApi(self.session, self.base_url, verify=verify)
        self.devices_api = DevicesApi(self.session, self.base_url, verify=verify)
        self.prof_cleans_api = ProfCleansApi(self.session, self.base_url, verify=verify)
        self.checkup_api = CheckupApi(self.session, self.base_url, verify=verify)
