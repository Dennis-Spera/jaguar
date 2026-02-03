#!/usr/bin/env python3

"""

 File: cpuPerDatabase.py
 Author: Dennis Spera
 Date: 2026-02-03
 
 Description: 
  1.) calculate the cpu cycles spent on a database by database perspective.

 Change Log:
  1. 2026-02-03 - Initial 

 Testing: 
  1. performed against test datasets performed normally

 Sample Output:

 Database                           CPU Seconds
 ----------------------------------------------
 my-test                            1972.694049
 config                                0.072238
 admin                                 0.062042
 
"""

import json, sys
from collections import Counter
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

cpuCycles = list()
sorted_list = list()
for json in jsonFile:
    if json['c'] == 'COMMAND':
       try:
        cpuCycles.append({'json':j.dumps(json),'cpuCycles':json['attr']['cpuNanos'],'db':json["attr"]["command"]["$db"]})
       except:
        pass

# Sum cpuNanos per database
db_cpu_totals = {}
for entry in cpuCycles:
    db = entry['db']
    cpu_nanos = entry['cpuCycles']
    if db in db_cpu_totals:
        db_cpu_totals[db] += cpu_nanos
    else:
        db_cpu_totals[db] = cpu_nanos

# Convert to seconds and sort by cpuNanos
db_cpu_seconds = [(db, nanos / 1000000000) for db, nanos in db_cpu_totals.items()]
sorted_db_cpu = sorted(db_cpu_seconds, key=lambda x: x[1], reverse=True)

# Print results
print(f"{'Database':<30} {'CPU Seconds':>15}")
print("-" * 46)
for db, cpu_seconds in sorted_db_cpu:
    print(f"{db:<30} {cpu_seconds:>15.6f}") 
