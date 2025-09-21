#!/bin/bash

# Check if an argument was provided
if [ $# -eq 0 ]; then
  echo "Usage: $0 <input_parameter>"
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

# Try to run the Python script with error handling
if ! python3 start-pipelines.py "$INPUT_PARAM"; then
  echo "ERROR: Pipeline was unable to run."
  echo "The Python script failed with exit code: $?"
  exit 1
fi
