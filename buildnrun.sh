cd eeg-pyspark-pipeline
make build
make push
cd ..

cd eeg-ray-tuner
make build
make push
cd ..

py-neuro-env
python start-pipelines.py