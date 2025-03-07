#!/usr/bin/env python3

"""

 File: millis.py
 Author: Dennis Spera
 Date: 2024-06-24

 Description: 
  1.) sort durationMillis from mongod.log(s) on stdin from highest durationMillii to lowest.
  2.) usage: {stdin} | millis [-ge {durationMillis}] [-ctx {context}] [-u] 
      a. if context is not specified will match all contexts
      b. take first unique queryHash
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
unique = list()

for line in sys.stdin:
    if is_json(line):
       jsonFile.append( j.loads(line))
sys.stdin.close()

millis = list()
for json in jsonFile:
    if json['c'] == ctx or ctx == '_not_selected_':
       try:
        if int(json['attr']['durationMillis']) >= ge:
           millis.append({'json':j.dumps(json),'milli':json['attr']['durationMillis']})
       except:
        pass
       
deduped = list()
if c.contains_switches('u'):
   for element in millis:
       try:
         _json = j.loads(element['json'])

         if _json['attr']['queryHash'] not in unique:
            unique.append(_json['attr']['queryHash'])
            deduped.append({'json':element['json'],'milli':element['milli']})
       except:
         pass 
   millis = deduped             

try:       
 sorted_list = sorted(millis, key=lambda x: x['milli'], reverse=True)

 for element in sorted_list:
     print(element['json']) 
except:
     sys.stderr.write('No useable data found'+"\n")