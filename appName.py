#!/usr/bin/env python3

"""

 File: appName.py
 Author: Dennis Spera
 Date: 2024-06-24
 Description: Extract appName totals from mongod.log on stdin.

"""

import json as j, sys
from collections import Counter

def is_json(json):
    try:
        j.loads(json)
    except ValueError:
        return False
    return True


def extract_app_name(entry):
    attr = entry.get('attr', {})

    app_name = attr.get('appName')
    if app_name:
        return app_name

    doc = attr.get('doc', {})
    application = doc.get('application', {})
    app_name = application.get('name')
    if app_name:
        return app_name

    return None


app_names = Counter()

for line in sys.stdin:
    if not is_json(line):
        continue

    data = j.loads(line)
    app_name = extract_app_name(data)
    if app_name:
        app_names[app_name] += 1

sys.stdin.close()

sorted_result = dict(sorted(app_names.items(), key=lambda x: x[1], reverse=True))

print("| Count | appName |")
print("| --- | --- |")

for k, v in sorted_result.items():
    safe_name = str(k).replace("|", "\\|")
    print(f"| {v} | {safe_name} |")