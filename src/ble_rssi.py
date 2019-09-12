import subprocess
import multiprocessing
import time
import os
import json
import sys
import re

from datetime import datetime

class BleRssi:

    def __init__(self):
        # Save current time for file names
        self.time_ms = time.time()
        # All Events registered from btmon
        self.hci_events = {}
        # All found addresses without duplicates
        self.addresses = []
        # All addresses with their rssi values
        self.rssis = {}

    def discovery(self, scan_time=10):
        # Create file to which write the btmon output
        log = open('btmon_dump.txt', 'w')
        # First start btmon, then hcitool lescan
        btmon = subprocess.Popen(['sudo', 'btmon'], stdout=log, stderr=subprocess.STDOUT)
        lescan = subprocess.Popen(['sudo', 'hcitool', 'lescan', '--duplicates'],
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            # Give the processes time to run and collect data
            lescan.wait(timeout=int(scan_time))
            btmon.wait(timeout=int(scan_time))
        except subprocess.TimeoutExpired:
            # When given Timeout expired, kill the processes
            try:
                subprocess.check_call(['sudo', 'kill', '9', str(lescan.pid)])
                subprocess.check_call(['sudo', 'kill', str(btmon.pid)])
            except subprocess.CalledProcessError:
                print('', end='')

    def parse_events(self):
        # parse the data form the btmon output file into a dictionary
        key = ''
        append = False
        btfile = open('btmon_dump.txt')
        for number, line in enumerate(btfile):
            if str(line).startswith('>' or '<' or '@'):
                # Key line / Header of an Event
                if str(line).startswith('> HCI Event: LE Meta Event'):
                    # Header of an searched event -> Add as key to dict
                    key = line
                    self.hci_events[key] = {}
                    append = True
                else:
                    # no interessted in this header or it's information
                    append = False
            elif append:
                # Preceding header was interesting, so add the succeeding data as key-value pairs to the dict
                # But only when there are key and values
                if ':' in line:
                    line = line.strip()
                    sec_key, sec_value = line[:line.find(':')], line[line.find(':')+2:]
                    self.hci_events[key][sec_key] = sec_value
                    if sec_key == 'Address' and sec_value not in self.addresses:
                        # if key value pair is an address, add also to address list
                        self.addresses.append(sec_value[:sec_value.find(' ')])

        # Remove duplicates of addresses
        self.addresses = list(dict.fromkeys(self.addresses))

        # Export the LE Events to a json file
        with open('./results/ble_dump_' + str(self.time_ms) + '.json', 'w') as jsble:
            json.dump(self.hci_events, jsble, indent=4)

        # Remove btmon.txt file
        os.remove('btmon_dump.txt')

    def extract_rssi(self, add):
        # Go though the keys and extract the Address and RSSI value if both are in the values
        for key in self.hci_events.keys():
            if 'Address' and 'RSSI' in self.hci_events[key].keys():
                if self.hci_events[key]['Address'][:self.hci_events[key]['Address'].find(' ')] == add:
                    self.rssis[add].append(int(self.hci_events[key]['RSSI'][:self.hci_events[key]['RSSI'].find(' ')]))

    def parse_rssi(self, specific=None):
        # get the rssi values
        if specific is None:
            # if no argument is provided, we get the values for all addresses discovered
            for address in self.addresses:
                self.rssis[address] = []
                self.extract_rssi(address)
        else:
            # if an address is specified, we only get the values for this address
            self.rssis[specific] = []
            self.extract_rssi(specific)


def wrong_usage():
    print('Wrong arguments supplied!\n')
    print('Usage: ble_rssi.py [Duration] [Address]')
    print('\t[Duration]\tHow long do you want to scan for devices and gather information (default: 10s)')
    print('\t[Address]\tSpecific address you want to gather information about '
          '(default: you gather information about all discoverd devices)')
    sys.exit(1)


def arguments():
    arg_len = len(sys.argv)
    address = ''
    duration = ''
    # Check how much & what arguments have been supplied
    if arg_len == 2:
        arg1 = sys.argv[1]
        if re.match('([0-9a-fA-F]:?){12}', arg1):
            address = arg1
        elif re.match('^[1-9]+', arg1):
            duration = int(arg1)
        else:
            wrong_usage()
    elif arg_len == 3:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        if re.match('([0-9a-fA-F]:?){12}', arg1):
            address = arg1
            duration = int(arg2)
        elif re.match('([0-9a-fA-F]:?){12}', arg2):
            address = arg2
            duration = int(arg1)
        else:
            wrong_usage()
    elif arg_len > 3:
        wrong_usage()

    return address, duration


def main():
    os.system('clear')
    discover = True
    bt = BleRssi()
    address, duration = arguments()
    print('Discovering ble devices...\n')
    try:
        discover = False
        # Run discovery
        if duration != '':
            bt.discovery(duration)
        else:
            bt.discovery()

        # Parse gathered data
        bt.parse_events()

        if address == '':
            print('Found ' + str(len(bt.addresses)) + ' ble devices!')
            for add in bt.addresses:
                print('|--> ' + str(bt.addresses.index(add)+1) + '. [' + add + ']')

        else:
            found = False
            for add in bt.addresses:
                if add == address:
                    found = True
                    break
            if found:
                print('Found ble device [' + address + ']')
                print('|--> 1. [' + address + ']')
            else:
                print('Ble device [' + address + '] not found! Exiting!')
                exit(1)

        choice = input('\nWhich device do you wish to request the rsi value from? --> ')
        # Parse desired rssi values
        if address == '' and choice == '':
            bt.parse_rssi()
        elif address == '' and choice != '':
            bt.parse_rssi(bt.addresses[int(choice)-1])
        else:
            bt.parse_rssi(address)

        result = {}
        # print rssi values
        for add in bt.rssis.keys():
            print(str(list(bt.rssis.keys()).index(add)+1) + '. [' + add + ']', end='')
            if address != '' or choice != '':
                for rssi in bt.rssis[add]:
                    print('\n\t#' + str(rssi) + '', end='')
            rssi_sum = sum(bt.rssis[add])/len(bt.rssis[add])
            # Send Anonymised rssi values to the tangle
            # result['##:##:##:##:##:##'] = round(rssi_sum)
            # Send addresses in plain to the tangle
            result['[' + add + ']'] = round(rssi_sum)
            print('\t==> Average RSSI-Value:' + str(round(rssi_sum)))

        with open('./results/ble_result_' + str(bt.time_ms) + '.json', 'w') as jfile:
            json.dump(result, jfile, indent=4)

    finally:
        # Clean up not so properly to avoid conflicts on next usage
        os.system('sudo hciconfig hci0 down')
        time.sleep(1)
        os.system('sudo hciconfig hci0 up')
        time.sleep(1)

        # Send transaction to the tangle
        # subprocess.call(['node', 'send_iota_msg.js', 'ble_result.json'])

        # Send private mam stream
        # subprocess.call(['node', 'send_iota_mam.js', 'ble_result.json'])


if __name__ == '__main__':
    main()
