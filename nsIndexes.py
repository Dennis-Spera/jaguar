#!/usr/bin/env python3

"""

 File: nsIndexes.py
 Author: Dennis Spera
 Date: 2024-06-24
 Description: 
  1.) list indexes by namespace for mongod.log(s) read on stdin.

 Change Log:
  1. 2024-06-24 - Initial
  2. 2024-07-13 - Add additional error checking and global help fucntion

 Testing: 
  1. Not defined
"""

import json, sys
import json as j
from collections import Counter
import re as regex

def is_json(json):
    try:
        j.loads(json)
    except ValueError:
        return False
    return True

jsonFile = list()

for line in sys.stdin:
  try:
    if is_json(line):
       jsonFile.append( j.loads(line))
  except:
    pass
  
sys.stdin.close()
nsIndexes = list()
sorted_list = list()
for json in jsonFile:
    if json['c'] == 'COMMAND':         
        try:
           if not regex.match(r"(.*)(COLLSCAN)(.*)", json['attr']['planSummary']):   
              nsIndexes.append({'ns':str(json['attr']['ns']),'index':json['attr']['planSummary']})
        except: pass
        
        try: sorted_list = sorted(nsIndexes, key=lambda x: x['ns'], reverse=True)
        except:pass
        
print('**Index Aggregations**',"\n")

print("{:<40}  {:<60}  {:>10} ".format('Name Space', 'Index', 'Count'))
print("{:<40}  {:<60}  {:>10} ".format('----------------------------------------', '----------------------------------------', '----------'))

unique_counts = Counter(tuple(d.items()) for d in sorted_list)

for unique_dict, count in unique_counts.items():
    print("{:<40}  {:<60}  {:>10} ".format(dict(unique_dict)['ns'], dict(unique_dict)['index'], count))

      
