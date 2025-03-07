#!/usr/bin/env python3

"""

 File: drivers.py
 Author: Dennis Spera
 Date: 2024-06-24
 Description: 
  1.) Extract driver totals from mongod.log on stdin.
 Change Log:
  1. 2024-06-24 - Initial 

 Testing: 
  1. Not defined

"""

import json as j, sys
from collections import Counter

def is_json(json):
    try:
        j.loads(json)
    except ValueError:
        return False
    return True

jsonFile = list()

for line in sys.stdin:
    if is_json(line):
       data = j.loads(line)
       jsonFile.append(data)

sys.stdin.close()

drivers = list()
for json in jsonFile:
    if json['c'] == 'NETWORK':
       try:
        drivers.append({json['attr']['doc']['driver']['name']+' <version> '+json['attr']['doc']['driver']['version']:1})
       except:
        pass    

result = Counter(key for d in drivers for key in d)
sorted_result = dict(sorted(result.items(), key=lambda x: x[1], reverse=True))

print("{:>10}   {:<10}".format('Count', 'Driver'))
print("{:>10}   {:<10}".format('-----', '----------------------'))

for k,v in sorted_result.items():

    print("{:>10}   {:<10}".format(v, k))