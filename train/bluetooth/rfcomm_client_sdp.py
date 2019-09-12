import sys
from bluetooth import *

service_matches = find_service(name='Bluetooth Serial Port', uuid=SERIAL_PORT_CLASS)

if(len(service_matches) == 0):
    print('Couldn`t find any service!')
    sys.exit(0)

first_match = service_matches[0]
port = first_match['port']
name = first_match['name']
host = first_match['host']

print('Connection to' + host)

sock = BluetoothSocket(RFCOMM)
sock.connect((host, port))
sock.send('hello')
sock.close()
