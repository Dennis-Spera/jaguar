#!/usr/bin/env python3

"""

 File: prettyJson.py
 Author: Dennis Spera
 Date: 2024-06-24
 Description: format mongodb json similiar to that of jq.

"""

import sys
import json as j

for line in sys.stdin:
   print(j.dumps(j.loads(line.strip()), indent=4))
sys.stdin.close()
