STANDARD_IMAGE=simplified-pyspark:standard
FIXED_IMAGE=simplified-pyspark:fixed
RANDOM_UID?=23456

build-standard:
	docker build -f standard/Dockerfile -t $(STANDARD_IMAGE) .

build-fixed:
	docker build -f fixed/Dockerfile -t $(FIXED_IMAGE) .

build-all: build-standard build-fixed

run-standard:
	docker run --rm $(STANDARD_IMAGE)

run-fixed:
	docker run --rm $(FIXED_IMAGE)

run-standard-udf:
	docker run --rm $(STANDARD_IMAGE) spark-submit /app/app.py --job udf

run-fixed-udf:
	docker run --rm $(FIXED_IMAGE) spark-submit /app/app.py --job udf

run-standard-udtf:
	docker run --rm $(STANDARD_IMAGE) spark-submit /app/app.py --job udtf

run-fixed-udtf:
	docker run --rm $(FIXED_IMAGE) spark-submit /app/app.py --job udtf

run-standard-random-uid:
	docker run --rm --user $(RANDOM_UID):$(RANDOM_UID) $(STANDARD_IMAGE)

run-fixed-random-uid:
	docker run --rm --user $(RANDOM_UID):$(RANDOM_UID) $(FIXED_IMAGE)
