#!/bin/bash

# Define the input file in the current directory
input_file="./fronttest.yaml"

# Use sed to find and replace the targetPort value
sed -i 's/targetPort: 8010/targetPort: 8050/' "$input_file"

echo "Updated targetPort from 8010 to 8050 in $input_file"

