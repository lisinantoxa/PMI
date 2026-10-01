import base64
import os

import pytest
from datetime import datetime

from core.helpers import user_session_by_user
from resources.data.regression_data import (
    get_device_create_json, get_link_data, get_linking_date_data,
    get_case_create_json, get_new_client_json, get_validation_code_json,
    get_depersonalization_json,
)
from resources.test_data import (
    SUCCESSFUL_200_RESPONSE_CODE, SUCCESSFUL_201_RESPONSE_CODE,
    EXPECTED_422_RESPONSE_CODE,
)

LINKING_DEVICE_CODES = ["BV002443", "BV002437"]


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


# ── Общая логика подготовки устройства ──────────────────────

def _create_and_link_devices(auth_session_user, consumer):
    """Создаёт двухкомпонентное устройство и привязывает его к клиенту.

    Возвращает коды созданных устройств: [device1, device2].
    """
    device1, device2 = [
        get_device_create_json(code=code, consumer=consumer) for code in LINKING_DEVICE_CODES
    ]

    for device in (device1, device2):
        create_device = auth_session_user.devices_api.create_devices(data=device)
        auth_session_user.devices_api.assert_response(create_device, SUCCESSFUL_200_RESPONSE_CODE)

    case_date = get_case_create_json(case_reason="LinkingDevice", consumer=consumer)
    create_linking_case = auth_session_user.devices_api.create_case(data=case_date)
    auth_session_user.devices_api.assert_response(create_linking_case, SUCCESSFUL_201_RESPONSE_CODE)

    request_code = create_linking_case["result"]["ConsumerRequest"]["Code"]

    link_data = get_link_data(
        consumer=consumer,
        device1=device1["ProductInstance"]["Code"],
        device2=device2["ProductInstance"]["Code"],
        request=request_code,
    )
    link = auth_session_user.devices_api.consumer_device_link(data=link_data)
    # 422 — ожидаемая ошибка валидации на этапе привязки
    auth_session_user.devices_api.assert_response(link, EXPECTED_422_RESPONSE_CODE)

    link_date_data = get_linking_date_data(
        consumer=consumer,
        device1=device1["ProductInstance"]["Code"],
        device2=device2["ProductInstance"]["Code"],
        request=request_code,
        date=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        item1=link["result"]["BindingRequest"]["Items"][0]["ItemCode"],
        item2=link["result"]["BindingRequest"]["Items"][1]["ItemCode"],
    )
    set_date = auth_session_user.devices_api.set_transaction_date(data=link_date_data)
    auth_session_user.devices_api.assert_response(set_date, SUCCESSFUL_200_RESPONSE_CODE)

    return [device1["ProductInstance"]["Code"], device2["ProductInstance"]["Code"]]


@pytest.fixture(scope='class')
def create_device_and_link_to_consumer(auth_session_user, config_consumer):
    """Устройства, привязанные к тестовому клиенту из --consumer."""
    return _create_and_link_devices(auth_session_user, config_consumer)


# ── Подготовка нового клиента ───────────────────────────────

@pytest.fixture(scope='class')
def create_client(auth_session_user):
    """Регистрирует нового клиента по флоу CRM.02 → CRM.09 → CRM.10.

    Возвращает dict:
      code — код созданного клиента (ConsumerCode),
      info — анкета, отправленная в CRM.02 (для assert_client_info).

    После теста клиент деперсонализируется (CRM.51).
    """
    new_client_json = get_new_client_json()

    form = auth_session_user.client_api.clients_form_validate(new_consumer_json=new_client_json)
    auth_session_user.client_api.assert_response(form, SUCCESSFUL_200_RESPONSE_CODE)

    transaction = auth_session_user.client_api.create_transaction(data={
        "ConsumerFormCode": form["result"]["ConsumerFormId"],
        "CodeDeliveryMethod": "Telegram",
    })
    auth_session_user.client_api.assert_response(transaction, SUCCESSFUL_200_RESPONSE_CODE)

    client = auth_session_user.client_api.set_validation_code(
        code_validation_json=get_validation_code_json(
            AppFormId=form["result"]["ConsumerFormId"],
        ),
    )
    auth_session_user.client_api.assert_response(client, SUCCESSFUL_200_RESPONSE_CODE)
    consumer_code = client["result"]["ConsumerCode"]

    yield {"code": consumer_code, "info": new_client_json}

    auth_session_user.client_api.client_depersonalization(
        depers_json=get_depersonalization_json(code=consumer_code),
    )


@pytest.fixture(scope='class')
def create_device_and_link_to_new_client(auth_session_user, create_client):
    """Создаёт и привязывает устройства к новому клиенту из create_client."""
    return _create_and_link_devices(auth_session_user, create_client["code"])
