# simplifiedPyspark

This directory is a minimal, reusable standalone PySpark example for three environments:

- Docker on a local machine
- Singularity outside HPC
- Singularity in HPC-style environments with changing runtime UIDs

It is intentionally split into two variants:

- `standard/`: a near-vanilla container setup that is expected to work in Docker but fail in stricter Singularity or HPC-like runs
- `fixed/`: a small portability-focused setup that adds writable temp paths, stable Hadoop user handling, and runtime UID repair

The shared demo app runs three Spark workloads:

- a basic DataFrame transformation
- a Python UDF
- a Python UDTF

The UDF and UDTF cases are useful because they exercise Python artifact shipping and are more likely to expose the environment problems this example is meant to teach.

## Layout

```text
simplifiedPyspark/
├── README.md
├── shared/
│   ├── app.py
│   └── jobs.py
├── standard/
│   ├── Dockerfile
│   ├── entrypoint.sh
│   └── session_builder.py
└── fixed/
    ├── Dockerfile
    ├── entrypoint.sh
    └── session_builder.py
```

## Build

Build from the `simplifiedPyspark/` directory so the Docker build context includes `shared/`.

```bash
docker build -f standard/Dockerfile -t simplified-pyspark:standard .
docker build -f fixed/Dockerfile -t simplified-pyspark:fixed .
```

## Run In Docker

```bash
docker run --rm simplified-pyspark:standard
docker run --rm simplified-pyspark:fixed
```

To simulate the arbitrary runtime UID behavior common on HPC systems:

```bash
make run-standard-random-uid
make run-fixed-random-uid
```

In the current example:

- `standard` fails under a remapped UID
- `fixed` succeeds under the same remapped UID by creating UID-specific writable runtime directories under `/tmp`

## Run In Singularity

The image changes alone are not enough. The launch pattern from the original EEG pipeline is also important.

Naive Singularity runs that fail in the current HPC simulation:

```bash
singularity run --cleanenv --no-mount tmp singularity/standard.sif
singularity run --cleanenv --no-mount tmp singularity/fixed.sif
```

Pipeline-style invocation that matches the original working setup more closely:

```bash
singularity run \
  --no-mount tmp \
  --cleanenv \
  --writable-tmpfs \
  --env HADOOP_CONF_DIR=/tmp \
  --env HADOOP_HOME=/tmp \
  --env "JAVA_TOOL_OPTIONS=-Djava.security.auth.login.config= -Dhadoop.security.authentication=simple -Dhadoop.security.authorization=false" \
  --bind /etc/passwd:/etc/passwd:ro \
  --bind /etc/group:/etc/group:ro \
  singularity/fixed.sif
```

Those flags come directly from the original launcher logic in [`start-pipelines.py`](/Users/user/projects/eeg-full-pipeline/start-pipelines.py#L408).

## Expected Behavior

- `standard` is the teaching baseline.
  It keeps the setup intentionally small and does not include the runtime user and writable-temp repairs needed for Singularity-heavy environments.
- `fixed` adds only the portability pieces needed to make the same app more robust across Docker, Singularity, and HPC-style runs.

## Notes For The Article

The intended article flow is:

1. show that the simple version works in Docker
2. run the same image through Singularity or an HPC simulation
3. capture the failure logs
4. explain why the failure happens
5. introduce the fixed variant
6. rerun the same jobs and show the environment-agnostic result

Capture real logs in the future rather than replacing them with paraphrases. The point of this example is reproducibility.
