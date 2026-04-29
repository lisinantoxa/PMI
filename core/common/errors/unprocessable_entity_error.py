from .base_api_error import BaseApiError


class UnprocessableEntityError(BaseApiError):
    def __init__(self, response):
        super().__init__('Unprocessable Entity', response)
