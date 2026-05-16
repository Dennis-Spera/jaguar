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

import json
import sys
from commandlines import Command as cmd

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

millis = list()
unique = set()
use_unique = c.contains_switches('u')

for line in sys.stdin:
    try:
        payload = json.loads(line)
    except ValueError:
        continue

    if payload['c'] != ctx and ctx != '_not_selected_':
        continue

    try:
        duration = int(payload['attr']['durationMillis'])
    except:
        continue

    if duration < ge:
        continue

    if use_unique:
        try:
            query_hash = payload['attr']['queryHash']
        except:
            continue

        if query_hash in unique:
            continue

        unique.add(query_hash)

    millis.append({'json': json.dumps(payload), 'milli': duration})

sys.stdin.close()

try:       
 sorted_list = sorted(millis, key=lambda x: x['milli'], reverse=True)

 for element in sorted_list:
     print(element['json']) 
except:
     sys.stderr.write('No useable data found'+"\n")