import testit
from allure import suite, title
from pytest import mark

from resources.data.replacement_data import (
    get_init_product_inspection_json,
    get_product_inspection_result_json,
    get_retail_replacement_order_json,
)
from resources.test_data import (
    SUCCESSFUL_200_RESPONSE_CODE,
    INSPECTION_RESULT_CHARGER_108,
    EXPECTED_REPLACEMENT_SOLUTION_CODE,
    REPLACEMENT_INBOUND_PROBLEM_CODE,
    REPLACEMENT_SOLUTION_CODE,
    SURVEY_CHARGER_RESULT_108,
    SURVEY_CHARGER_RESULT_105,
    INSPECTION_RESULT_CHARGER_105,
    EXPECTED_REPLACEMENT_SOLUTION_CODE_AFTER_PHYSICAL_DAMAGE,
    REPLACEMENT_REPLACEMENT_RESOLVE_REASON_CODE
)
from resources.testit_messages import add_flow_success_message

REPLACEMENT_ORDER_SUCCESS_MESSAGE = 'Запрос сохранен'


@suite('API тесты по флоу замены устройства (web)')
class TestReplacementApi:

    @testit.workItemID("1616")
    @mark.flaky(reruns=1, reruns_delay=60)
    @title('Замена устройства через веб: диагностика и заказ на замену: проблема с электроникой')
    def test_device_replacement_web_flow_electronic_issue(
            self,
            auth_session_user,
            config_consumer,
            create_device_and_link_to_consumer,
    ):
        device1, _ = create_device_and_link_to_consumer
        devices_api = auth_session_user.devices_api

        with testit.step("CRM.25 Инициация диагностики устройства"):
            inspection = devices_api.init_product_inspection(
                data=get_init_product_inspection_json(config_consumer, device1),
            )
            devices_api.assert_response(inspection, SUCCESSFUL_200_RESPONSE_CODE)

        assert inspection['result']['SurveyCode'], 'В ответе CRM.25 отсутствует SurveyCode'

        request_code = inspection['result']['ConsumerRequest']['Code']
        assert request_code, 'В ответе CRM.25 отсутствует ConsumerRequest.Code'

        inspection_code = inspection['result']['ProductInspection']['Code']
        assert inspection_code, 'В ответе CRM.25 отсутствует ProductInspection.Code'

        with testit.step("CRM.27 Отправка результатов диагностики"):
            inspection_result = devices_api.save_product_inspection_result(
                data=get_product_inspection_result_json(
                    request=request_code,
                    inspection=inspection_code,
                    survey_result=SURVEY_CHARGER_RESULT_108,
                ),
            )
            devices_api.assert_response(inspection_result, SUCCESSFUL_200_RESPONSE_CODE)

        saved_inspection = inspection_result['result']['ProductInspection']

        # Диагностика проведена по тому же запросу
        assert inspection_result['result']['ConsumerRequest']['Code'] == request_code, (
            f"Ожидался запрос {request_code}, получен "
            f"{inspection_result['result']['ConsumerRequest']['Code']}"
        )

        # Диагностика проведена по отправленному устройству
        inspected_items = saved_inspection['Items']
        assert inspected_items, 'В ответе CRM.27 отсутствуют Items диагностики'
        inspected_device = inspected_items[0]['ProductInstance']['Code']
        assert inspected_device.lower() == device1.lower(), (
            f'Ожидалась диагностика устройства {device1}, получено {inspected_device}'
        )

        # Результат диагностики соответствует ответу опроса 108
        assert inspected_items[0]['Result'] == INSPECTION_RESULT_CHARGER_108, (
            f"Ожидался результат диагностики {INSPECTION_RESULT_CHARGER_108}, "
            f"получен {inspected_items[0]['Result']}"
        )

        # CRM вернула ожидаемое возможное решение
        possible_solutions = saved_inspection['PossibleSolutions']
        assert possible_solutions, 'В ответе CRM.27 отсутствуют PossibleSolutions'
        solution_codes = [s['Solution']['Code'] for s in possible_solutions]
        assert EXPECTED_REPLACEMENT_SOLUTION_CODE in solution_codes, (
            f"Ожидалось решение {EXPECTED_REPLACEMENT_SOLUTION_CODE}, "
            f"получены: {solution_codes}"
        )

        with testit.step("CRM.17 Запрос на создание заказа замены"):
            replacement_order = devices_api.create_retail_replacement_order(
                data=get_retail_replacement_order_json(request=request_code),
            )
            devices_api.assert_response(replacement_order, SUCCESSFUL_200_RESPONSE_CODE)

        assert replacement_order['result']['Code'] == 200, (
            f"Ожидался Code 200 в ответе CRM.17, получен "
            f"{replacement_order['result']['Code']}"
        )
        assert replacement_order['result']['Message'] == REPLACEMENT_ORDER_SUCCESS_MESSAGE, (
            f"Ожидалось сообщение '{REPLACEMENT_ORDER_SUCCESS_MESSAGE}', получено "
            f"'{replacement_order['result']['Message']}'"
        )

        with testit.step('CRM.39 Проверка закрытого запроса замены'):
            request_info = devices_api.get_consumer_request_with_inspections_acts_orders(
                request_code=request_code,
            )
            devices_api.assert_response(request_info, SUCCESSFUL_200_RESPONSE_CODE)
            devices_api.assert_request_inprogress(
                request_info,
                REPLACEMENT_INBOUND_PROBLEM_CODE,
                REPLACEMENT_SOLUTION_CODE,
            )
        add_flow_success_message(
            flow_name="Замена устройства",
            request_code=request_code,
            checks=[
                "запрос диагностики создан",
                "результаты диагностики отправлены",
                "опрос создан",
                "диагностика создана",
                "запрос в статусе 'в процессе'",
                "CRM.39 подтвердил корректные значения",
                "причина открытия и решения клиента заполнены корректно"
            ],
            consumer=config_consumer,
            devices=f"{device1}",
            diagnostic=f'{inspected_items[0]["Result"]}',
            solution=EXPECTED_REPLACEMENT_SOLUTION_CODE
        )

    @testit.workItemID("1616")
    @mark.flaky(reruns=1, reruns_delay=60)
    @title('Замена устройства через веб: диагностика и заказ на замену: физическая повреждения ')
    def test_device_replacement_web_flow_physical_damage(
            self,
            auth_session_user,
            config_consumer,
            create_device_and_link_to_consumer,
    ):
        device1, _ = create_device_and_link_to_consumer
        devices_api = auth_session_user.devices_api

        with testit.step("CRM.25 Инициация диагностики устройства"):
            inspection = devices_api.init_product_inspection(
                data=get_init_product_inspection_json(config_consumer, device1),
            )
            devices_api.assert_response(inspection, SUCCESSFUL_200_RESPONSE_CODE)

        assert inspection['result']['SurveyCode'], 'В ответе CRM.25 отсутствует SurveyCode'

        request_code = inspection['result']['ConsumerRequest']['Code']
        assert request_code, 'В ответе CRM.25 отсутствует ConsumerRequest.Code'

        inspection_code = inspection['result']['ProductInspection']['Code']
        assert inspection_code, 'В ответе CRM.25 отсутствует ProductInspection.Code'

        with testit.step("CRM.27 Отправка результатов диагностики"):
            inspection_result = devices_api.save_product_inspection_result(
                data=get_product_inspection_result_json(
                    request=request_code,
                    inspection=inspection_code,
                    survey_result=SURVEY_CHARGER_RESULT_105,
                ),
            )
            devices_api.assert_response(inspection_result, SUCCESSFUL_200_RESPONSE_CODE)

        saved_inspection = inspection_result['result']['ProductInspection']

        # Диагностика проведена по тому же запросу
        assert inspection_result['result']['ConsumerRequest']['Code'] == request_code, (
            f"Ожидался запрос {request_code}, получен "
            f"{inspection_result['result']['ConsumerRequest']['Code']}"
        )

        # Диагностика проведена по отправленному устройству
        inspected_items = saved_inspection['Items']
        assert inspected_items, 'В ответе CRM.27 отсутствуют Items диагностики'
        inspected_device = inspected_items[0]['ProductInstance']['Code']
        assert inspected_device.lower() == device1.lower(), (
            f'Ожидалась диагностика устройства {device1}, получено {inspected_device}'
        )

        # Результат диагностики соответствует ответу опроса 108
        assert inspected_items[0]['Result'] == INSPECTION_RESULT_CHARGER_105, (
            f"Ожидался результат диагностики {INSPECTION_RESULT_CHARGER_105}, "
            f"получен {inspected_items[0]['Result']}"
        )

        # CRM вернула ожидаемое возможное решение
        possible_solutions = saved_inspection['PossibleSolutions']
        assert possible_solutions, 'В ответе CRM.27 отсутствуют PossibleSolutions'
        solution_codes = [s['Solution']['Code'] for s in possible_solutions]
        assert EXPECTED_REPLACEMENT_SOLUTION_CODE_AFTER_PHYSICAL_DAMAGE in solution_codes, (
            f"Ожидалось решение {EXPECTED_REPLACEMENT_SOLUTION_CODE_AFTER_PHYSICAL_DAMAGE}, "
            f"получены: {solution_codes}"
        )

        with testit.step("CRM.17 Запрос на создание заказа замены"):
            replacement_order = devices_api.create_retail_replacement_order(
                data=get_retail_replacement_order_json(request=request_code),
            )
            devices_api.assert_response(replacement_order, SUCCESSFUL_200_RESPONSE_CODE)

        assert replacement_order['result']['Code'] == 200, (
            f"Ожидался Code 200 в ответе CRM.17, получен "
            f"{replacement_order['result']['Code']}"
        )
        assert replacement_order['result']['Message'] == REPLACEMENT_ORDER_SUCCESS_MESSAGE, (
            f"Ожидалось сообщение '{REPLACEMENT_ORDER_SUCCESS_MESSAGE}', получено "
            f"'{replacement_order['result']['Message']}'"
        )

        with testit.step('CRM.39 Проверка закрытого запроса замены'):
            request_info = devices_api.get_consumer_request_with_inspections_acts_orders(
                request_code=request_code,
            )
            devices_api.assert_response(request_info, SUCCESSFUL_200_RESPONSE_CODE)
            devices_api.assert_request_closed(
                request_info,
                REPLACEMENT_INBOUND_PROBLEM_CODE,
                REPLACEMENT_REPLACEMENT_RESOLVE_REASON_CODE,
            )
        add_flow_success_message(
            flow_name="Замена устройства",
            request_code=request_code,
            checks=[
                "запрос диагностики создан",
                "результаты диагностики отправлены",
                "опрос создан",
                "диагностика создана",
                "запрос в статусе 'закрыто'",
                "CRM.39 подтвердил корректные значения",
                "причина открытия и закрытия заполнены корректно"
            ],
            consumer=config_consumer,
            devices=f"{device1}",
            diagnostic=f'{inspected_items[0]["Result"]}',
            solution=EXPECTED_REPLACEMENT_SOLUTION_CODE_AFTER_PHYSICAL_DAMAGE
        )
