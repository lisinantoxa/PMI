from datetime import datetime

from allure import suite, title

from resources.data.checkup_data import (
    get_checkup_case_create_json,
    get_checkup_close_json,
    get_checkup_survey_json,
    get_checkup_validate_json,
    get_checkup_group_json,
)


@suite('API тесты по флоу чекапа устройства')
class TestCheckupApi:
    @title('Полный флоу чекапа устройства для клиента')
    def test_device_checkup_flow(
            self,
            auth_session_user,
            config_user_credentials,
            config_consumer,
            create_device_and_link_to_consumer,
    ):
        device1, device2 = create_device_and_link_to_consumer
        checkup = auth_session_user.checkup_api

        case = checkup.create_checkup_case(
            data=get_checkup_case_create_json(config_consumer),
            config_user_credentials=config_user_credentials,
        )
        checkup.assert_success(case)
        request_code = case['result']['ConsumerRequest']['Code']

        group = checkup.group_devices_for_checkup(
            data=get_checkup_group_json(request_code, config_consumer),
            config_user_credentials=config_user_credentials,
        )
        checkup.assert_success(group)

        validation = checkup.validate_checkup_devices(
            data=get_checkup_validate_json(request_code, config_consumer, [device1, device2]),
            config_user_credentials=config_user_credentials,
        )
        checkup.assert_success(validation)

        survey = checkup.create_checkup_survey(
            data={'ConsumerRequest': {
                '$type': 'PMI.BDDM.Transactionaldata.ConsumerProductInstanceUpgradeRequestReference',
                'Code': request_code,
                'CodeSpace': 'B2CCRM',
            }, 'SalePoint': {'$type': 'PMI.BDDM.Staticdata.POSReference',
                             'CodeSpace': 'MDM', 'Code': 'MS257434'},
                'User': {'$type': 'PMI.BDDM.Staticdata.ADUserReference',
                         'CodeSpace': 'ActiveDirectory', 'Code': 'myahina@myizhora.net'}},
            config_user_credentials=config_user_credentials,
        )
        checkup.assert_success(survey)
        survey_code = survey['result']['ConsumerSurvey']['Code']

        results = checkup.save_checkup_survey_results(
            data=get_checkup_survey_json(request_code, config_consumer, survey_code),
            config_user_credentials=config_user_credentials,
        )
        checkup.assert_success(results)

        closed = checkup.close_checkup_case(
            data=get_checkup_close_json(request_code),
            config_user_credentials=config_user_credentials,
        )
        checkup.assert_success(closed)

        for device in (device1, device2):
            checkup.assert_success(checkup.get_checkup_report(
                config_consumer, device, config_user_credentials))
            checkup.assert_success(checkup.get_diagnostic_result(
                config_consumer, device, config_user_credentials))
