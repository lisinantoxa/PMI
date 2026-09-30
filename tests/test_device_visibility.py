import testit
from allure import suite, title
from pytest import mark

from resources.data.device_visibility_data import get_hide_device_json
from resources.test_data import SUCCESSFUL_200_RESPONSE_CODE
from resources.testit_messages import add_flow_success_message


@suite('API тесты по скрытию устройства')
class TestDeviceVisibilityApi:

    @mark.flaky(reruns=1, reruns_delay=60)
    @testit.workItemID("1631")
    @title('Скрытие устройства в личном кабинете пользователя')
    def test_hide_device_in_web(
            self, auth_session_user, config_consumer, create_device_and_link_to_consumer):
        device = create_device_and_link_to_consumer[0]

        with testit.step('CRM.116 Скрытие устройства в ЛК пользователя'):
            hide_device = auth_session_user.devices_api.hide_or_display_device(
                data=get_hide_device_json(consumer=config_consumer, device=device),
            )
            auth_session_user.devices_api.assert_response(hide_device, SUCCESSFUL_200_RESPONSE_CODE)

        assert hide_device["result"]["Message"] == "Устройство удалено из профиля клиента"
        add_flow_success_message(
            flow_name="Скрытие устройства WEB",
            checks=[
                "запрос успешно выполнен",
                "message ответа соответствует ожидаемому",
            ],
            consumer=config_consumer,
            device=device,
            response=hide_device
        )
