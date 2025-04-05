#!/usr/bin/env python3

"""

 File: jsonFetcher.py
 Author: Dennis Spera
 
"""

import sys
import json as j
from datetime import datetime
import re as regex
from commandlines import Command as cmd


b = str()
e = str()
start_d_t_fmt = None
end_d_t_fmt = None
max_input_length = 14
min_input_length = 8

def is_json(json):
    try:
        j.loads(json)
    except ValueError:
        return False
    return True

def printHelp():
    sys.stderr.write('enter a valid beginning {b} date and end {e} to extract from logs'+"\n")
    sys.stderr.write('jsonFetcher -b YYYYMMDD[24HRMISS] -e YYYYMMDD[24HRMISS]'+"\n")    

try:
   c = cmd()
  
   try:  
       b = c.get_definition('b') 
       if len(b) > max_input_length:
           sys.stderr.write('beginning timestamp exceeds beginning timesamp length of ' + str(max_input_length))
           printHelp()
           sys.exit(0)
       if len(b) < min_input_length:
           sys.stderr.write('beginning timestamp less than beginning timesamp length of ' + str(min_input_length))
           printHelp()
           sys.exit(0)           

       try:
          test = int(b) 
       except:
           sys.stderr.write('beginning timestamp is an invalid data format')
           sys.exit(0)      

       padding = max_input_length - len(b)             

       if padding > 0: 
          for i in range(1, padding+1, 1):
              b=b+'0'
  
       e = c.get_definition('e') 
       if len(e) > max_input_length:
           sys.stderr.write('ending timestamp exceeds ending timesamp length of ' + str(max_input_length))
           printHelp()
           sys.exit(0)
       if len(b) < min_input_length:
           sys.stderr.write('ending timestamp less than ending timesamp length of ' + str(min_input_length))
           printHelp()
           sys.exit(0)           

       try:
          test = int(e) 
       except:
           sys.stderr.write('end timestamp is an invalid data format')
           printHelp()
           sys.exit(0)      

       padding = max_input_length - len(e)             

       if padding > 0: 
          for i in range(1, padding+1, 1):
              e=e+'0'
                
   except:
        sys.stderr.write('error parsing input parameters')
        printHelp()
        sys.exit(0) 

   for line in sys.stdin:
     if is_json(line):

        d = j.loads(line)
        dateT = d["t"]["$date"]

        match_object = regex.match( r'(\d{4})([-])(\d{2})([-])(\d{2})([T])(\d{2})([:])(\d{2})([:])(\d{2})(.*)', dateT)
        d_t_fmt = datetime.strptime(match_object.group(1)+match_object.group(3)\
                                   +match_object.group(5)\
                                   +match_object.group(7)+match_object.group(9)
                                   +match_object.group(11), '%Y%m%d%H%M%S')  
        
        match_object = regex.match( r'(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})',  b) 

        try:
          start_d_t_fmt = datetime.strptime(match_object.group(1)+match_object.group(2)\
                                                       +match_object.group(3)\
                                                       +match_object.group(4)+match_object.group(5)
                                                       +match_object.group(6), '%Y%m%d%H%M%S')
        except:
                 sys.stderr.write('error converting start date-time to a datatime format')  
                 printHelp() 
                 sys.exit(0) 


        match_object = regex.match( r'(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})',  e) 

        try:
          end_d_t_fmt = datetime.strptime(match_object.group(1)+match_object.group(2)\
                                                       +match_object.group(3)\
                                                       +match_object.group(4)+match_object.group(5)
                                                       +match_object.group(6), '%Y%m%d%H%M%S')
        except:
                 sys.stderr.write('error converting end date-time to a datatime format') 
                 printHelp() 
                 sys.exit(0) 

        try:
           if (start_d_t_fmt <= d_t_fmt) and (end_d_t_fmt >= d_t_fmt) and not regex.match(r'^$', line):
              print(line,end="")

        except:
            sys.stderr.write('error with begin-date and end-date format'+"\n")  
            printHelp()
            sys.exit(0) 


   sys.stdin.close()

except OSError as err:
  sys.stderr.write(err)

