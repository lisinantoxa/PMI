import base64
import pytest
from core.helpers import user_session_by_user


def pytest_addoption(parser):
    parser.addoption(
        '--user',
        action='store',
        help='"--user" Указать логин пользователя'
    )
    parser.addoption(
        '--password',
        action='store',
        help='"--password" Указать пароль пользователя'
    )


@pytest.fixture(scope='session')
def base_url():
    return 'https://b2ccrm-uat.myizapps.com'


@pytest.fixture(scope='function')
def config_user_credentials(request):
    password = request.config.getoption(name='--password')
    username = request.config.getoption(name='--user')
    unicode_string = f'{username}:{password}'
    byte = unicode_string.encode('utf-8')
    valid_credentials = base64.b64encode(byte).decode("utf-8")
    headers = {"Authorization": "Basic " + valid_credentials}
    return headers


@pytest.fixture(scope='function')
def auth_session_user(base_url, config_user_credentials):
    user_session = user_session_by_user(base_url=base_url)
    return user_session
