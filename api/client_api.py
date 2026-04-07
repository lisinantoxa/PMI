import allure
import json

from core.common import BaseApi


class ClientApi(BaseApi):

    @allure.step('CRM.02 Создание анкеты клиента')
    def clients_form_validate(self, new_consumer_json, config_user_credentials):
        url = f'/ServiceModel/clients.svc/clients/formValidate'
        try:
            response = self.post(url=url, json=new_consumer_json, headers=config_user_credentials, external=True)
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

    @allure.step('CRM.09 Создание транзакции отправки кода')
    def create_transaction(self, data, config_user_credentials):
        url = f'/ServiceModel/cios.svc/createTransaction?ConsumerFormCode={data["ConsumerFormCode"]}&CodeDeliveryMethod={data["CodeDeliveryMethod"]}'
        try:
            response = self.post(url=url, headers=config_user_credentials, external=True)
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

    @allure.step('CRM.10NEW Отправка кода подтверждения')
    def set_validation_code(self, code_validation_json, config_user_credentials):
        url = f'/ServiceModel/clients.svc/clients/new'
        try:
            response = self.post(url=url, json=code_validation_json, headers=config_user_credentials, external=True)
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

    @allure.step('CRM.04 Поднятие карточки Клиента')
    def get_extended_consumer(self, consumer, config_user_credentials):
        url = f'/ServiceModel/consumers/GetExtendedConsumer?filter={{"Code":"{consumer}"}}'
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

    @allure.step('CRM.51 Деперсонализация клиента')
    def client_depersonalization(self, depers_json, config_user_credentials):
        url = f'/ServiceModel/clients/depersonalization'
        try:
            response = self.post(url=url, json=depers_json, headers=config_user_credentials, external=True)
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

    @allure.step('Проверка информации по зарегистрированному клиенту')
    def assert_client_info(self, send_info, response_info):
        assert send_info['Person']['ContactInfo']["Gender"] == response_info['Person']['ContactInfo'][
            "Gender"]
        assert send_info['Person']['ContactInfo']["Name"] == response_info['Person']['ContactInfo'][
            'Name']
        assert send_info['Person']['ContactInfo']["Surname"] == response_info['Person']['ContactInfo'][
            'Surname']
        assert send_info['Person']['ContactInfo']["PhoneNumbers"][0]['Number'] == \
               response_info['Person']['ContactInfo']['PhoneNumbers'][0]['Number']
        assert send_info['Person']['ContactInfo']["BirthDate"] == response_info['Person']['ContactInfo'][
            'BirthDate']
