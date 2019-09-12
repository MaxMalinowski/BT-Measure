import bluetooth
import bluetooth._bluetooth as bt
import struct
import array
import fcntl
import time
import json
import subprocess
import os


class RSSI(object):

    def __init__(self, addr):
        self.addr = addr
        self.hci_sock = bt.hci_open_dev()
        self.hci_fd = self.hci_sock.fileno()
        self.bt_sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
        self.hci_sock.settimeout(10)
        self.connected = False
        self.closed = False
        self.cmd_pkt = None

    def prep_cmd_pkt(self):
        # da fuck is dis ?!
        reqstr = struct.pack(b'6sB17s', bt.str2ba(self.addr), bt.ACL_LINK, b'\0'*17)
        request = array.array('b', reqstr)
        handle = fcntl.ioctl(self.hci_fd, bt.HCIGETCONNINFO, request, 1)
        handle = struct.unpack(b'8xH14x', request.tostring())[0]
        self.cmd_pkt = struct.pack('H', handle)

    def connect(self):
        self.bt_sock.connect((self.addr, 1))
        self.connected = True

    def close(self):
        self.bt_sock.close()
        self.hci_sock.close()
        self.closed = True

    def request_rssi(self):
        try:
            if self.closed:
                return None
            if not self.connected:
                self.connect()

            self.prep_cmd_pkt()
            rssi = bt.hci_send_req(self.hci_sock, bt.OGF_STATUS_PARAM, bt.OCF_READ_RSSI, bt.EVT_CMD_COMPLETE, 4, self.cmd_pkt)
            rssi = struct.unpack('b', rssi[3].to_bytes(1, 'big'))
            return rssi
        except IOError as e:
            print(e)
            self.connected = False
            self.bt_sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
            return None


def main():
    os.system('clear') 

    discover = True
    print('Discovering Bluetooth devices...\n')
    while discover:
        discover = False
        devices = bluetooth.discover_devices()
        if len(devices) > 0: 
            print('Found ' + str(len(devices)) + ' devices')
            
            for address in devices:
                name = bluetooth.lookup_name(address)
                print('|--> ' + str(devices.index(address)+1) + '. Device: "' + str(name) + '" [' + str(address) + ']')

            found = input('\nFound your device? [Y/n] --> ')
            
            if found.startswith('y') or found.startswith('Y') or found == '':
                break
            else:
                print('\nRestarting discovery...')
                discover = True
        else:
            print('No devices found. Restarting discovery...')
            discover = True

    choice = input('Which device do you wish to request the rsi value from? --> ')

    address = devices[int(choice)-1]
    btrssi = RSSI(address)
    value_list = []
    average = 0
    while_count = 0
    try:
        while while_count < 10:
            summ = 0
            count_none = 0
            value = ''
        
            for i in range(100):
                req = btrssi.request_rssi()[0]
                if not (req is None): 
                    summ += req
                else:
                    count_none += 1
        
            if count_none > 50: 
                value = 'No Signal'
            else:
                value = str(summ/(100 - count_none))
                value_list.append(float(value))

            time.sleep(0.5)
            while_count += 1
            print('RSSI [' + address + ']: ' + value)
    finally:
        average = sum(i for i in value_list) / len(value_list)

        json_file = {address: average}
        with open('bt_rssi.json', 'w') as jfile:
            json.dump(json_file, jfile, indent=4)

    print('==> Average RSSI-Value: ' + str(average))
    print('==> Sending values to the tangle...')
    subprocess.call(['node', './send_iota_mam.js', 'bt_rssi.json'])


if __name__ == '__main__':
    main()
