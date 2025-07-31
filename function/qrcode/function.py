"""
Name: qrcode
Description: QR Code UUID Generator
Parameters: uuid
"""

import os.path
import json
import segno

def functioncall(uuid):
    qrcode_file = 'static/function/qrcode/' + str(uuid) + '.png'
    qr_exist = os.path.isfile(qrcode_file)
    if qr_exist == False:
        with open('function/qrcode/config.json', 'r') as file:
            data = json.load(file)
        qr_code = segno.make_qr(uuid)
        #qr_code.save(qrcode_file, scale = 10, border = 1, light = 'white', dark = 'black', quiet_zone = 'white', data_dark = 'black', data_light = 'black')
        qr_code.save(qrcode_file,
                     scale = data['scale'],
                     border = data['border'],
                     light = data['light'],
                     dark = data['dark'],
                     quiet_zone = data['quiet_zone'],
                     data_dark = data['data_dark'],
                     data_light = data['data_light']
                )
    output = '<a href="/' + str(qrcode_file) + '" target="_new"><img src="/' + str(qrcode_file) + '" alt="QR" width="20"></a>'
    return output

