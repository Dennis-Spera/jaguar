#!/usr/bin/env python3

"""

 File: cpuc.py
 Author: Dennis Spera
 Date: 2024-12-07

 Description: 
  1.) sort cpuNanos from mongod.log(s) on stdin from highest cpuNanos to lowest.
  2.) usage: {stdin} | cpuc -ge {cpuNanos} [-ctx {context}] 
      a. if context is not specified will match all contexts

 Change Log:
  1. 2024-06-24 - Initial 
  2. 2024-07-14 - Additional error checking

 Testing: 
  1. Not defined

"""

import json, sys
import json as j
from commandlines import Command as cmd

def is_json(json):
    try:
        j.loads(json)
    except ValueError:
        return False
    return True

ge = int()
c = cmd()
try:
 ge = int(c.get_definition('ge')) 
except:
 ge = int(0)

try:
 ctx = (c.get_definition('ctx')).upper() 
except:
 ctx = '_not_selected_'

jsonFile = list()

for line in sys.stdin:
    if is_json(line):
       jsonFile.append( j.loads(line))
sys.stdin.close()

cpuNanos = list()
for json in jsonFile:
    if json['c'] == ctx or ctx == '_not_selected_':
       try:
        if int(json['attr']['cpuNanos']) >= ge:
           cpuNanos.append({'json':j.dumps(json),'cpuNanos':json['attr']['cpuNanos']})
       except:
        pass

try:       
 sorted_list = sorted(cpuNanos, key=lambda x: x['cpuNanos'], reverse=True)

 for element in sorted_list:
     print(element['json']) 
except:
     sys.stderr.write('No useable data found'+"\n")