from resources.data.regression_data import get_new_client_json

# HTTP-коды
SUCCESSFUL_200_RESPONSE_CODE = 200
SUCCESSFUL_201_RESPONSE_CODE = 201
SUCCESSFUL_202_RESPONSE_CODE = 202
EXPECTED_422_RESPONSE_CODE = 422

# Тестовые данные
NEW_CLIENT_JSON = get_new_client_json()

# Замена web: ответы опроса диагностики
SURVEY_CHARGER_RESULT_108 = '108'  # Проблемы с электроникой
SURVEY_CHARGER_RESULT_105 = '105'  # Физические повреждения

# Чекап
CHECKUP_INBOUND_PROBLEM_CODE = 'Чекап'
CHECKUP_RESOLVE_REASON_CODE = 'Чекап проведен, красная зона, доступна замена по гарантии'

# Скрытие устройства
WEB_HIDE_INBOUND_PROBLEM_CODE = 'Удаление устройства из профиля'
WEB_HIDE_RESOLVE_REASON_CODE = 'Устройство удалено из профиля'

# Проф. чистка
PROF_CLEANING_INBOUND_PROBLEM_CODE = 'Профессиональная чистка'
PROF_CLEANING_NO_CLEANING_RESOLVE_REASON_CODE = 'Диагностика проведена (чистка не состоялась)'
PROF_CLEANING_REPLACEMENT_RESOLVE_REASON_CODE = 'Проф чистка не помогла, необходима замена'

# Замена web
INSPECTION_RESULT_CHARGER_108 = 'ElectronicIssue'
INSPECTION_RESULT_CHARGER_105 = 'PhysicalDamage'
EXPECTED_REPLACEMENT_SOLUTION_CODE = 'KITWarrantyReplacement'
EXPECTED_REPLACEMENT_SOLUTION_CODE_AFTER_PHYSICAL_DAMAGE = 'Sale'
REPLACEMENT_INBOUND_PROBLEM_CODE = 'Диагностика'
REPLACEMENT_SOLUTION_CODE = 'Гарантийная замена комплекта'
REPLACEMENT_REPLACEMENT_RESOLVE_REASON_CODE = 'Продажа'
