#!/usr/bin/env python3

"""

 File: ns.py
 Author: Dennis Spera
 Date: 2024-06-24
 Description: 
  1.) sort by namespace from mongod.log(s) on stdin.

 Change Log:
  1. 2024-06-24 - Initial 
  2. 2024-07-17 - reworded comments, removed unused modules

 Testing: 
  1. Not defined
"""

import json, sys
import json as j

def is_json(json):
    try:
        j.loads(json)
    except ValueError:
        return False
    return True

jsonFile = list()

for line in sys.stdin:
    if is_json(line):
       jsonFile.append( j.loads(line))
sys.stdin.close()

ns = list()
for json in jsonFile:
    if json['c'] == 'COMMAND':
       try:
        ns.append({'json':j.dumps(json),'ns':json['attr']['ns']})
       except:
        pass
       
sorted_list = sorted(ns, key=lambda x: x['ns'], reverse=True)

for element in sorted_list:
    print(element['json']) 
