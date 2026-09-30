import json

import allure

from core.common import BaseApi


class CheckupApi(BaseApi):

    @allure.step('CRM.03 Создание запроса чекап')
    def create_checkup_case(self, data):
        response = self.put(
            url='/ServiceModel/cases.svc/searchOrCreate',
            json=data,
        )
        return self._request_result(response)

    @allure.step('CRM.227 Группировка устройств для чекапа')
    def group_devices_for_checkup(self, data):
        response = self.get(
            url='/ServiceModel/ProductInstances/groupDevicesForCheckup',
            json=data,
        )
        return self._request_result(response)

    @allure.step('CRM.228 Валидация устройств для чекапа')
    def validate_checkup_devices(self, data):
        response = self.post(
            url='/ServiceModel/ProductInspection/ValidateCheckUpDevices',
            json=data,
        )
        return self._request_result(response)

    @allure.step('CRM.234 Запрос на прохождение опроса чекап')
    def create_checkup_survey(self, data):
        response = self.post(
            url='/ServiceModel/ConsumerSurveys/CreateCheckupSurvey',
            json=data,
        )
        return self._request_result(response)

    @allure.step('CRM.235 Сохранение результата опроса чекап')
    def save_checkup_survey_results(self, data):
        response = self.post(
            url='/ServiceModel/ConsumerSurveys/SaveCheckupSurveyResults',
            json=data,
        )
        return self._request_result(response)

    @allure.step('CRM.233 Закрытие запроса чекап')
    def close_checkup_case(self, data):
        response = self.post(
            url='/ServiceModel/ConsumerRequests/CloseCheckUpConsumerRequest',
            json=data,
        )
        return self._request_result(response)

    @allure.step('CRM.229 Отчет по чекапу устройства')
    def get_checkup_report(self, consumer, device):
        response = self.get(
            url='/ServiceModel/consumers/GetCheckupReportForClientDevice',
            params={'filter': json.dumps({
                'Consumer.Code': consumer,
                'ProductInstance.Code': device,
            }, ensure_ascii=False)},
        )
        return self._request_result(response)

    @allure.step('CRM.232 Диагностический результат устройства')
    def get_diagnostic_result(self, consumer, device):
        response = self.get(
            url='/ServiceModel/ProductInspections/GetDiagnosticResult',
            params={'filter': json.dumps({
                'Consumer.Code': consumer,
                'ProductInstance.Code': device,
            }, ensure_ascii=False)},
        )
        return self._request_result(response)

    @staticmethod
    def assert_success(response):
        assert 200 <= response['code'] < 300, (
            f"Ожидался успешный ответ 2xx, получен {response['code']}: "
            f"{response['result']}"
        )
