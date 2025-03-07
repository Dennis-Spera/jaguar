#!/usr/bin/env python3

"""

 File: queryHash.py
 Author: Dennis Spera
 Date: 2024-06-24
 Description: 
  1.) Aggregate the count of query shapes.

 Change Log:
  1. 2024-06-24 - Initial 

 Testing: 
  1. Not defined
"""

from collections import Counter, OrderedDict
import sys, re
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

queryHash = list()
queryHashCmd = list()
for json in jsonFile:
    if json['c'] == 'COMMAND':
      try:
        queryHash.append(json['attr']['queryHash'])        
        queryHashCmd.append({json['attr']['queryHash']:json['attr']['command']})
      except:
       pass

queryHashTotals = dict(Counter(queryHash))
sortedByKey = OrderedDict(sorted(queryHashTotals.items()))
sortedByValue = {k: v for k, v in sorted(queryHashTotals.items(), key=lambda item: item[1], reverse=True)}

print("{:>10}   {:<10}   {:<10}".format('Count', 'queryHash', 'command'))
print("{:>10}   {:<10}   {:<10}".format('-----', '---------','------------------------'))

def getCommand(qh):
  for d in queryHashCmd: 
      for k,v in d.items():
          if k == qh:
             return(v)
  
for k,v in sortedByValue.items():
    print("{:>10}   {:<10}".format(v, k),end='')    
    print(str(getCommand(k))[0:150],' ....')