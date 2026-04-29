import base64
import pytest
from core.helpers import user_session_by_user
from resources.data.regression_data import get_device_create_json, get_link_data, get_linking_date_data, \
    get_case_create_json
from datetime import datetime


def pytest_addoption(parser):
    parser.addoption(
        '--crm_user',
        action='store',
        help='"--user" Указать логин пользователя'
    )
    parser.addoption(
        '--password',
        action='store',
        help='"--password" Указать пароль пользователя'
    )
    parser.addoption(
        '--consumer',
        action='store',
        help='"--password" Указать тестового клиента'
    )


@pytest.fixture(scope='session')
def base_url():
    return 'https://b2ccrm-preprod.myizapps.com'


@pytest.fixture(scope='session')
def config_user_credentials(request):
    password = request.config.getoption(name='--password')
    username = request.config.getoption(name='--user')
    unicode_string = f'{username}:{password}'
    byte = unicode_string.encode('utf-8')
    valid_credentials = base64.b64encode(byte).decode("utf-8")
    headers = {"Authorization": "Basic " + valid_credentials}
    return headers


@pytest.fixture(scope='session')
def config_consumer(request):
    consumer = request.config.getoption(name='--consumer')
    return consumer


@pytest.fixture(scope='class')
def auth_session_user(base_url, config_user_credentials):
    user_session = user_session_by_user(base_url=base_url)
    return user_session


@pytest.fixture(scope='class')
def create_device_and_link_to_consumer(auth_session_user, config_consumer, config_user_credentials):
    codes = ["BV002443", "BV002437"]
    device1, device2 = [get_device_create_json(code=code) for code in codes]
    [auth_session_user.devices_api.create_devices(data=device, config_user_credentials=config_user_credentials)
     for device in [device1, device2]]
    case_date = get_case_create_json(case_reason="LinkingDevice", consumer=config_consumer)
    create_linking_case = auth_session_user.devices_api.create_case(data=case_date,
                                                                    config_user_credentials=config_user_credentials)
    link_data = get_link_data(consumer=config_consumer,
                              device1=device1["ProductInstance"]["Code"],
                              device2=device2["ProductInstance"]["Code"],
                              request=create_linking_case["result"]["ConsumerRequest"]["Code"])
    link = auth_session_user.devices_api.consumer_device_link(data=link_data,
                                                              config_user_credentials=config_user_credentials)
    link_date_data = get_linking_date_data(consumer=config_consumer,
                                           device1=device1["ProductInstance"]["Code"],
                                           device2=device2["ProductInstance"]["Code"],
                                           request=create_linking_case["result"]["ConsumerRequest"]["Code"],
                                           date=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                                           item1=link["result"]["BindingRequest"]["Items"][0]["ItemCode"],
                                           item2=link["result"]["BindingRequest"]["Items"][1]["ItemCode"])
    auth_session_user.devices_api.set_transaction_date(data=link_date_data,
                                                       config_user_credentials=config_user_credentials)
    return [device1["ProductInstance"]["Code"], device2["ProductInstance"]["Code"]]
