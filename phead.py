#!/usr/bin/env python3

"""

 File: pread.py
 Author: Dennis Spera
 Date: 2024-06-24
 Description: 
  1.) perform the sames as the linux head command. Since the linux head command sends a $SIGTERM
      to the reader, python functions need a specific way to emulate this function.
  2.) default is 6 records, this can be overridden by -r {int}

 Change Log:
  1. 2024-06-24 - Initial

 Testing: 
  1. Not defined
"""

import sys
import json as j
from commandlines import Command as cmd

def is_json(json):
    try:
        j.loads(json)
    except ValueError:
        return False
    return True

r = str()

try:
   c = cmd()  
   r = c.get_definition('r') 
   r = int(r)

except Exception as err:
   r = 6

count=0
try:
 for line in sys.stdin:
   count+=1
   
   if count < r+1:
      print(line,end="")

 sys.stdin.close()
except Exception as e:
 print(e)
