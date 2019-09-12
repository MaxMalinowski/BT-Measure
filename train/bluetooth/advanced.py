import bluetooth
import bluetooth._bluetooth as bt

hci_sock = bt.hci_open_dev()
print(hci_sock)
