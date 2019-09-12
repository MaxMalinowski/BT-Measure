from gattlib import DiscoveryService

service = DiscoveryService('hci0')
i = 0
while i < 10:
    devices = service.discover(2)
    for address, name in devices.items():
        print(address + name)
    i+= 1
