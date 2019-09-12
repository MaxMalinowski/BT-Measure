import json
from bluetooth import *

devices = discover_devices()
print('Found ' + str(len(devices)) + ' devices')
data = {}

for address in devices:
    name = lookup_name(address)
    data[address] = name
    # print('Found device ' + name + ' [' + address + ']')

with open('found_devices.json', 'w') as jfile:
    json.dump(data, jfile)
