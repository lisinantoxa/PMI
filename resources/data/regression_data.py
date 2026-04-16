from more_itertools.more import consumer

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
            "Code": "MYIZHORA\\alisin1",
            "CodeSpace": "ActiveDirectory",
            "Name": "Olga Los"
        },
        "Channel": "QPointCC"
    }


def get_device_create_json(code,
                           serial_number=None):
    if serial_number is None:
        serial_number = BaseRandomizer().random_string(string_length=14)
    return {
        "$type": "PMI.QPCC.Services.Crm.CoreCrmExtensions.PmCreateDeviceRequest",
        "$version": "2.89.1.0",
        "User": {
            "Code": "MYIZHORA\\alisin1",
            "CodeSpace": "ActiveDirectory"
        },
        "Consumer": {
            "Code": "CONS7971378",
            "CodeSpace": "B2CCRM"
        },
        "ProductInstance": {
            "$type": "PMI.BDDM.Staticdata.EquipmentProductInstanceReference",
            "Code": serial_number,
            "CodeSpace": "DeviceManagement"
        },
        "Product": {
            "$type": "PMI.BDDM.Staticdata.BrandVariantReference",
            "Code": code,
            "CodeSpace": "MDM",
            "Name": "Зарядное устройство IQOS 3 DUOS (золотой)"
        }}


def get_case_create_json(case_reason,
                         consumer):
    return {
        "$type": "PMI.POS.Services.Surveys.Model.Case.CaseSearch+Request",
        "$version": "1.0.0.0",
        "Consumer": {
            "$type": "PMI.BDDM.Transactionaldata.ConsumerProductInspectionRequest",
            "Code": consumer,
            "CodeSpace": "B2CCRM"
        },
        "SalesPoint": {
            "$type": "PMI.BDDM.Staticdata.POSReference",
            "Code": "MS257434",
            "CodeSpace": "MDM"
        },
        "ConsumerRequestProblemType": {
            "Code": case_reason,
            "Name": "Привязка устройства"
        },
        "User": {
            "Code": "myahina@myizhora.net",
            "CodeSpace": "ActiveDirectory"
        }
    }


def get_link_data(device1,
                  device2,
                  consumer,
                  request):
    return {
        "$type": "PMI.POS.Services.LinkedObjects.Model.BindDevice+Request",
        "$version": "1.0.0.0",
        "BindingRequest": {
            "Items": [
                {
                    "SalePoint": {
                        "$type": "PMI.BDDM.Staticdata.POSReference",
                        "Code": "MS257434",
                        "CodeSpace": "MDM"
                    },
                    "SerialNumber": device1
                },
                {
                    "SalePoint": {
                        "$type": "PMI.BDDM.Staticdata.POSReference",
                        "Code": "MS257434",
                        "CodeSpace": "MDM"
                    },
                    "SerialNumber": device2
                }
            ],
            "Consumer": {
                "Code": consumer,
                "CodeSpace": "RRPSF"
            },
            "Code": request,
            "CodeSpace": "B2CCRM"
        },
        "ConsumerRequest": {
            "Code": request,
            "CodeSpace": "B2CCRM"
        },
        "User": {
            "Code": "MYIZHORA\\alisin1",
            "CodeSpace": "ActiveDirectory"
        }
    }


def get_linking_date_data(device1,
                          device2,
                          consumer,
                          request,
                          item1,
                          item2,
                          date):
    return {
        "$type": "PMI.POS.Services.LinkedObjects.Model.SetTransactionDate+Request",
        "$version": "1.0.0.0",
        "BindingRequest": {
            "Items": [
                {
                    "ItemCode": item1,
                    "ProductInstance": {
                        "$type": "PMI.BDDM.Staticdata.EquipmentProductInstanceReference",
                        "Code": device1,
                        "CodeSpace": "DeviceManagement"
                    },
                    "SaleDate": date,
                    "SalePoint": {
                        "$type": "PMI.BDDM.Staticdata.POSReference",
                        "Code": "MS257434",
                        "CodeSpace": "MDM"
                    }
                }
                ,
                {
                    "ItemCode": item2,
                    "ProductInstance": {
                        "$type": "PMI.BDDM.Staticdata.EquipmentProductInstanceReference",
                        "Code": device2,
                        "CodeSpace": "DeviceManagement"
                    },
                    "SaleDate": date,
                    "SalePoint": {
                        "$type": "PMI.BDDM.Staticdata.POSReference",
                        "Code": "NO001805",
                        "CodeSpace": "MDM"
                    }
                }
            ],
            "Consumer": {
                "Code": consumer,
                "CodeSpace": "RRPSF"
            },
            "Code": request,
            "CodeSpace": "B2CCRM"
        },
        "ConsumerRequest": {
            "Code": request,
            "CodeSpace": "B2CCRM"
        },
        "User": {
            "Code": "myahina@myizhora.net",
            "CodeSpace": "ActiveDirectory"
        }
    }
