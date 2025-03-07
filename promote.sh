#!/bin/bash

# Prompt for the directory to copy files to
read -p "Enter the directory to copy files to: " target_dir

# Check if the directory exists
if [ -d "$target_dir" ]; then
    echo "Directory exists. Proceeding with file copy..."
    # List of filenames to copy
    
    files="appName bytesRead collScans cpuc \
           docsExamined drivers formatOne jsonFetcher keysExamined millis\
           ns nsCount nsCountUser nsIndexes phead prettyJson queryHash"       

    # Directory to copy files from
    source_dir="dist"

    # Copy files from source_dir to target_dir
    for file in $files; do
        if [ -e "$source_dir/$file" ] && [ -f "$source_dir/$file" ]; then
            cp "$source_dir/$file" "$target_dir"
            echo "Copied $file to $target_dir"
        else
           if [ -f "$source_dir/$file" ]; then 
              echo "File $file does not exist in $source_dir"
           fi
        fi
    done
else
    echo "Warning: Directory does not exist."
fi