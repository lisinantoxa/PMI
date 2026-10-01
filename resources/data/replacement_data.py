import json

# Точка продажи веб-канала (DigitalPOS)
WEB_SALE_POINT_CODE = "MS269762"
REPLACEMENT_PRODUCT_CODE = "BV004732"
REPLACEMENT_PRODUCT_NAME = "Комплект lil SOLID 3.0, Космический черный"
COURIER_CODE = "CDEK"
COURIER_NAME = "BCP_ZaberySam2"
FULFILLMENT_TYPE = "POSSelfPickUp"
SURVEY_CHARGER_KEY = "charger"

DELIVERY_POINT = {
    "KLADR": "7700000000006180001",
    "Address": {
        "AddressLine": "Цветной б-р, д 2",
        "City": "Москва",
        "Country": "Россия",
        "ZipCode": "127051",
    },
}


def get_init_inspection_json(consumer, device):
    """CRM.25 Инициация диагностики устройства."""
    return {
        "Consumer": {
            "$type": "PMI.BDDM.Staticdata.UserReference",
            "Code": consumer,
            "CodeSpace": "RRPSF",
        },
        "EquipmentProductInstance": {
            "$type": "PMI.BDDM.Staticdata.EquipmentProductInstanceReference",
            "Code": device,
            "CodeSpace": "RRPSF",
        },
        "SalePoint": {
            "$type": "PMI.BDDM.Staticdata.DigitalPOSReference",
            "Code": WEB_SALE_POINT_CODE,
            "CodeSpace": "MDM",
        },
        "Channel": "Web",
    }


def get_inspection_result_json(consumer_request, product_inspection, result):
    """CRM.27 Отправка результатов диагностики."""
    return {
        "Survey": json.dumps({SURVEY_CHARGER_KEY: result}),
        "ConsumerRequest": {
            "$type": "PMI.BDDM.Transactionaldata.ConsumerProductInspectionRequestReference",
            "Code": consumer_request,
            "CodeSpace": "B2CCRM",
        },
        "ProductInspection": {
            "$type": "PMI.BDDM.Transactionaldata.ProductInspectionReference",
            "Code": product_inspection,
            "CodeSpace": "B2CCRM",
        },
        "Channel": "Web",
    }


def get_replacement_order_json(consumer_request):
    """CRM.17 Запрос на создание заказа на замену."""
    return {
        "ReplacementOrder": {
            "$type": "PMI.BDDM.Transactionaldata.RetailReplacementOrder",
            "CreatedBy": {
                "$type": "PMI.BDDM.Staticdata.ADUserReference",
                "Code": "PMRU\\svcUatBitrix",
                "CodeSpace": "ActiveDirectory",
            },
            "DeliveryInfo": {
                "CourierCompany": {"Code": COURIER_CODE, "Name": COURIER_NAME},
                "DeliveryTimeZone": "UTC+03:00",
                "DeliveryType": "Standard",
                "DeliveryPoint": DELIVERY_POINT,
            },
            "SourcePoint": {
                "$type": "PMI.BDDM.Staticdata.POSReference",
                "Code": WEB_SALE_POINT_CODE,
                "CodeSpace": "MDM",
                "Name": "WEB",
            },
            "ProvidedItems": [
                {
                    "ItemCode": "ITMCD-1",
                    "Product": {
                        "$type": "PMI.BDDM.Staticdata.BrandVariantReference",
                        "Code": REPLACEMENT_PRODUCT_CODE,
                        "CodeSpace": "MDM",
                        "Name": REPLACEMENT_PRODUCT_NAME,
                    },
                    "Quantity": {"UOM": "Piece", "Value": 1},
                }
            ],
        },
        "ConsumerRequest": {
            "$type": "PMI.BDDM.Transactionaldata.ConsumerProductInspectionRequest",
            "Code": consumer_request,
            "CodeSpace": "B2CCRM",
            "FulfillmentType": FULFILLMENT_TYPE,
        },
        "Channel": "Web",
    }
