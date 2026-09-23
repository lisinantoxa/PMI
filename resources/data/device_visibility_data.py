def get_hide_device_json(consumer, device, sale_point='MS269762'):
    return {
        'SalePoint': {
            '$type': 'PMI.BDDM.Staticdata.DigitalPOSReference',
            'Code': sale_point,
            'CodeSpace': 'MDM'
        },
        'Consumer': {
            'Code': consumer,
            'CodeSpace': 'B2CCRM'
        },
        'EquipmentProductInstance': {
            '$type': 'PMI.BDDM.Staticdata.EquipmentProductInstanceReference',
            'CodeSpace': 'DeviceManagement',
            'Code': device
        },
        'Channel': 'Web'
    }
