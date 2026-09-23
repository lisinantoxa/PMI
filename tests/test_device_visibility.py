import testit
from allure import suite, title
from pytest import mark

from resources.data.device_visibility_data import get_hide_device_json
from resources.test_data import SUCCESSFUL_200_RESPONSE_CODE


@suite('API тесты по скрытию устройства')
class TestDeviceVisibilityApi:
    @mark.flaky(reruns=0, reruns_delay=60)
    @testit.workItemID("1193671f-7d86-4f39-80ac-61a0713d14a9")
    @title('Скрытие устройства в личном кабинете пользователя')
    def test_hide_device_in_web(
            self,
            auth_session_user,
            config_user_credentials,
            config_consumer,
            create_device_and_link_to_consumer,
    ):
        device = create_device_and_link_to_consumer[0]

        with testit.step('CRM.116 Скрытие устройства в ЛК пользователя'):
            hide_device = auth_session_user.devices_api.hide_or_display_device(
                data=get_hide_device_json(
                    consumer=config_consumer,
                    device=device,
                ),
                config_user_credentials=config_user_credentials,
            )
            auth_session_user.client_api.assert_response(
                current_response=hide_device,
                expected_response=SUCCESSFUL_200_RESPONSE_CODE,
            )

        assert hide_device["result"]["Message"] == "Устройство удалено из профиля клиента"
        testit.addMessage(
            f'Устройство {device} скрыто в личном кабинете клиента {config_consumer}. CRM.116 response: {hide_device}'
        )
