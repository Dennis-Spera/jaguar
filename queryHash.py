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

from collections import Counter
import sys
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
shapeHeading = None

def normalizeShapeValue(value):
  if isinstance(value, str):
    return value
  return j.dumps(value, separators=(',', ':'), sort_keys=True)

for record in jsonFile:
    if record.get('c') != 'COMMAND':
      continue

    attr = record.get('attr')
    if not isinstance(attr, dict):
      continue

    shape = attr.get('queryShape')
    if shape is not None:
      qh = normalizeShapeValue(shape)
      if shapeHeading is None:
        shapeHeading = 'queryShape'
    else:
      qh = attr.get('queryShapeHash') or attr.get('queryHash')
      if qh is not None:
        qh = normalizeShapeValue(qh)
      if qh and shapeHeading is None:
        shapeHeading = 'queryShapeHash' if attr.get('queryShapeHash') else 'queryHash'

    if not qh:
      continue

    queryHash.append(qh)
    queryHashCmd.append({qh: attr.get('command', 'N/A')})

queryHashTotals = dict(Counter(queryHash))
sortedByValue = {k: v for k, v in sorted(queryHashTotals.items(), key=lambda item: item[1], reverse=True)}

COUNT_WIDTH = 10
MIN_SHAPE_WIDTH = 16
MAX_SHAPE_WIDTH = 64
COMMAND_WIDTH = 120

if shapeHeading is None:
  shapeHeading = 'queryShapeHash'

shapeMaxLen = max((len(k) for k in sortedByValue), default=0)
SHAPE_WIDTH = min(MAX_SHAPE_WIDTH, max(MIN_SHAPE_WIDTH, len(shapeHeading), shapeMaxLen))

print(f"{'Count':>{COUNT_WIDTH}}   {shapeHeading:<{SHAPE_WIDTH}}   command")
print(f"{'-' * 5:>{COUNT_WIDTH}}   {'-' * len(shapeHeading):<{SHAPE_WIDTH}}   {'-' * 24}")

def getCommand(qh):
  for d in queryHashCmd: 
      for k,v in d.items():
          if k == qh:
             return(v)

def formatCommand(command):
  text = command if isinstance(command, str) else j.dumps(command, separators=(',', ':'))
  if len(text) <= COMMAND_WIDTH:
    return text
  return text[:COMMAND_WIDTH - 3] + '...'

def formatShape(shapeValue):
  text = shapeValue if isinstance(shapeValue, str) else j.dumps(shapeValue, separators=(',', ':'), sort_keys=True)
  if len(text) <= SHAPE_WIDTH:
    return text
  return text[:SHAPE_WIDTH - 3] + '...'
  
for k,v in sortedByValue.items():
    print(f"{v:>{COUNT_WIDTH}}   {formatShape(k):<{SHAPE_WIDTH}}   {formatCommand(getCommand(k))}")