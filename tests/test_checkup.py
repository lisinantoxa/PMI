import testit
from allure import suite, title

from resources.data.checkup_data import (
    get_checkup_case_create_json,
    get_checkup_close_json,
    get_checkup_survey_json,
    get_checkup_validate_json,
    get_checkup_group_json,
)


@testit.workItemID("8d89dfb5-3d60-4d47-a3f4-c93e2f93e46d")
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

        with testit.step("CRM.03 Создание запроса чекап"):
            case = checkup.create_checkup_case(
                data=get_checkup_case_create_json(config_consumer),
                config_user_credentials=config_user_credentials,
            )
            checkup.assert_success(case)
        request_code = case['result']['ConsumerRequest']['Code']

        with testit.step("CRM.227 Группировка устройств для чекапа"):
            group = checkup.group_devices_for_checkup(
                data=get_checkup_group_json(request_code, config_consumer),
                config_user_credentials=config_user_credentials,
            )
            checkup.assert_success(group)

        with testit.step("CRM.228 Валидация устройств для чекапа"):
            validation = checkup.validate_checkup_devices(
                data=get_checkup_validate_json(request_code, config_consumer, [device1, device2]),
                config_user_credentials=config_user_credentials,
            )
            checkup.assert_success(validation)

        with testit.step("CRM.234 Создание опроса чекап"):
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

        with testit.step("CRM.235 Сохранение результата опроса чекап"):
            results = checkup.save_checkup_survey_results(
                data=get_checkup_survey_json(request_code, config_consumer, survey_code),
                config_user_credentials=config_user_credentials,
            )
            checkup.assert_success(results)

        with testit.step("CRM.233 Закрытие запроса чекап"):
            closed = checkup.close_checkup_case(
                data=get_checkup_close_json(request_code),
                config_user_credentials=config_user_credentials,
            )
            checkup.assert_success(closed)

        for device in (device1, device2):
            with testit.step(f"CRM.229 Отчет по чекапу устройства {device}"):
                report = checkup.get_checkup_report(config_consumer, device, config_user_credentials)
                checkup.assert_success(report)

            with testit.step(f"CRM.232 Диагностический результат устройства {device}"):
                diagnostic = checkup.get_diagnostic_result(config_consumer, device, config_user_credentials)
                checkup.assert_success(diagnostic)

        testit.addMessage(f"Флоу чекапа устройства успешно пройден по всем шагам и проверкам итоговых результатов. CRM.233 - {closed}")
