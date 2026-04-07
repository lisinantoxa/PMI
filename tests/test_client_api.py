from pytest import mark

from resources.data.regression_data import get_validation_code_json, get_depersonalization_json
from resources.test_data import (
    SUCCESSFUL_200_RESPONSE_CODE,
    NEW_CLIENT_JSON
)
from allure import (
    title,
    suite
)


@suite('API тесты по клиентам')
class TestClientApi:

    @mark.flaky(reruns=0, reruns_delay=60)
    @title('Регистрации клиента')
    def test_client_reqistration(self, base_url, auth_session_user, config_user_credentials):
        new_client_info = NEW_CLIENT_JSON
        clients_form_validate = auth_session_user.client_api.clients_form_validate(
            new_consumer_json=new_client_info,
            config_user_credentials=config_user_credentials)
        auth_session_user.client_api.assert_response(current_response=clients_form_validate,
                                                     expected_response=SUCCESSFUL_200_RESPONSE_CODE)
        create_transaction = auth_session_user.client_api.create_transaction(
            data={"ConsumerFormCode": clients_form_validate["result"]["ConsumerFormId"],
                  "CodeDeliveryMethod": "Telegram"},
            config_user_credentials=config_user_credentials)
        auth_session_user.client_api.assert_response(current_response=create_transaction,
                                                     expected_response=SUCCESSFUL_200_RESPONSE_CODE)
        try:
            clients_new = auth_session_user.client_api.set_validation_code(
                code_validation_json=get_validation_code_json(
                    AppFormId=clients_form_validate["result"]["ConsumerFormId"]),
                config_user_credentials=config_user_credentials)
            auth_session_user.client_api.assert_response(current_response=clients_new,
                                                         expected_response=SUCCESSFUL_200_RESPONSE_CODE)
            client_info = auth_session_user.client_api.get_extended_consumer(
                consumer=clients_new["result"]["ConsumerCode"],
                config_user_credentials=config_user_credentials)
            auth_session_user.client_api.assert_response(current_response=client_info,
                                                         expected_response=SUCCESSFUL_200_RESPONSE_CODE)
            auth_session_user.client_api.assert_client_info(send_info=new_client_info,
                                                            response_info=client_info["result"])
        finally:
            print(clients_new["result"]["ConsumerCode"])
            auth_session_user.client_api.client_depersonalization(
                depers_json=get_depersonalization_json(code=clients_new["result"]["ConsumerCode"]),
                config_user_credentials=config_user_credentials)
