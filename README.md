# RSSI Scanner

Scanner getting the rssi values of Bluetooth / BLE devices

## Installation

````bash
sudo python3 setup.py install
sudo npm install .
````

## Usage

All source code files are lying in the src folder.

To scan for bluetooth devices use the bluetooth_rssi.py script.
````bash
sudo python3 bluetooth_rssi.py
````

To scan for ble devices use the ble_rssi.py scipt.
````bash
sudo python3 ble_rssi.py
````

If wished, to set a device in advertising mode (e.g. to verify) execute the command.
````bash
sudo hciconfig hci0 leadv
````

Directly on the commandline this can be used to verify or gain more insight
````bash
sudo hcidump --raw
sudo hcidump --raw -X
# used be the ble_rssi.py script
sudo btmon
````

As an experimental feature, the scan results can be sent to an iota address or to a private mam stream.
Use for this purpose the send_/ fetch_iota_mam.js scripts or the send_iota_mam.js script.
````bash
# using the mam stream
node send_iota_mam.js [json-file]
node fetch_iota_mam.js [root-address]

# using an addressa and wallet
node send_iota_msg.js [json-file]
````

The iota scipts can also be executed automatically in the python scripts. Just uncomment the specific lines.

For further information about iota see https://docs.iota.org/
