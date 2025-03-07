#!/usr/bin/env python3

"""

 File: nsCount.py
 Author: Dennis Spera
 Modification log;

  2024-06-24 -- initial
  2024-12-15 -- provide different output specification
 
 Description: 
  Display counts by namespace 
  depending on how you would like the output to be displayed use the following parameters

  cat mongodb | nsCount         #   default tabular
  cat mongodb | nsCount -o tab  #   tabular
  cat mongodb | nsCount -o md   #   markup
  cat mongodb | nsCount -o csv  #   comma delimited

"""

import json, sys
import json as j
from collections import Counter
from tabulate import tabulate
from commandlines import Command as cmd

def is_json(json):
    try:
        j.loads(json)
    except ValueError:
        return False
    return True

class formatOutput:
    def __init__(self):
       '''

       '''

    def _printOutput(self, header, data, _format):

        if _format == 'default':       
           table = tabulate(data, headers=header, tablefmt="grid")
           print(table) 

        elif _format == 'tab':       
           table = tabulate(data, headers=header, tablefmt="grid")
           print(table) 

        elif _format == 'md':  
           
           for col in header:
              print ('|',end="")
              print ( '**',col,'**',end="",sep="" ) 
           print('|')   

           for col in header:
              print ('|',end="")
              print ( len(col) * '-',end="",sep="" ) 
           print('|')            

           for l in data:
             for col in l: 
               print ('|',end="")
               print ( col,end="",sep="" )
             print('|')  

        elif _format == 'csv':    

           ct=1   
           for col in header:
              print ( col,end="",sep="" ) 
              if len(header) > ct:
                 print (',',end="",sep="" ) 
              ct+=1          
           
           print("\r")
           for l in data:
             ct=1
             for col in l: 
               print ( col,end="",sep="" ) 
               if len(header) > ct:
                 print (',',end="",sep="" ) 
               else:
                 print ("\r")                  
               ct+=1   

        else:
           sys.stderr.write('output format '+_format+' is not implemented')
         
o = 'default'
c = str()
try:
   c = cmd() 
   try:  
       o = c.get_definition('o') 
   except:
       pass
except:
   pass

jsonFile = list()

ptr=0
for line in sys.stdin:
   ptr+=1
   if is_json(line):
      try: 
        jsonFile.append( j.loads(line))
      except:
        sys.stderr.write('rec #'+str(ptr)+' invalid json bypassed')
sys.stdin.close()

ns = list()
for json in jsonFile:
    if json['c'] == 'COMMAND':
       try:
        ns.append(json['attr']['ns'])
       except:
        pass
       
sorted_list = sorted(ns)
element_counts = Counter(sorted_list)

data = []
for element, count in element_counts.items():
    data.append([str(element), count]) 

data.sort(key=lambda x: x[1], reverse=True)

header = ["Name Space", "Count"] 
fmt = formatOutput()
fmt._printOutput(header, data, o)
