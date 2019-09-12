import json
from bluetooth import *

try:
    j = 0
    data = {}
    res = find_service()
except Error as e:
    print(e)
else:
    for i in res:
        data[str('service' + str(j))] = i
        print(i)
        j += 1
    with open('found_services.json', 'w') as jfile:
        json.dump(data, jfile, indent=4, sort_keys=True)
