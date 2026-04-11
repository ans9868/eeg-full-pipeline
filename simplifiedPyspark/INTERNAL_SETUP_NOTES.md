# Internal Setup Notes

This document is intentionally internal-facing.
It is not written in article style.
It is a record of the problems I ran into while extracting the reusable `simplifiedPyspark` example from the larger EEG PySpark setup.

## Goal

Build a minimal PySpark example with:

- a `standard` variant that is close to vanilla and can fail in realistic ways
- a `fixed` variant that carries only the portability logic we actually need
- validation across:
  - local Docker
  - Singularity in the HPC simulation
  - arbitrary remapped UIDs as a proxy for real HPC behavior

## Problems I Ran Into

### 1. Docker success was misleading

At first, Docker looked "good enough" because both variants could be made to run locally.
That was misleading.

What actually happened:

- `standard` in Docker still emitted the Hadoop / UnixPrincipal warning stack
- the warning did not always stop execution
- that made it tempting to treat it as harmless noise

Why this mattered:

- the same warning became much more important once the runtime UID changed
- under a remapped UID, the problem turned into a real failure instead of just startup noise

Internal takeaway:

- if Docker prints the Hadoop login warning, do not treat that as solved just because the job finishes

### 2. I initially underweighted the launch command

I first focused too heavily on the image: Dockerfile, entrypoint, and session builder.
That was only part of the story.

The original EEG code already had important Singularity runtime flags in [`start-pipelines.py`](/Users/user/projects/eeg-full-pipeline/start-pipelines.py#L408):

- `--no-mount tmp`
- `--cleanenv`
- `--writable-tmpfs`
- `/etc/passwd` and `/etc/group` binds
- `HADOOP_CONF_DIR=/tmp`
- `HADOOP_HOME=/tmp`
- `JAVA_TOOL_OPTIONS=...simple auth...`

Without those flags:

- `standard` failed immediately in the HPC simulation with:
  - `mkdir: cannot create directory '/tmp/.ivy2': Read-only file system`
- `fixed` got further, but still failed with:
  - `Failed to create a temp directory (under /tmp) after 10 attempts!`

Internal takeaway:

- the article should clearly separate image-level fixes from launch-time fixes
- the runtime command matters just as much as the image

### 3. Ivy was more fragile than expected

The simplified setup initially failed much earlier than expected because Spark/Ivy was trying to resolve to a bad default path.

Observed failure:

```text
IllegalArgumentException: basedir must be absolute: ?/.ivy2.5.2/local
```

What fixed it:

- explicitly using `spark-submit --conf spark.jars.ivy=/tmp/.ivy2 ...`
- creating `/tmp/.ivy2` in the entrypoint

Why this matters:

- this is easy to miss when trying to make a "minimal" example
- if we omit it, we get a misleading failure before the more interesting Spark/Hadoop portability issues appear

Internal takeaway:

- "minimal" still needs to be realistic enough to get past Ivy

### 4. My first `fixed` implementation was not actually HPC-safe enough

I initially made `fixed` create shared directories like `/tmp/spark-local` during the image build and hand them to the `spark` user.
That looked reasonable but broke under arbitrary remapped UIDs.

Observed failure under:

```bash
docker run --rm --user 23456:23456 simplified-pyspark:fixed
```

Observed error:

```text
java.nio.file.AccessDeniedException: /tmp/spark-local/blockmgr-...
```

Root problem:

- the directory existed
- but it belonged to the wrong user model for a remapped UID run

What actually worked:

- create UID-specific runtime directories in the entrypoint under `/tmp`
- export those paths into Spark
- switch into a writable runtime workdir before `spark-submit` starts

This is now implemented in [`fixed/entrypoint.sh`](/Users/user/projects/eeg-full-pipeline/simplifiedPyspark/fixed/entrypoint.sh#L22) and consumed in [`fixed/session_builder.py`](/Users/user/projects/eeg-full-pipeline/simplifiedPyspark/fixed/session_builder.py#L19).

Internal takeaway:

- precreating global temp dirs during image build is not enough
- runtime directory creation is the safer pattern

### 5. Spark artifact temp directories were easy to forget

Even after getting farther, `standard` still failed under arbitrary UID runs because Spark tried to create runtime artifacts under the current working directory.

Observed failure:

```text
java.io.IOException: Failed to create a temp directory (under artifacts) after 10 attempts!
```

What was going on:

- Spark 4 creates runtime artifact dirs relative to the working directory in some flows
- our image `WORKDIR` was `/app`
- `/app` is not a good writable target for arbitrary remapped users

What fixed it for `fixed`:

- `cd` into a writable runtime workdir under `/tmp`

Internal takeaway:

- writable Spark local dirs are not enough by themselves
- writable working directory also matters

### 6. The HPC simulation is helpful but incomplete

The current HPC simulation was very useful, but it does not reproduce every real-HPC failure mode.

What it reproduced well:

- read-only temp issues
- missing writable overlay behavior
- the importance of the original Singularity flags

What it did not fully reproduce:

- arbitrary unknown user IDs the same way a real HPC environment often does

Why:

- the simulation runs Singularity as `root`
- once we used the full pipeline-style run command, both `standard` and `fixed` could succeed there

So for now:

- the HPC simulation is best for the Singularity temp/overlay story
- the arbitrary-UID Docker run is the better proxy for the real HPC user-remap story

Internal takeaway:

- do not oversell the simulation as identical to the real cluster

### 7. I had to keep pulling details back from the original EEG setup

Whenever I simplified too aggressively, things broke in ways that were not educational.
The original EEG PySpark setup already encoded several survival lessons:

- stable `HADOOP_USER_NAME`
- dynamic `USER` repair
- `nss_wrapper` for unknown UIDs
- explicit Hadoop simple-auth settings
- explicit local filesystem settings
- Singularity launch flags that preserve writable temp space

Internal takeaway:

- the right move was not to invent a new minimal setup from scratch
- the right move was to distill the existing proven setup carefully

## What Ended Up Mattering Most

If I had to summarize the real portability requirements as a short internal checklist:

1. give Ivy a known writable location
2. give Spark a known writable local dir
3. give Spark a writable working directory
4. force simple Hadoop auth and local filesystem assumptions
5. give Java/Hadoop a stable username even under weird runtime UIDs
6. use runtime-created temp dirs instead of assuming image-owned dirs are enough
7. use the correct Singularity launch flags

## Good Failure Cases We Now Have

These are useful for the future article and demos:

- `standard` naive Singularity:
  - `/tmp/.ivy2` read-only failure
- `fixed` naive Singularity:
  - Spark temp directory failure under `/tmp`
- `standard` arbitrary UID Docker:
  - Hadoop UnixPrincipal login failure
  - Spark artifact temp directory failure under `artifacts`
- `fixed` arbitrary UID Docker:
  - succeeds end-to-end

## What I Would Re-Check On Real HPC

When real cluster access is available, I would test:

1. whether the runtime UID is missing from the container user database
2. whether `/tmp` is writable without extra flags
3. whether `/etc/passwd` and `/etc/group` binds are required there
4. whether the same `standard` vs `fixed` split reproduces cleanly
5. whether `spark.jars.ivy=/tmp/.ivy2` is still enough on that system

## Recommended Internal Framing For The Article

The article should probably not claim:

- "Docker vs Singularity" only

It should more accurately claim:

- "There are at least three separate portability problems"
  - writable temp and overlay behavior
  - runtime UID / Unix user lookup
  - Spark/Hadoop local filesystem assumptions

That framing matches what actually happened during setup.
