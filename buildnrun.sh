cd eeg-pyspark-pipeline
make build
make push
cd ..

cd eeg-ray-tuner
make build
make push
cd ..

python start-pipelines.py

