import allure

from core.common import BaseApi


class ProfCleansApi(BaseApi):

    @allure.step('CRM.63 Выбор устройства и получение опроса')
    def create_prof_clean_survey(self, data):
        response = self.post(
            url='/ServiceModel/surveys.svc/createProfCleaningSurvey',
            json=data,
        )
        return self._request_result(response)

    @allure.step('CRM.64 Отправка результатов опроса проф. чистки')
    def send_prof_clean_result(self, data):
        response = self.post(
            url='/ServiceModel/surveys.svc/sendProfCleaningSurveyResult',
            json=data,
        )
        return self._request_result(response)
