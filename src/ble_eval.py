import json
import os
from matplotlib.pyplot import scatter, show, plot, subplot, title, xlabel, ylabel, savefig, legend

addr = {}

os.system('ls -l ./results/')
name = input('input name to evaluate: ')


with open('./results/' + str(name)) as json_file:
    data = json.load(json_file)
    for key in data.keys():
       try:
           address = data[key]['Address'][:data[key]['Address'].find(' ')]
           tmp_rssi = float(data[key]['RSSI'][:data[key]['RSSI'].find(' ')])
           tmp_time = float(key[key.rfind(' ')+1:len(key)-2])
           rssi = tmp_rssi
           time = tmp_time
       except:
           print('')
       finally:
           if address not in addr.keys():
              addr[address] = []
              addr[address].append((time, rssi))
           else:
              addr[address].append((time, rssi))


print('How do you want to analyze the data?\n\t1. draw all discoverd addresses\n\t2  draw addresses with more then 50 responses\n\t3. draw every address on its own\n\t4. draw specific address\n')
choice = input('')

if choice is  '1':  
    for key in addr.keys():
        x, y = zip(*addr[key])
        plot(x, y, label=key)
    title('ble')
    xlabel('time')
    ylabel('rssi')
    legend(bbox_to_anchor=(1, 1), loc='upper left')
    show()
elif choice is  '2':   
    for key in addr.keys():
        if len(addr[key]) > 50:
            x, y = zip(*addr[key])
            plot(x, y, label=key)
    title('ble')
    xlabel('time')
    ylabel('rssi')
    legend(bbox_to_anchor=(1, 1), loc='upper left')
    show()
elif choice is '3':   
    for key in addr.keys():
            x, y = zip(*addr[key])
            plot(x, y, label=key)
            title('ble')
            xlabel('time')
            ylabel('rssi')
            legend(bbox_to_anchor=(1, 1), loc='upper left')
            show()
elif choice is '4':  
    for key in addr.keys():
        print(str(list(addr.keys()).index(key)) + '. ' + str(key))
    add_choice = input('Enter number of desired address: ')
    x, y = zip(*addr[list(addr.keys())[int(add_choice)]])
    plot(x, y, label=addr[list(addr.keys())[int(add_choice)]])
    title('ble')
    xlabel('time')
    ylabel('rssi')
    legend(bbox_to_anchor=(1, 1), loc='upper left')
    show()
else:
    print ('ups, you messed up :D')

