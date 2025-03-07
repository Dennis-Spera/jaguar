#!/bin/bash

export files="appName.py bytesRead.py collScans.py cpuc.py \
              docsExamined.py drivers.py formatOne.py jsonFetcher.py keysExamined.py millis.py \
              ns.py nsCount.py nsCountUser.py nsIndexes.py phead.py prettyJson.py queryHash.py"


for file in $files; do
    pyinstaller --onefile $file
done