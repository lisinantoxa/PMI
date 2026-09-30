import base64
import os

import pytest
from datetime import datetime

from core.helpers import user_session_by_user
from resources.data.regression_data import (
    get_device_create_json, get_link_data, get_linking_date_data,
    get_case_create_json,
)


def pytest_addoption(parser):
    parser.addoption('--crm_user', action='store', help='Логин пользователя CRM')
    parser.addoption('--password', action='store', help='Пароль пользователя CRM')
    parser.addoption('--consumer', action='store', help='Код тестового клиента')
    parser.addoption(
        '--base_url',
        action='store',
        default=os.environ.get('BASE_URL', 'https://b2ccrm-preprod.myizapps.com'),
        help='Base URL тестируемого окружения',
    )


@pytest.fixture(scope='session')
def base_url(request):
    return request.config.getoption('--base_url')


@pytest.fixture(scope='session')
def config_user_credentials(request):
    """Basic-auth заголовок — устанавливается один раз на сессию."""
    password = request.config.getoption('--password')
    username = request.config.getoption('--crm_user')
    if not username or not password:
        pytest.fail('--crm_user и --password обязательны. '
                     'Передайте через CLI или переменные окружения.')
    credentials = base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')
    return {"Authorization": f"Basic {credentials}"}


@pytest.fixture(scope='session')
def config_consumer(request):
    return request.config.getoption('--consumer')


@pytest.fixture(scope='class')
def auth_session_user(base_url, config_user_credentials):
    return user_session_by_user(
        base_url=base_url,
        auth_headers=config_user_credentials,
        verify=False,
    )


@pytest.fixture(scope='class')
def create_device_and_link_to_consumer(auth_session_user, config_consumer):
    codes = ["BV002443", "BV002437"]
    device1, device2 = [get_device_create_json(code=code) for code in codes]

    for device in (device1, device2):
        auth_session_user.devices_api.create_devices(data=device)

    case_date = get_case_create_json(case_reason="LinkingDevice", consumer=config_consumer)
    create_linking_case = auth_session_user.devices_api.create_case(data=case_date)

    link_data = get_link_data(
        consumer=config_consumer,
        device1=device1["ProductInstance"]["Code"],
        device2=device2["ProductInstance"]["Code"],
        request=create_linking_case["result"]["ConsumerRequest"]["Code"],
    )
    link = auth_session_user.devices_api.consumer_device_link(data=link_data)

    link_date_data = get_linking_date_data(
        consumer=config_consumer,
        device1=device1["ProductInstance"]["Code"],
        device2=device2["ProductInstance"]["Code"],
        request=create_linking_case["result"]["ConsumerRequest"]["Code"],
        date=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        item1=link["result"]["BindingRequest"]["Items"][0]["ItemCode"],
        item2=link["result"]["BindingRequest"]["Items"][1]["ItemCode"],
    )
    auth_session_user.devices_api.set_transaction_date(data=link_date_data)

    return [device1["ProductInstance"]["Code"], device2["ProductInstance"]["Code"]]
