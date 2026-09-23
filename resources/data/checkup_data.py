def get_checkup_case_create_json(consumer):
    return {
        '$type': 'PMI.POS.Services.Surveys.Model.Case.CaseSearch+Request',
        '$version': '1.0.0.0',
        'Consumer': {'$type': 'PMI.BDDM.Transactionaldata.ConsumerProductInspectionRequest',
                     'Code': consumer, 'CodeSpace': 'B2CCRM'},
        'SalesPoint': {'$type': 'PMI.BDDM.Staticdata.POSReference',
                       'Code': 'MS257434', 'CodeSpace': 'MDM'},
        'ConsumerRequestProblemType': {'Code': 'Checkup', 'Name': 'Чекап'},
        'User': {'Code': 'MYIZHORA\\amezents1', 'CodeSpace': 'ActiveDirectory'},
    }


def get_checkup_group_json(request, consumer):
    return {
        'ConsumerRequest': {
            '$type': 'PMI.BDDM.Transactionaldata.ConsumerProductInspectionRequestReference',
            'Code': request, 'CodeSpace': 'B2CCRM',
        },
        'User': {'$type': 'PMI.BDDM.Staticdata.ADUserReference',
                 'Code': 'myahina@myizhora.net', 'CodeSpace': 'ActiveDirectory'},
        'SalePoint': {'$type': 'PMI.BDDM.Staticdata.POSReference',
                      'Code': 'NO001805', 'CodeSpace': 'MDM'},
    }


def get_checkup_validate_json(request, consumer, devices):
    return {
        'ConsumerRequest': {
            '$type': 'PMI.BDDM.Transactionaldata.ConsumerProductInstanceUpgradeRequestReference',
            'Code': request, 'CodeSpace': 'B2CCRM',
        },
        'SalePoint': {'$type': 'PMI.BDDM.Staticdata.POSReference',
                      'CodeSpace': 'MDM', 'Code': 'MS257434'},
        'User': {'$type': 'PMI.BDDM.Staticdata.ADUserReference',
                 'CodeSpace': 'ActiveDirectory', 'Code': 'MYIZHORA\\alisin1'},
        'Items': [{
            '$type': 'PMI.BDDM.Transactionaldata.ProductInstanceInspectionItem',
            'ProductInstance': {
                '$type': 'PMI.BDDM.Staticdata.EquipmentProductInstanceReference',
                'Code': device, 'CodeSpace': 'DeviceManagement',
            },
        } for device in devices],
    }


def get_checkup_survey_json(request, consumer, survey):
    answers = [
        ('SQ-00000070_Q-00051', 'Да'), ('SQ-00000070_Q-00052', 'Да'),
        ('SQ-00000070_Q-00053', 'Да'), ('SQ-00000070_Q-00054', 'Нет'),
        ('SQ-00000070_Q-00055', 'Да'), ('SQ-00000070_Q-00056', 'Да'),
        ('SQ-00000070_Q-00057', 'Да'), ('SQ-00000070_Q-00058', 'Да'),
        ('SQ-00000070_Q-00059', 'Да'), ('SQ-00000070_Q-00060', 'Автоматический расчет'),
        ('SQ-00000070_Q-00061', '0'),
    ]
    return {
        'ConsumerRequest': {'$type': 'PMI.BDDM.Transactionaldata.ConsumerProductInspectionRequestReference',
                            'Code': request, 'CodeSpace': 'B2CCRM'},
        'SalePoint': {'$type': 'PMI.BDDM.Staticdata.POSReference',
                      'CodeSpace': 'MDM', 'Code': 'MS257434'},
        'User': {'$type': 'PMI.BDDM.Staticdata.ADUserReference',
                 'CodeSpace': 'ActiveDirectory', 'Code': 'myahina@myizhora.net'},
        'ConsumerSurvey': {'$type': 'PMI.BDDM.Transactionaldata.ConsumerSurvey',
                           'Code': survey, 'CodeSpace': 'B2CCRM',
                           'Answers': [{'$type': 'PMI.BDDM.Transactionaldata.TextAnswer',
                                        'QuestionCode': code, 'SubmittedReply': value}
                                       for code, value in answers]},
        'Result': '{"question1": true, "question2": true, "question3": false, '
                   '"question4": true, "question5": true, "question6": true, '
                   '"question7": true, "question8": true, "question9": true, '
                   '"question10": true, "question11": "0", "question12": 111}',
    }


def get_checkup_close_json(request):
    return {
        'ConsumerRequest': {'$type': 'PMI.BDDM.Transactionaldata.ConsumerProductInstanceUpgradeRequestReference',
                            'Code': request, 'CodeSpace': 'B2CCRM'},
        'SalePoint': {'$type': 'PMI.BDDM.Staticdata.POSReference',
                      'CodeSpace': 'MDM', 'Code': 'MS257434'},
        'User': {'$type': 'PMI.BDDM.Staticdata.ADUserReference',
                 'CodeSpace': 'ActiveDirectory', 'Code': 'myahina@myizhora.net'},
        'RetailSaleOrder': {'$type': 'PMI.BDDM.Staticdata.RetailSaleOrderReference',
                            'Code': 'OE-00214323234', 'CodeSpace': 'MDM'},
    }
