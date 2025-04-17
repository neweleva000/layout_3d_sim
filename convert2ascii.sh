#!/bin/bash

# Check if a folder is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <folder>"
    exit 1
fi

# Get the folder path from the argument
folder="$1"

# Check if the folder exists
if [ ! -d "$folder" ]; then
    echo "Error: Directory $folder does not exist."
    exit 1
fi

# Loop through all STL files in the folder
for stl_file in "$folder"/*.stl; do
    # Check if the file exists
    if [ -f "$stl_file" ]; then
        # Extract the filename without extension
        filename=$(basename "$stl_file" .stl)

        # Define the output file name (replace .stl with .ascii)
        output_file="$folder/$filename.ascii"

        # Convert the STL to ASCII using stl2ascii
        echo "Converting $stl_file to $output_file"
        stl2ascii "$stl_file" "$stl_file.ascii"

        if [ $? -eq 0 ]; then
            echo "Conversion successful: $output_file"
        else
            echo "Error: Conversion failed for $stl_file"
        fi
    fi
done

