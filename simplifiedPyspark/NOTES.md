# Notes

This file is for collecting the real evidence needed for the article.

## Jobs To Exercise

- DataFrame transformation
- Python UDF
- Python UDTF

## Environment Matrix

- Docker local
- Singularity outside HPC
- Singularity in HPC simulation
- Real HPC when available

## Standard Variant

Expected role:

- minimal baseline
- useful for reproducing environment-specific failures

Log capture checklist:

- exact command
- runtime UID / `whoami`
- full stderr
- first failure line
- whether DataFrame, UDF, and UDTF fail in the same or different ways

Known failure classes to watch for:

- read-only filesystem errors for artifact or temp directories
- missing writable warehouse or local Spark dirs
- Unix user resolution errors
- Hadoop local filesystem auth or user-name errors

Current observed behavior:

- Docker local:
  - runs successfully
  - but may emit Hadoop / UnixPrincipal warning stacks before continuing
- Docker local with an arbitrary runtime UID:
  - fails
  - first emits the Hadoop / UnixPrincipal login warning
  - later fails creating Spark SQL artifact temp directories under `/app/artifacts`
- Singularity with a naive run:
  - fails immediately on Ivy temp setup
- Singularity with the original pipeline-style launch flags:
  - runs successfully in the current HPC simulation

Observed naive Singularity failure:

```text
mkdir: cannot create directory '/tmp/.ivy2': Read-only file system
```

Observed arbitrary-UID Docker failures:

```text
org.apache.hadoop.security.KerberosAuthException: failure to login:
javax.security.auth.login.LoginException: java.lang.NullPointerException: invalid null input: name
```

```text
java.io.IOException: Failed to create a temp directory (under artifacts) after 10 attempts!
```

## Fixed Variant

Expected role:

- same app
- minimal portability additions
- demonstrates the smallest practical fix set

Important evidence to capture:

- same command shape as standard
- runtime UID and env details
- proof that the same jobs now complete

Current observed behavior:

- Docker local:
  - runs successfully and cleanly
- Docker local with an arbitrary runtime UID:
  - runs successfully
  - DataFrame, UDF, and UDTF all complete
- Singularity with a naive run:
  - gets past Ivy setup, but Spark itself still fails creating temp dirs in `/tmp`
- Singularity with the original pipeline-style launch flags:
  - runs successfully in the current HPC simulation

Observed naive Singularity failure after image-level fixes:

```text
java.io.IOException: Failed to create a temp directory (under /tmp) after 10 attempts!
```

Observed arbitrary-UID Docker success indicators:

```text
[fixed] USER=uid23456 CURRENT_USER=uid23456 CURRENT_UID=23456
[fixed] SIMPLIFIED_RUNTIME_ROOT=/tmp/simplified-pyspark-23456
```

```text
[JOB:dataframe] Completed
[JOB:udf] Completed
[JOB:udtf] Completed
```

## Key Commands

Naive Singularity run that failed:

```bash
singularity run --cleanenv --no-mount tmp singularity/standard.sif
singularity run --cleanenv --no-mount tmp singularity/fixed.sif
```

Arbitrary-UID Docker comparison:

```bash
docker run --rm --user 23456:23456 simplified-pyspark:standard
docker run --rm --user 23456:23456 simplified-pyspark:fixed
```

Pipeline-style Singularity run that worked in HPC simulation:

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

The same improved invocation also worked for `standard.sif` in the current HPC simulation.

## Important Interpretation

The current HPC simulation runs Singularity as `root`, with valid `/etc/passwd` and `/etc/group` binds.
That means this simulation is very good for reproducing:

- read-only temp and writable-overlay issues
- missing Singularity runtime flags

But it does not fully reproduce the arbitrary-UID problem common on real HPC systems.
The arbitrary-UID Docker test is a better proxy for that behavior right now:

- `standard` fails under a remapped UID
- `fixed` succeeds by creating UID-specific runtime directories under `/tmp`, switching to a writable working directory, and synthesizing a stable username for Java and Hadoop

## Article Skeleton

1. Start with a simple standalone Spark image
2. Show that Docker can look fine
3. Move the same image into Singularity or HPC-like execution
4. Capture the failure log
5. Explain writable temp paths
6. Explain runtime UID and Unix user lookup
7. Explain why Hadoop still matters even for local standalone Spark
8. Introduce the fixed image
9. Rerun the DataFrame, UDF, and UDTF jobs
10. Summarize the portable pattern
