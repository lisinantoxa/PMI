import allure
import json

from core.common import BaseApi


class ProfCleansApi(BaseApi):

    @allure.step('CRM.63 Выбор устройства и получение опроса')
    def create_prof_clean_survey(self, data, config_user_credentials):
        url = f'/ServiceModel/surveys.svc/createProfCleaningSurvey'
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

    @allure.step('CRM.64 Отправка результатов опроса проф. чистки')
    def send_prof_clean_result(self, data, config_user_credentials):
        url = f'/ServiceModel/surveys.svc/sendProfCleaningSurveyResult'
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
