#!/usr/bin/env python3

"""

 File: collscans.py
 Author: Dennis Spera
 Date: 2024-06-24
 Description: 
  1.) list collection scans by namespace for mongod.log(s) read on stdin.
 Change Log:
  1. 2024-06-24 - Initial 
  2. 2024-07-17 - reworded comments, removed unused modules

 Testing: 
  1. Not defined
"""

import json, sys
import json as j
import re as regex

jsonFile = list()

for line in sys.stdin:
  try:
    jsonFile.append( j.loads(line))
  except:
    pass
sys.stdin.close()

for json in jsonFile:
    if json['c'] == 'COMMAND':         
        try:
           if regex.match(r"(.*)(COLLSCAN)(.*)", json['attr']['planSummary']):   
              print(j.dumps(json))
        except: pass
        
      
