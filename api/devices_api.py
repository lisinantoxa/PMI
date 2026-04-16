import allure
import json

from core.common import BaseApi


class DevicesApi(BaseApi):

    @allure.step('CRM.24 Получение данных по устройствам клиента')
    def get_consumer_devices(self, consumer, config_user_credentials):
        url = f'/ServiceModel/selfService/consumerDevices.svc/get?ConsumerCode={consumer}'
        try:
            response = self.get(url=url, headers=config_user_credentials, external=True)
            if response.status_code == 200:
                result = json.loads(response.text)
            elif response.status_code == 400:
                result = json.loads(response.text)
            elif response.status_code == 401:
                result = response.text
            elif response.status_code == 422:
                result = json.loads(response.text)
            else:
                result = json.loads(response.text)
            return {
                'code': response.status_code,
                'result': result
            }
        except Exception as err:
            raise err

    @allure.step('CRM.203 Создание устройства')
    def create_devices(self, data, config_user_credentials):
        url = f'/ServiceModel/device/CreateDevice'
        try:
            response = self.post(url=url, json=data, headers=config_user_credentials, external=True)
            if response.status_code == 200:
                result = json.loads(response.text)
            elif response.status_code == 400:
                result = json.loads(response.text)
            elif response.status_code == 401:
                result = response.text
            elif response.status_code == 422:
                result = json.loads(response.text)
            else:
                result = json.loads(response.text)
            return {
                'code': response.status_code,
                'result': result
            }
        except Exception as err:
            raise err

    @allure.step('CRM.03 Создание запроса')
    def create_case(self, data, config_user_credentials):
        url = f'/ServiceModel/cases.svc/searchOrCreate'
        try:
            response = self.put(url=url, json=data, headers=config_user_credentials, external=True)
            if response.status_code == 200:
                result = json.loads(response.text)
            elif response.status_code == 404:
                result = json.loads(response.text)
            elif response.status_code == 401:
                result = response.text
            elif response.status_code == 422:
                result = json.loads(response.text)
            else:
                result = json.loads(response.text)
            return {
                'code': response.status_code,
                'result': result
            }
        except Exception as err:
            raise err

    @allure.step('CRM.26 Запрос на привязку устройства')
    def consumer_device_link(self, data, config_user_credentials):
        url = f'/ServiceModel/posService/consumerDevices.svc/link'
        try:
            response = self.post(url=url, json=data, headers=config_user_credentials, external=True)
            if response.status_code == 200:
                result = json.loads(response.text)
            elif response.status_code == 400:
                result = json.loads(response.text)
            elif response.status_code == 401:
                result = response.text
            elif response.status_code == 422:
                result = json.loads(response.text)
            else:
                result = json.loads(response.text)
            return {
                'code': response.status_code,
                'result': result
            }
        except Exception as err:
            raise err

    @allure.step('CRM.47 Ввод даты транзакции')
    def set_transaction_date(self, data, config_user_credentials):
        url = f'/ServiceModel/posService/consumerDevices.svc/setTransactionDate'
        try:
            response = self.post(url=url, json=data, headers=config_user_credentials, external=True)
            if response.status_code == 200:
                result = json.loads(response.text)
            elif response.status_code == 400:
                result = json.loads(response.text)
            elif response.status_code == 401:
                result = response.text
            elif response.status_code == 422:
                result = json.loads(response.text)
            else:
                result = json.loads(response.text)
            return {
                'code': response.status_code,
                'result': result
            }
        except Exception as err:
            raise err
