import logging

import allure
from requests import Response, Session

from .errors import (
    AccessError, AuthError, BadRequestError, BaseApiError,
    NotFoundError, ServerError, UnprocessableEntityError,
)
from .tools.curlify import to_curl


class BaseApi:
    def __init__(self, session: Session, base_url: str, *, verify: bool = True):
        self.session = session
        self.base_url = base_url
        self.verify = verify
        self.log = logging.getLogger(__name__)

    # ── HTTP-методы ────────────────────────────────────────────

    def get(self, url, **kwargs):
        return self._send(url, self.session.get, 'GET', **kwargs)

    def post(self, url, **kwargs):
        return self._send(url, self.session.post, 'POST', **kwargs)

    def put(self, url, **kwargs):
        return self._send(url, self.session.put, 'PUT', **kwargs)

    def patch(self, url, **kwargs):
        return self._send(url, self.session.patch, 'PATCH', **kwargs)

    def delete(self, url, **kwargs):
        return self._send(url, self.session.delete, 'DELETE', **kwargs)

    # ── Универсальный обработчик ответа ─────────────────────────

    def _request_result(self, response: Response) -> dict:
        try:
            result = response.json()
        except ValueError:
            result = response.text
        return {'code': response.status_code, 'result': result}

    # ── Assertions ─────────────────────────────────────────────

    def assert_response(self, current_response, expected_response):
        assert current_response['code'] == expected_response, (
            f'Ожидаемый код {expected_response} не совпадает '
            f'с текущим {current_response["code"]}'
        )

    def assert_error(self, current_error, expected_error):
        assert current_error == expected_error, (
            f'Ожидаемая ошибка {expected_error} не совпадает '
            f'с текущей {current_error}'
        )

    def assert_field_value(self, current_value, expected_value):
        assert current_value == expected_value, (
            f'Ожидаемое поле {expected_value} не совпадает '
            f'с текущим значением {current_value}'
        )

    @staticmethod
    def assert_request_closed(response, inbound_problem, resolve_reason):
        request = response['result']['Request']
        assert request['Status'] == 'Closed', (
            f"Ожидался статус запроса Closed, получен {request['Status']}"
        )
        assert request['InboundProblem']['Name'] == inbound_problem, (
            f"Ожидался InboundProblem {inbound_problem}, "
            f"получен {request['InboundProblem']}"
        )
        assert request['ResolveReason']['Name'] == resolve_reason, (
            f"Ожидался ResolveReason {resolve_reason}, "
            f"получен {request['ResolveReason']}"
        )

    @staticmethod
    def assert_request_inprogress(response, inbound_problem, picked_solution):
        request = response['result']['Request']
        assert request['Status'] == 'InProgress', (
            f"Ожидался статус запроса Closed, получен {request['Status']}"
        )
        assert request['InboundProblem']['Name'] == inbound_problem, (
            f"Ожидался InboundProblem {inbound_problem}, "
            f"получен {request['InboundProblem']}"
        )
        assert request['PickedSolution']['Name'] == picked_solution, (
            f"Ожидался ResolveReason {picked_solution}, "
            f"получен {request['ResolveReason']}"
        )

    # ── Внутренние методы ──────────────────────────────────────

    def _send(self, url, callback, method, *, raise_on_error: bool = False, **kwargs):
        skip_body = kwargs.pop('skip_body', False)
        self._log_request_data(url, method, **kwargs)
        response = callback(self._path(url), verify=self.verify, **kwargs)
        self._log_response_data(response, skip_body)
        self._attach_curl(response)

        if raise_on_error:
            self._raise_for_status(response)

        return response

    def _attach_curl(self, response):
        try:
            curl = to_curl(response.request)
            self.log.info(f'curl: {curl}')
            allure.attach(curl, 'curl')
        except UnicodeDecodeError:
            self.log.info('Cannot curlify request :(')

    def _log_request_data(self, url, method, **kwargs):
        request_message = f'{method} {self._path(url)}'
        if method == 'GET' and 'params' in kwargs:
            request_message += f'?{kwargs["params"]}'
        headers = (
            {**self.session.headers, **kwargs.get('headers')}
            if kwargs.get('headers')
            else self.session.headers
        )
        request_message += f'\nHeaders: {headers}'
        request_message += f'\nCookies: {self.session.cookies.get_dict()}'
        allure.attach(request_message.replace('\n', '\n\n'), 'Request',
                      allure.attachment_type.TEXT)
        if kwargs.get('json'):
            request_message += f'\nBody: {kwargs.get("json")}'
        if kwargs.get('data'):
            request_message += f'\nData: {kwargs.get("data")}'
        if kwargs.get('files'):
            if isinstance(kwargs.get('files'), dict):
                self.file_ = kwargs.get("files")["file"]
                request_message += f'\nFiles: {self.file_[0]}'
            elif isinstance(kwargs.get('files'), list):
                request_message += f'\nFiles: {[f[1][0] for f in kwargs.get("files")]}'
        self.log.info(request_message)

    def _log_response_data(self, response: Response, skip_body: bool):
        response_message = (
            f'Response status: {response.status_code}, '
            f'elapsed: {response.elapsed.seconds}s'
        )
        response_message += f'\nResponse headers: {response.headers}'
        if skip_body:
            response_message += 'Response body was skipped'
            allure.attach('Response body was skipped', allure.attachment_type.TEXT)
        elif response.text != '':
            response_message += f'\nResponse body: {response.text}'
            allure.attach(response.text, 'Response', allure.attachment_type.JSON)
        self.log.info(response_message)

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
            elif response.status_code in (404, 410):
                raise NotFoundError(response)
            elif response.status_code == 422:
                raise UnprocessableEntityError(response)
            else:
                raise BaseApiError('Client', response)
        elif 500 <= response.status_code < 600:
            raise ServerError(response)
