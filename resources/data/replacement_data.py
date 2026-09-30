from core.common import BaseRandomizer


def get_init_product_inspection_json(consumer, device, sale_point='MS269762'):
    return {
        'Consumer': {
            '$type': 'PMI.BDDM.Staticdata.UserReference',
            'Code': consumer,
            'CodeSpace': 'RRPSF',
        },
        'EquipmentProductInstance': {
            '$type': 'PMI.BDDM.Staticdata.EquipmentProductInstanceReference',
            'Code': device,
            'CodeSpace': 'RRPSF',
        },
        'SalePoint': {
            '$type': 'PMI.BDDM.Staticdata.DigitalPOSReference',
            'Code': sale_point,
            'CodeSpace': 'MDM',
        },
        'Channel': 'Web',
    }


def get_product_inspection_result_json(request, inspection, survey_result):
    return {
        'Survey': survey_result,
        'ConsumerRequest': {
            '$type': 'PMI.BDDM.Transactionaldata.ConsumerProductInspectionRequestReference',
            'Code': request,
            'CodeSpace': 'B2CCRM',
        },
        'ProductInspection': {
            '$type': 'PMI.BDDM.Transactionaldata.ProductInspectionReference',
            'Code': inspection,
            'CodeSpace': 'B2CCRM',
        },
        'Channel': 'Web',
    }


def get_retail_replacement_order_json(
        request,
        created_by='PMRU\\svcUatBitrix',
        sale_point='MS269762',
        product_code='BV004732',
        product_name='Комплект lil SOLID 3.0, Космический черный',
        item_code=None,
        fulfillment_type='POSSelfPickUp',
):
    if item_code is None:
        item_code = f'ITMCD-{BaseRandomizer().randint(1, 9999)}'

    return {
        'ReplacementOrder': {
            '$type': 'PMI.BDDM.Transactionaldata.RetailReplacementOrder',
            'CreatedBy': {
                '$type': 'PMI.BDDM.Staticdata.ADUserReference',
                'Code': created_by,
                'CodeSpace': 'ActiveDirectory',
            },
            'DeliveryInfo': {
                'CourierCompany': {
                    'Code': 'CDEK',
                    'Name': 'BCP_ZaberySam2',
                },
                'DeliveryTimeZone': 'UTC+03:00',
                'DeliveryType': 'Standard',
                'DeliveryPoint': {
                    'KLADR': '7700000000006180001',
                    'Address': {
                        'AddressLine': 'Цветной б-р, д 2',
                        'City': 'Москва',
                        'Country': 'Россия',
                        'ZipCode': '127051',
                    },
                },
            },
            'SourcePoint': {
                '$type': 'PMI.BDDM.Staticdata.POSReference',
                'Code': sale_point,
                'CodeSpace': 'MDM',
                'Name': 'WEB',
            },
            'ProvidedItems': [
                {
                    'ItemCode': item_code,
                    'Product': {
                        '$type': 'PMI.BDDM.Staticdata.BrandVariantReference',
                        'Code': product_code,
                        'CodeSpace': 'MDM',
                        'Name': product_name,
                    },
                    'Quantity': {
                        'UOM': 'Piece',
                        'Value': 1,
                    },
                },
            ],
        },
        'ConsumerRequest': {
            '$type': 'PMI.BDDM.Transactionaldata.ConsumerProductInspectionRequest',
            'Code': request,
            'CodeSpace': 'B2CCRM',
            'FulfillmentType': fulfillment_type,
        },
        'Channel': 'Web',
    }
