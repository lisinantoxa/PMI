from datetime import datetime
from pyexpat.errors import codes

from pytest import mark
from allure import (
    title,
    suite
)

from resources.data.regression_data import (
    get_case_create_json, get_prof_clean_survey_json, get_device_create_json, get_prof_clean_survey_result_json)
from resources.test_data import SUCCESSFUL_200_RESPONSE_CODE, SUCCESSFUL_201_RESPONSE_CODE


@suite('API тесты по флоу проф чистки устройства')
class TestProfCleaningApi:

    @mark.flaky(reruns=0, reruns_delay=60)
    @title('Чистка устройства не состоялась')
    def test_diagnostic_completed_without_cleaning(self, base_url, auth_session_user, config_user_credentials,
                                                   config_consumer, create_device_and_link_to_consumer):
        case_date = get_case_create_json(case_reason="ProfessionalCleaning", consumer=config_consumer)
        # создание запроса с причиной открытия проф.чистка
        create_linking_case = auth_session_user.devices_api.create_case(data=case_date,
                                                                        config_user_credentials=config_user_credentials)
        auth_session_user.client_api.assert_response(current_response=create_linking_case,
                                                     expected_response=SUCCESSFUL_201_RESPONSE_CODE)

        # создание опроса и выбор устройства для проф. чистки
        prof_clean_survey_data = get_prof_clean_survey_json(device1=create_device_and_link_to_consumer[0],
                                                            device2=create_device_and_link_to_consumer[1],
                                                            request=create_linking_case["result"]["ConsumerRequest"][
                                                                "Code"])
        create_survey = auth_session_user.prof_cleans_api.create_prof_clean_survey(data=prof_clean_survey_data,
                                                                                   config_user_credentials=config_user_credentials)
        auth_session_user.client_api.assert_response(current_response=create_survey,
                                                     expected_response=SUCCESSFUL_200_RESPONSE_CODE)
        # завершение проф чистки с результатом
        prof_clean_survey_result = get_prof_clean_survey_result_json(
            request=create_linking_case["result"]["ConsumerRequest"][
                "Code"],
            result="101",
            survey=create_survey["result"]["SurveyCode"])
        prof_clean_result = auth_session_user.prof_cleans_api.send_prof_clean_result(data=prof_clean_survey_result,
                                                                                     config_user_credentials=config_user_credentials)
        auth_session_user.client_api.assert_response(current_response=prof_clean_result,
                                                     expected_response=SUCCESSFUL_200_RESPONSE_CODE)
        assert prof_clean_result["result"]["Message"] == "Диагностика проведена. Чистка устройства не требуется."
        assert prof_clean_result["result"]["Code"] == 200

    @mark.flaky(reruns=0, reruns_delay=60)
    @title('Чистка устройства не помогла, необходима замена')
    def test_cleaning_unsuccess_and_replacement(self, base_url, auth_session_user, config_user_credentials,
                                                config_consumer, create_device_and_link_to_consumer):
        case_date = get_case_create_json(case_reason="ProfessionalCleaning", consumer=config_consumer)
        # создание запроса с причиной открытия проф.чистка
        create_linking_case = auth_session_user.devices_api.create_case(data=case_date,
                                                                        config_user_credentials=config_user_credentials)
        auth_session_user.client_api.assert_response(current_response=create_linking_case,
                                                     expected_response=SUCCESSFUL_201_RESPONSE_CODE)

        # создание опроса и выбор устройства для проф. чистки
        prof_clean_survey_data = get_prof_clean_survey_json(device1=create_device_and_link_to_consumer[0],
                                                            device2=create_device_and_link_to_consumer[1],
                                                            request=create_linking_case["result"]["ConsumerRequest"][
                                                                "Code"])
        create_survey = auth_session_user.prof_cleans_api.create_prof_clean_survey(data=prof_clean_survey_data,
                                                                                   config_user_credentials=config_user_credentials)
        auth_session_user.client_api.assert_response(current_response=create_survey,
                                                     expected_response=SUCCESSFUL_200_RESPONSE_CODE)
        # завершение проф чистки с результатом
        prof_clean_survey_result = get_prof_clean_survey_result_json(
            request=create_linking_case["result"]["ConsumerRequest"][
                "Code"],
            result="104",
            survey=create_survey["result"]["SurveyCode"])
        prof_clean_result = auth_session_user.prof_cleans_api.send_prof_clean_result(data=prof_clean_survey_result,
                                                                                     config_user_credentials=config_user_credentials)
        auth_session_user.client_api.assert_response(current_response=prof_clean_result,
                                                     expected_response=SUCCESSFUL_200_RESPONSE_CODE)
        assert prof_clean_result["result"][
                   "Message"] == "Клиенту необходимо оформить замену устройства. Вернитесь в карточку клиента и оформите запрос \"Диагностика\" для валидации возможных решений для клиента."
        assert prof_clean_result["result"]["Code"] == 202
