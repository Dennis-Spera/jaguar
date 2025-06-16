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

        try: print("{:<20} {:<1} {:>0}".format('Submission Time ', '=', json['t']['$date']))
        except: pass
        try: print("{:<20} {:<1} {:>0}".format('command ', '=', str(json['attr']['command'])))
        except: pass

        print("\n")

        try: print("{:<20} {:<1} {:>0}".format('ns|name space ', '=', str(json['attr']['ns'])))
        except: pass
        try: print("{:<20} {:<1} {:>0}".format('planSummary ', '=', json['attr']['planSummary']))
        except: pass
        try: print("{:<20} {:<1} {:>0}".format('keysExamined ', '=', json['attr']['keysExamined']))
        except: pass
        try: print("{:<20} {:<1} {:>0}".format('docsExamined ', '=', json['attr']['docsExamined']))
        except: pass
        
        try: print("{:<20} {:<1} {:>0}".format('queryHash ', '=', json['attr']['queryHash']))
        except: pass
        try: print("{:<20} {:<1} {:>0}".format('queryShapeHash ', '=', json['attr']['queryShapeHash']))
        except: pass

        try: print("{:<20} {:<1} {:>0}".format('planningTimeMicros ', '=', json['attr']['planningTimeMicros']))
        except: pass
        try: print("{:<20} {:<1} {:>0}".format('queryFramework ', '=', json['attr']['queryFramework']))
        except: pass

        try: print("{:<20} {:<1} {:>0}".format('locks ', '=', str(json['attr']['locks'])))
        except: pass        

        try: print("{:<20} {:<1} {:>0}".format('reslen ', '=', str(json['attr']['reslen'])))
        except: pass        

        try: print("{:<20} {:<1} {:>0}".format('readConcern ', '=', str(json['attr']['readConcern'])))
        except: pass  
        try: print("{:<20} {:<1} {:>0}".format('writeConcern ', '=', str(json['attr']['writeConcern'])))
        except: pass

        try: print("{:<20} {:<1} {:>0}".format('$readPreference ', '=', str(json['attr']['$readPreference'])))
        except: pass  
        try: print("{:<20} {:<1} {:>0}".format('$writePreference ', '=', str(json['attr']['$writePreference'])))
        except: pass

        try: print("{:<20} {:<1} {:>0}".format('numYields ', '=', json['attr']['numYields']))
        except: pass
        try: print("{:<20} {:<1} {:>0}".format('nreturned  ', '=', json['attr']['nreturned']))
        except: pass 
        try: print("{:<20} {:<1} {:>0}".format('durationMillis ', '=', json['attr']['durationMillis']))       
        except: pass 

        try: 
          seconds = round(int(json['attr']['cpuNanos']) / 1000000000,2)
          print("{:<20} {:<1} {:>0}".format('cpuNanos', '=', str(json['attr']['cpuNanos']) + " (" + str(seconds) + " seconds)"))       
        except: pass 


        try: print("{:<20} {:<1} {:>0}".format('remote ', '=', json['attr']['remote']))
        except: pass 
        try: print("{:<20} {:<1} {:>0}".format('bytesRead ', '=', json['attr']['storage']['data']['bytesRead']))
        except: pass 

        print("-----------------------------------------------------------------------------------------------------\n")

       
