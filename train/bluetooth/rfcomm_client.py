from bluetooth import *

server_address = 'ENTER-YOUR-MAC-ADDRESS-HERE'
port  = 1

sock = BluetoothSocket(RFCOMM)
sock.connect((server_address, port))

sock.send('Hello World!')
sock.close()
