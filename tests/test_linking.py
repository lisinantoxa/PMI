from datetime import datetime

from pytest import mark
from allure import (
    title,
    suite
)

from resources.data.regression_data import (get_link_data,
                                            get_linking_date_data,
                                            get_device_create_json,
                                            get_case_create_json)
from resources.test_data import SUCCESSFUL_200_RESPONSE_CODE, SUCCESSFUL_201_RESPONSE_CODE, SUCCESSFUL_422_RESPONSE_CODE


@suite('API тесты по флоу привязки устройства')
class TestLinkingApi:

    @mark.flaky(reruns=0, reruns_delay=60)
    @title('Привязка двухкомпонентного устройства')
    @mark.parametrize("codes", [
        ["BV002443", "BV002437"],
        ["BV007904", "BV007908"]
    ])
    def test_linking_duos_devices(self, base_url, auth_session_user, config_user_credentials, config_consumer, codes):
        device1, device2 = [get_device_create_json(code=code) for code in codes]
        case_date = get_case_create_json(case_reason="LinkingDevice", consumer=config_consumer)
        create_device1, create_device2 = [
            auth_session_user.devices_api.create_devices(data=device, config_user_credentials=config_user_credentials)
            for device in [device1, device2]
        ]
        auth_session_user.client_api.assert_response(current_response=create_device1,
                                                     expected_response=SUCCESSFUL_200_RESPONSE_CODE)
        auth_session_user.client_api.assert_response(current_response=create_device2,
                                                     expected_response=SUCCESSFUL_200_RESPONSE_CODE)
        create_linking_case = auth_session_user.devices_api.create_case(data=case_date,
                                                                        config_user_credentials=config_user_credentials)
        auth_session_user.client_api.assert_response(current_response=create_linking_case,
                                                     expected_response=SUCCESSFUL_201_RESPONSE_CODE)
        link_data = get_link_data(consumer=config_consumer,
                                  device1=device1["ProductInstance"]["Code"],
                                  device2=device2["ProductInstance"]["Code"],
                                  request=create_linking_case["result"]["ConsumerRequest"]["Code"])
        link = auth_session_user.devices_api.consumer_device_link(data=link_data,
                                                                  config_user_credentials=config_user_credentials)
        auth_session_user.client_api.assert_response(current_response=link,
                                                     expected_response=SUCCESSFUL_422_RESPONSE_CODE)
        link_date_data = get_linking_date_data(consumer=config_consumer,
                                               device1=device1["ProductInstance"]["Code"],
                                               device2=device2["ProductInstance"]["Code"],
                                               request=create_linking_case["result"]["ConsumerRequest"]["Code"],
                                               date=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                                               item1=link["result"]["BindingRequest"]["Items"][0]["ItemCode"],
                                               item2=link["result"]["BindingRequest"]["Items"][1]["ItemCode"])
        set_date = auth_session_user.devices_api.set_transaction_date(data=link_date_data,
                                                                      config_user_credentials=config_user_credentials)
        auth_session_user.client_api.assert_response(current_response=set_date,
                                                     expected_response=SUCCESSFUL_200_RESPONSE_CODE)
        assert set_date["result"]["BindingRequest"]["Items"][0]["Result"] == "SuccessfulBinding"
        assert set_date["result"]["BindingRequest"]["Items"][1]["Result"] == "SuccessfulBinding"
