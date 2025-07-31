"""
Name: barcode
Description: Barcode UUID Generator
Parameter: uuid
"""

import os.path
from io import BytesIO
from barcode import Code128
from barcode.writer import ImageWriter

def functioncall(uuid):
    barcode_file = 'static/function/barcode/' + str(uuid) + '.png'
    bc_exist = os.path.isfile(barcode_file)
    if bc_exist == False:
        with open(barcode_file, "wb") as f:
            Code128(uuid, writer=ImageWriter()).write(f)
    output = '<a href="/' + str(barcode_file) + '" target="_new"><img src="/' + str(barcode_file) + '" alt="UUID Barcode" width="20"></a>'
    return output

