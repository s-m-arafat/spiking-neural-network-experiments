#!/bin/bash

ROOT_FOLDER="/media/arafat/Arafat/UrbanSound/data"
REPORT_FILE="folder_structure_report.txt"

echo "Folder Structure Report" > "$REPORT_FILE"
echo "Date: $(date)" >> "$REPORT_FILE"
echo >> "$REPORT_FILE"

# Traverse each subfolder and count file types
find "$ROOT_FOLDER" -type d | while read -r dir; do
    echo "Folder: $dir" >> "$REPORT_FILE"
    echo "File Type Counts:" >> "$REPORT_FILE"
    find "$dir" -type f | grep -oE '\.[a-zA-Z0-9]+$' | sort | uniq -c | while read -r count ext; do
        echo "  $ext: $count" >> "$REPORT_FILE"
    done
    echo >> "$REPORT_FILE"
done

echo "Report generated: $REPORT_FILE"