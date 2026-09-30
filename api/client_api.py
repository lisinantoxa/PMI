import allure

from core.common import BaseApi


class ClientApi(BaseApi):

    @allure.step('CRM.02 Создание анкеты клиента')
    def clients_form_validate(self, new_consumer_json):
        response = self.post(
            url='/ServiceModel/clients.svc/clients/formValidate',
            json=new_consumer_json,
        )
        return self._request_result(response)

    @allure.step('CRM.09 Создание транзакции отправки кода')
    def create_transaction(self, data):
        url = (
            f'/ServiceModel/cios.svc/createTransaction'
            f'?ConsumerFormCode={data["ConsumerFormCode"]}'
            f'&CodeDeliveryMethod={data["CodeDeliveryMethod"]}'
        )
        response = self.post(url=url)
        return self._request_result(response)

    @allure.step('CRM.10NEW Отправка кода подтверждения')
    def set_validation_code(self, code_validation_json):
        response = self.post(
            url='/ServiceModel/clients.svc/clients/new',
            json=code_validation_json,
        )
        return self._request_result(response)

    @allure.step('CRM.04 Поднятие карточки Клиента')
    def get_extended_consumer(self, consumer):
        url = f'/ServiceModel/consumers/GetExtendedConsumer?filter={{"Code":"{consumer}"}}'
        response = self.get(url=url)
        return self._request_result(response)

    @allure.step('CRM.51 Деперсонализация клиента')
    def client_depersonalization(self, depers_json):
        response = self.post(
            url='/ServiceModel/clients/depersonalization',
            json=depers_json,
        )
        return self._request_result(response)

    @allure.step('Проверка информации по зарегистрированному клиенту')
    def assert_client_info(self, send_info, response_info):
        assert send_info['Person']['ContactInfo']['Gender'] == response_info['Person']['ContactInfo']['Gender']
        assert send_info['Person']['ContactInfo']['Name'] == response_info['Person']['ContactInfo']['Name']
        assert send_info['Person']['ContactInfo']['Surname'] == response_info['Person']['ContactInfo']['Surname']
        assert send_info['Person']['ContactInfo']['PhoneNumbers'][0]['Number'] == \
               response_info['Person']['ContactInfo']['PhoneNumbers'][0]['Number']
        assert send_info['Person']['ContactInfo']['BirthDate'] == response_info['Person']['ContactInfo']['BirthDate']
