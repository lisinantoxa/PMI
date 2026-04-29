import logging
import allure
from requests import Session, Response

from .errors import (AccessError, AuthError, BadRequestError, BaseApiError, NotFoundError, ServerError,
                     UnprocessableEntityError)
from .tools.curlify import to_curl


class BaseApi:
    def __init__(self, session: Session, base_url):
        self.session = session
        self.base_url = base_url
        self.log = logging.getLogger(__name__)

    def get(self, url, external=False, **kwargs):
        callback = self.session.get
        return self._send(url, callback, 'GET', verify=False, external=external, **kwargs)

    def post(self, url, external=False, **kwargs):
        callback = self.session.post
        return self._send(url, callback, 'POST', verify=False, external=external, **kwargs)

    def put(self, url, external=False, **kwargs):
        callback = self.session.put
        return self._send(url, callback, 'PUT', verify=False, external=external, **kwargs)

    def patch(self, url, external=False, **kwargs):
        callback = self.session.patch
        return self._send(url, callback, 'PATCH', verify=False, external=external, **kwargs)

    def delete(self, url, external=False, **kwargs):
        callback = self.session.delete
        return self._send(url, callback, 'DELETE', verify=False, external=external, **kwargs)

    def assert_response(self, current_response, expected_response):
        assert current_response[
                   'code'] == expected_response, f'Ожидаемый код {expected_response} не совпадает с текущим {current_response["code"]}'

    def compare_response_json_with_schema(self, response, schema):
        result = set(response) - set(schema)
        assert len(result) == 0, f'В response_schema нет ключей response: {result}'
        result = set(schema) - set(response)
        assert len(result) == 0, f'В response нет ключей response_schema: {result}'

    def assert_error(self, current_error, expected_error):
        assert current_error == expected_error, f'Ожидаемая ошибка {expected_error} не совпадает с текущей {current_error}'

    def assert_field_value(self, current_value, expected_value):
        assert current_value == expected_value, f'Ожидаемое поле {expected_value} не совпадает с текущим значением {current_value}'

    def assert_response_data(self, data, response, get_response):
        for value in data:
            assert response['result']['result'][value] == get_response['result']['result'][value]

    def _log_request_data(self, url, method, **kwargs):
        request_message = f'{method} {self._path(url)}'
        if method == 'GET' and 'params' in kwargs:
            request_message += f'?{kwargs["params"]}'
        headers = {**self.session.headers, **kwargs.get('headers')} if kwargs.get('headers') else self.session.headers
        request_message += f'\nHeaders: {headers}'
        request_message += f'\nCookies: {self.session.cookies.get_dict()}'
        allure.attach(request_message.replace('\n', '\n\n'), 'Request', allure.attachment_type.TEXT)
        if kwargs.get('json'):
            request_message += f'\nBody: {kwargs.get("json")}'
        if kwargs.get('data'):
            request_message += f'\nData: {kwargs.get("data")}'
        if kwargs.get('files'):
            # single file uploading
            if isinstance(kwargs.get('files'), dict):
                self.file_ = kwargs.get("files")["file"]
                request_message += f'\nFiles: {self.file_[0]}'
            # multiple files uploading
            elif isinstance(kwargs.get('files'), list):
                request_message += f'\nFiles: {[f[1][0] for f in kwargs.get("files")]}'
        self.log.info(request_message)

    def _log_response_data(self, response: Response, skip_body: bool):
        response_message = f'Response status: {response.status_code}, elapsed: {response.elapsed.seconds}s'
        response_message += f'\nResponse headers: {response.headers}'
        if skip_body:
            response_message += 'Response body was skipped'
            allure.attach('Response body was skipped', allure.attachment_type.TEXT)
        elif response.text != '':
            response_message += f'\nResponse body: {self._decode(response.text)}'
            allure.attach(response.text, 'Response', allure.attachment_type.JSON)
        self.log.info(response_message)

    def _send(self, url, callback, method, external=False, **kwargs):
        # Need to pop this parameter before callback
        skip_body = kwargs.pop('skip_body', False)
        self._log_request_data(url, method, **kwargs)
        response = callback(self._path(url), **kwargs)
        self._log_response_data(response, skip_body)
        try:
            curl = to_curl(response.request)
            self.log.info(f'curl: {curl}')  # noqa: E800
            allure.attach(curl, 'curl')
        except UnicodeDecodeError:  # curlify can fall when decoding request body
            self.log.info('Cannot curlify request :(')

        if external:
            return response
        else:
            self._raise_for_status(response)
            try:
                return response.json()
            except ValueError:
                return response.text

    def _decode(self, text):
        return (text.encode('utf-8')).decode('utf-8')

    def _path(self, url):
        return f'{self.base_url}{url}'

    def _raise_for_status(self, response):
        if 400 <= response.status_code < 500:
            if response.status_code == 400:
                raise BadRequestError(response)
            elif response.status_code == 401:
                raise AuthError(response)
            elif response.status_code == 403:
                raise AccessError(response)
            elif response.status_code in [404, 410]:
                raise NotFoundError(response)
            elif response.status_code == 422:
                raise UnprocessableEntityError(response)
            else:
                raise BaseApiError('Client', response)
        elif 500 <= response.status_code < 600:
            raise ServerError(response)
