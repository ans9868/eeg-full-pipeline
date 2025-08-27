#!/bin/bash

# Check if an argument was provided
if [ $# -eq 0 ]; then
  echo "Usage: $0 <input_parameter>"
  exit 1
fi

INPUT_PARAM="$1"

cd eeg-pyspark-pipeline
make build
make push
cd ..

cd eeg-ray-tuner
make build
make push
cd ..

python start-pipelines.py "$INPUT_PARAM"

