from core.common import BaseRandomizer


def get_new_client_json(
        Number=BaseRandomizer().phone(mask='79xxxxxxxxx'),
        BirthDate="2002-11-20",
        Gender="Female",
        Name="Елизавета",
        Surname="Алексеевна"
):
    return {
        "$type": "PMI.POS.Services.Customers.Model.ClientFormValidateRequest",
        "$version": "1.0.0.0",
        "Person": {
            "ContactInfo": {
                "Addresses": [
                    {
                        "City": "Ярославль",
                        "FIAS": {
                            "Code": "6b1bab7d-ee45-4168-a2a6-4ce2880d90d3",
                            "CodeSpace": "SmacX"
                        },
                        "FIASLevel": "1"
                    }
                ],
                "BirthDate": BirthDate,
                "Gender": Gender,
                "Name": Name,
                "Surname": Surname,
                "PhoneNumbers": [
                    {
                        "Type": "Mobile",
                        "Number": Number
                    }
                ]
            },
            "Status": "Draft"
        },
        "Consumer": {
            "Registration": {
                "RegisteredBy": {
                    "$type": "PMI.BDDM.Staticdata.ADUserReference",
                    "Code": "MYIZHORA\\amezents1",
                    "CodeSpace": "ActiveDirectory",
                    "Name": "Саляхов Ринат"
                },
                "SalePoint": {
                    "$type": "PMI.BDDM.Staticdata.POSReference",
                    "Code": "NO001805"
                }
            }
        }
    }


def get_not_exist_name():
    return BaseRandomizer().uid()


def get_validation_code_json(AppFormId):
    return {
        "$type": "PMI.POS.Services.Customers.Model.CustomerCreateRequest",
        "$version": "2.82.6.0",
        "AppFormId": AppFormId,
        "ValidationCode": "1111",
        "Channel": "POS"
    }


def get_depersonalization_json(code):
    return {
        "$type": "Terrasoft.Configuration.Pmi.CoreCrm.DepersonalizationRequest",
        "$version": "2.97.2.0",
        "Consumer": {
            "Code": code,
            "CodeSpace": "B2CCRM",
            "DeleteReason": "101",
            "DeleteType": {
                "Code": "101"
            }
        },
        "User": {
            "$type": "PMI.BDDM.Staticdata.ADUserReference",
            "Code": "MYIZHORA\\olos1",
            "CodeSpace": "ActiveDirectory",
            "Name": "Olga Los"
        },
        "Channel": "QPointCC"
    }
