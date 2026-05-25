#!/usr/bin/env python3

"""

 File: formatOne.py
 Author: Dennis Spera
 Date: 2024-06-24
 Description: 
  1.) concise format(1) of mongod.log(s) on stdin.

 Change Log:
  1. 2024-06-24 - Initial
  2. 2024-07-13 - Add additional error checking and global help fucntion

 Testing: 
  1. Not defined
"""

import json, sys
from collections import Counter
import json as j

use_legacy_output = ('--legacy' in sys.argv) or ('-l' in sys.argv)

def is_json(json):
    try:
        j.loads(json)
    except ValueError:
        return False
    return True

jsonFile = list()

for line in sys.stdin:
  if is_json(line):
     try:
       jsonFile.append( j.loads(line))
     except:
       pass
  
sys.stdin.close()

formatted = list()
for json in jsonFile:
    if json['c'] == 'COMMAND':

        print("-----------------------------------------------------------------------------------------------------")
        print("")
        try: print("{:<20} {:<1} {:>0}".format('Submission Time ', '=', json['t']['$date']))
        except: pass
        attr = json.get('attr', {})

        if use_legacy_output:
          try: print("{:<20} {:<1} {:>0}".format('command ', '=', str(attr['command'])))
          except: pass
          try: print("{:<20} {:<1} {:>0}".format('originatingCommand ', '=', str(attr['originatingCommand'])))
          except: pass

          try: print("{:<20} {:<1} {:>0}".format('ns|name space ', '=', str(attr['ns'])))
          except: pass
          try: print("{:<20} {:<1} {:>0}".format('planSummary ', '=', attr['planSummary']))
          except: pass
          try: print("{:<20} {:<1} {:>0}".format('keysExamined ', '=', attr['keysExamined']))
          except: pass
          try: print("{:<20} {:<1} {:>0}".format('docsExamined ', '=', attr['docsExamined']))
          except: pass

          try: print("{:<20} {:<1} {:>0}".format('queryHash ', '=', attr['queryHash']))
          except: pass
          try: print("{:<20} {:<1} {:>0}".format('queryShapeHash ', '=', attr['queryShapeHash']))
          except: pass

          try: print("{:<20} {:<1} {:>0}".format('appName ', '=', attr['appName']))
          except: pass

          try: print("{:<20} {:<1} {:>0}".format('hasSortStage ', '=', attr['hasSortStage']))
          except: pass

          try: print("{:<20} {:<1} {:>0}".format('planningTimeMicros ', '=', attr['planningTimeMicros']))
          except: pass
          try: print("{:<20} {:<1} {:>0}".format('queryFramework ', '=', attr['queryFramework']))
          except: pass

          try: print("{:<20} {:<1} {:>0}".format('locks ', '=', str(attr['locks'])))
          except: pass
          try: print("{:<20} {:<1} {:>0}".format('reslen ', '=', str(attr['reslen'])))
          except: pass
          try: print("{:<20} {:<1} {:>0}".format('nBatches ', '=', str(attr['nBatches'])))
          except: pass

          try: print("{:<20} {:<1} {:>0}".format('readConcern ', '=', str(attr['readConcern'])))
          except: pass
          try: print("{:<20} {:<1} {:>0}".format('writeConcern ', '=', str(attr['writeConcern'])))
          except: pass
          try: print("{:<20} {:<1} {:>0}".format('$readPreference ', '=', str(attr['$readPreference'])))
          except: pass
          try: print("{:<20} {:<1} {:>0}".format('$writePreference ', '=', str(attr['$writePreference'])))
          except: pass

          try: print("{:<20} {:<1} {:>0}".format('numYields ', '=', attr['numYields']))
          except: pass
          try: print("{:<20} {:<1} {:>0}".format('nreturned  ', '=', attr['nreturned']))
          except: pass
          try: print("{:<20} {:<1} {:>0}".format('durationMillis ', '=', attr['durationMillis']))
          except: pass

          try:
            seconds = round(int(attr['cpuNanos']) / 1000000000,2)
            print("{:<20} {:<1} {:>0}".format('cpuNanos', '=', str(attr['cpuNanos']) + " (" + str(seconds) + " seconds)"))
          except: pass

          try: print("{:<20} {:<1} {:>0}".format('remote ', '=', attr['remote']))
          except: pass
          try: print("{:<20} {:<1} {:>0}".format('bytesRead ', '=', attr['storage']['data']['bytesRead']))
          except: pass

          print("-----------------------------------------------------------------------------------------------------\n")
        else:
          if attr.get('command') is not None:
            print("```json")
            print("Command = " + j.dumps(attr.get('command'), separators=(',', ':')))
            print("```")
            print("")

          if attr.get('originatingCommand') is not None:
            print("```json")
            print("Originating Command = " + j.dumps(attr.get('originatingCommand'), separators=(',', ':')))
            print("```")
            print("")

          def print_row(label, value):
            if value is None:
              return
            safe_value = str(value).replace("|", "\\|")
            print(f"| {label} | {safe_value} |")

          print("| Metric | Value |")
          print("| --- | --- |")

          print_row('ns|name space', attr.get('ns'))
          print_row('planSummary', attr.get('planSummary'))
          print_row('keysExamined', attr.get('keysExamined'))
          print_row('docsExamined', attr.get('docsExamined'))
          print_row('queryHash', attr.get('queryHash'))
          print_row('queryShapeHash', attr.get('queryShapeHash'))
          print_row('appName', attr.get('appName'))
          print_row('hasSortStage', attr.get('hasSortStage'))
          print_row('planningTimeMicros', attr.get('planningTimeMicros'))
          print_row('queryFramework', attr.get('queryFramework'))
          print_row('locks', attr.get('locks'))
          print_row('reslen', attr.get('reslen'))
          print_row('nBatches', attr.get('nBatches'))
          print_row('readConcern', attr.get('readConcern'))
          print_row('writeConcern', attr.get('writeConcern'))
          print_row('$readPreference', attr.get('$readPreference'))
          print_row('$writePreference', attr.get('$writePreference'))
          print_row('numYields', attr.get('numYields'))
          print_row('nreturned', attr.get('nreturned'))
          print_row('durationMillis', attr.get('durationMillis'))

          cpu_nanos = attr.get('cpuNanos')
          if cpu_nanos is not None:
            try:
              seconds = round(int(cpu_nanos) / 1000000000, 2)
              print_row('cpuNanos', f"{cpu_nanos} ({seconds} seconds)")
            except:
              print_row('cpuNanos', cpu_nanos)

          print_row('remote', attr.get('remote'))
          print_row('bytesRead', attr.get('storage', {}).get('data', {}).get('bytesRead'))

       
