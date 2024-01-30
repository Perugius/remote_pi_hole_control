from pn532 import *
import time
import requests
import json

lookup_action = ['status', 'enable', 'disable']

# nfc init
pn532 = PN532_I2C(debug=False, reset=20, req=16)
ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
pn532.SAM_configuration()
print('Waiting for RFID/NFC card...')


def nfc_read():
    uid = pn532.read_passive_target(timeout=0.01)
    # Try again if no card is available.
    if uid is None:
        return
    return [hex(i) for i in uid]


def pi_hole_control(action):
    url = "http://192.168.1.106/admin/api.php?" + lookup_action[action] + "=300&auth=7d672902bb13cd1f10cae707022df2d90ba4a8c0771686ac73a02b30a0581966"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = json.loads(response.text)
            status_value = data["status"]
            return status_value

        else:
            return ("Unable to fetch")
    except:
        return "error"


while (True):

    #read nfc, if its read check for current status and swap to opposite status
    if nfc_read():
        current_status = pi_hole_control(0)
        print("changed!")
        if current_status == 'enabled':
            pi_hole_control(2)
        elif current_status == 'disabled':
            pi_hole_control(1)
    print(pi_hole_control(0))
    time.sleep(1)
