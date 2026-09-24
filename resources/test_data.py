from resources.data.regression_data import (get_new_client_json)

SUCCESSFUL_200_RESPONSE_CODE = 200
SUCCESSFUL_201_RESPONSE_CODE = 201
SUCCESSFUL_202_RESPONSE_CODE = 202
SUCCESSFUL_422_RESPONSE_CODE = 422
NEW_CLIENT_JSON = get_new_client_json()
CHECKUP_INBOUND_PROBLEM_CODE = 'Чекап'
CHECKUP_RESOLVE_REASON_CODE = 'Чекап проведен, красная зона, доступна замена по гарантии'
WEB_HIDE_INBOUND_PROBLEM_CODE = 'Удаление устройства из профиля'
WEB_HIDE_RESOLVE_REASON_CODE = 'Устройство удалено из профиля'
PROF_CLEANING_INBOUND_PROBLEM_CODE = 'Профессиональная чистка'
PROF_CLEANING_NO_CLEANING_RESOLVE_REASON_CODE = 'Диагностика проведена (чистка не состоялась)'
PROF_CLEANING_REPLACEMENT_RESOLVE_REASON_CODE = 'Проф чистка не помогла, необходима замена'

