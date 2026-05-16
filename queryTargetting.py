#!/usr/bin/env python3

"""

 File: queryTargetting.py
 Author: Dennis Spera

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

qt = list()
sorted_list = list()
for json in jsonFile:
    if json['c'] == 'COMMAND':
       try:
        qt.append({'json':j.dumps(json),'command':json['attr']['command'],'docsExamined':json['attr']['docsExamined'],'nReturned':json['attr']['nreturned'], 'ratio': int(json['attr']['docsExamined']/json['attr']['nreturned'])})

       except:
        pass
       
try:       
  sorted_list = sorted(qt, key=lambda x: x['ratio'], reverse=True)
  for element in sorted_list:
       print('----------------------------------------')
       print(element['json'],"\n")
       print('docsExamined: {0}, nreturned: {1}, query targetting ratio: {2}'.format(element['docsExamined'], element['nReturned'], element['ratio']))
       print('\n')
except:
  print('no queries with "docsExamined" could be found for the date range')
