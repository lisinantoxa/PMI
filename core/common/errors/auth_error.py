from .base_api_error import BaseApiError


class AuthError(BaseApiError):
    def __init__(self, response):
        super().__init__('Unathorized', response)
