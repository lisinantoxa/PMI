import json

import allure

from core.common import BaseApi


class DevicesApi(BaseApi):

    @allure.step('CRM.24 Получение данных по устройствам клиента')
    def get_consumer_devices(self, consumer):
        url = f'/ServiceModel/selfService/consumerDevices.svc/get?ConsumerCode={consumer}'
        response = self.get(url=url)
        return self._request_result(response)

    @allure.step('CRM.203 Создание устройства')
    def create_devices(self, data):
        response = self.post(
            url='/ServiceModel/device/CreateDevice',
            json=data,
        )
        return self._request_result(response)

    @allure.step('CRM.03 Создание запроса')
    def create_case(self, data):
        response = self.put(
            url='/ServiceModel/cases.svc/searchOrCreate',
            json=data,
        )
        return self._request_result(response)

    @allure.step('CRM.26 Запрос на привязку устройства')
    def consumer_device_link(self, data):
        response = self.post(
            url='/ServiceModel/posService/consumerDevices.svc/link',
            json=data,
        )
        return self._request_result(response)

    @allure.step('CRM.47 Ввод даты транзакции')
    def set_transaction_date(self, data):
        response = self.post(
            url='/ServiceModel/posService/consumerDevices.svc/setTransactionDate',
            json=data,
        )
        return self._request_result(response)

    @allure.step('CRM.116 Скрытие устройства в личном кабинете')
    def hide_or_display_device(self, data):
        response = self.post(
            url='/ServiceModel/consumerDevices/hideOrdisplayDevice',
            json=data,
        )
        return self._request_result(response)

    @allure.step('CRM.39 Получение запроса')
    def get_consumer_request_with_inspections_acts_orders(self, request_code):
        response = self.get(
            url='/ServiceModel/ConsumerRequests/GetConsumerRequestWithInspectionsActsOrders',
            params={'filter': json.dumps({'CaseCode': request_code})},
        )
        return self._request_result(response)

    @allure.step('CRM.25 Инициация диагностики устройства')
    def init_product_inspection(self, data):
        response = self.post(
            url='/ServiceModel/selfService/consumerDevices.svc/initProductInspection',
            json=data,
        )
        return self._request_result(response)

    @allure.step('CRM.27 Отправка результатов диагностики')
    def save_product_inspection_result(self, data):
        response = self.post(
            url='/ServiceModel/selfService/consumerDevices.svc/saveProductInspectionResult',
            json=data,
        )
        return self._request_result(response)

    @allure.step('CRM.17 Запрос на создание заказа замены')
    def create_retail_replacement_order(self, data):
        response = self.post(
            url='/ServiceModel/selfService/consumerDevices.svc/createRetailReplacementOrder',
            json=data,
        )
        return self._request_result(response)
