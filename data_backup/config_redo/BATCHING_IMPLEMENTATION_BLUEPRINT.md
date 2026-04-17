# Mac Mini Batch Processing Implementation Blueprint

This blueprint gives concrete, copy-ready code snippets for adding **smart subject batching** to the PySpark stage.

## Goal

Prevent memory crashes in `process_subjects` by scheduling subjects into batches using `.set` file sizes.

---

## 1) `config-maker.py` changes

### Where
- Function: `deploymentMethodPart6(...)`

### Add these prompts under `config["pyspark"]`

```python
# 6.1.7 Auto batch sizing
config["pyspark"]["auto_batch_size"] = questionary.select(
    "6.1.7 Enable auto batch sizing for process_subjects?",
    choices=["Yes", "No"],
).ask()

# 6.1.8 Subject batch size hard cap
config["pyspark"]["max_subjects_per_batch"] = validate_integer_input(
    "6.1.8 Max subjects per batch (hard cap, e.g., 6):",
    default="6"
)

# 6.1.9 Memory budget percent
config["pyspark"]["memory_budget_percent"] = float(questionary.text(
    "6.1.9 Memory budget percent for batching (0-100):",
    default="45"
).ask())

# 6.1.10 Memory safety buffer MB
config["pyspark"]["memory_safety_buffer_mb"] = float(questionary.text(
    "6.1.10 Memory safety buffer MB (headroom, e.g., 1024):",
    default="1024"
).ask())

# 6.1.11 Allow swap for budget
config["pyspark"]["allow_swap_for_budget"] = questionary.select(
    "6.1.11 Allow swap memory in batch budget?",
    choices=["Yes", "No"],
).ask())
```

### Default block (`No (use defaults)`) should include

```python
"auto_batch_size": "Yes",
"max_subjects_per_batch": 6,
"memory_budget_percent": 45.0,
"memory_safety_buffer_mb": 1024.0,
"allow_swap_for_budget": "Yes",
"batch_target_mb": 180.0,  # optional hard ceiling (kept for compatibility)
```

---

## 2) `config_handler.py` changes

### A) Validation in `deploymentMethodPart6_validate`

After required field checks:

```python
if "auto_batch_size" in pyspark_config and pyspark_config["auto_batch_size"] not in ["Yes", "No"]:
    raise ValueError("pyspark.auto_batch_size must be 'Yes' or 'No'")

if "max_subjects_per_batch" in pyspark_config:
    v = int(pyspark_config["max_subjects_per_batch"])
    if v < 1:
        raise ValueError("pyspark.max_subjects_per_batch must be >= 1")

if "memory_budget_percent" in pyspark_config:
    v = float(pyspark_config["memory_budget_percent"])
    if not (1.0 <= v <= 95.0):
        raise ValueError("pyspark.memory_budget_percent must be between 1 and 95")

if "memory_safety_buffer_mb" in pyspark_config:
    v = float(pyspark_config["memory_safety_buffer_mb"])
    if v < 0:
        raise ValueError("pyspark.memory_safety_buffer_mb must be >= 0")

if "allow_swap_for_budget" in pyspark_config and pyspark_config["allow_swap_for_budget"] not in ["Yes", "No"]:
    raise ValueError("pyspark.allow_swap_for_budget must be 'Yes' or 'No'")
```

### B) Add properties

```python
@property
def auto_batch_size(self) -> bool:
    return self.raw_config.get("pyspark", {}).get("auto_batch_size", "Yes") == "Yes"

@property
def max_subjects_per_batch(self) -> int:
    pyspark_cfg = self.raw_config.get("pyspark", {})
    return int(pyspark_cfg.get("max_subjects_per_batch", pyspark_cfg.get("subject_batch_size", 6)))

@property
def memory_budget_percent(self) -> float:
    return float(self.raw_config.get("pyspark", {}).get("memory_budget_percent", 45.0))

@property
def memory_safety_buffer_mb(self) -> float:
    return float(self.raw_config.get("pyspark", {}).get("memory_safety_buffer_mb", 1024.0))

@property
def allow_swap_for_budget(self) -> bool:
    return self.raw_config.get("pyspark", {}).get("allow_swap_for_budget", "Yes") == "Yes"
```

---

## 3) `process_subjects.py` changes (main batching logic)

### A) Add helper functions near top

```python
from typing import Optional


def _file_size_mb(path: str) -> float:
    try:
        return os.path.getsize(path) / (1024 * 1024)
    except Exception:
        return 0.0


def _compute_batch_target_mb(config_handler: 'UnifiedConfigHandler') -> Tuple[float, Dict[str, float]]:
    # compute RAM(+optional swap) budget using percent and safety buffer
    ...


def _schedule_batches_ffd(
    subject_data: List[Tuple[str, str, str]],
    target_batch_mb: float,
    max_subjects_per_batch: Optional[int],
) -> List[List[Tuple[str, str, str]]]:
    # subject_data tuples are (SubjectID, Group, Path)
    decorated = []
    for row in subject_data:
        size_mb = _file_size_mb(row[2])
        decorated.append((row, size_mb))

    decorated.sort(key=lambda x: x[1], reverse=True)

    batches: List[List[Tuple[str, str, str]]] = []
    totals: List[float] = []

    for (row, size_mb) in decorated:
        placed = False
        for i in range(len(batches)):
            room_ok = (totals[i] + size_mb) <= target_batch_mb
            count_ok = True if max_subjects_per_batch is None else len(batches[i]) < max_subjects_per_batch
            if room_ok and count_ok:
                batches[i].append(row)
                totals[i] += size_mb
                placed = True
                break

        if not placed:
            batches.append([row])
            totals.append(size_mb)

    return batches
```

### A.1) Put explicit knob comments *in code* (right next to batching logic)

Add a short comment block directly above the batch settings in `process_subjects.py` so future us remembers intent and rollout order:

```python
# Batching knobs (roll out gradually; do NOT enable all at once):
# 1) memory_budget_percent (primary control, safest first)
# 2) memory_safety_buffer_mb (extra headroom)
# 3) max_subjects_per_batch (guardrail, not primary scheduler)
# 4) allow_swap_for_budget (keep OFF by default; swap can be very slow)
#
# NOTE:
# - We schedule by estimated memory/file size, not fixed subject count.
# - max_subjects_per_batch is only a cap.
# - Prefer RAM-only budgeting first for stable behavior.
```

### B) Replace single-pass UDTF execution with per-batch execution

Current code does one global call:

```sql
SELECT * FROM ProcessSubjectUDTF(TABLE(subjects_metadata))
```

Replace with:

```python
# Build batch settings
target_batch_mb, diag = _compute_batch_target_mb(config_handler)
max_subjects = config_handler.max_subjects_per_batch

batches = _schedule_batches_ffd(
    subject_data=subject_data,
    target_batch_mb=target_batch_mb,
    max_subjects_per_batch=max_subjects,
)

print(f"📦 Smart batching enabled: {len(batches)} batches")
print(f"   target_batch_mb={target_batch_mb:.1f}, max_subjects_per_batch={max_subjects}")

batch_dfs: List[DataFrame] = []

for idx, batch_rows in enumerate(batches, start=1):
    batch_subjects_df = spark.createDataFrame(batch_rows, get_subject_schema())
    batch_subjects_df = batch_subjects_df.coalesce(min(len(batch_rows), 4))
    batch_subjects_df.createOrReplaceTempView("subjects_metadata")

    print(f"🔄 Running batch {idx}/{len(batches)} with {len(batch_rows)} subjects")
    part_df = spark.sql("SELECT * FROM ProcessSubjectUDTF(TABLE(subjects_metadata))")

    # Break lineage per batch to reduce pressure
    part_df = part_df.checkpoint()
    _ = part_df.count()
    batch_dfs.append(part_df)

# Union all batch outputs
processed_subjects_df = batch_dfs[0]
for i in range(1, len(batch_dfs)):
    processed_subjects_df = processed_subjects_df.unionByName(batch_dfs[i])

processed_subjects_df = processed_subjects_df.checkpoint()
_ = processed_subjects_df.count()
```

### C) Keep label encoding global (important)

Keep `encode_groups_to_labels(...)` **after** all batch outputs are unioned (as it currently is). This preserves consistent label mapping for disease classes.

---

## 4) Optional but recommended: `process_subject.py`

This file is still a memory hotspot due to:
- `read_raw_eeglab(..., preload=True)`
- `Epochs(..., preload=True)`

Do this as phase 2 if needed:
- add a config switch to try `preload=False` path where safe.
- keep current behavior as default for correctness stability.

---

## 5) Runtime notes

Because `start-pipelines.py` runs Docker images:
- `nour333/eeg-spark-pipeline:latest`

You must rebuild/publish image (or point to local image tag) for code changes to take effect in container runs.

---

## 6) Acceptance tests

1. Tiny smoke (4 subjects): should produce identical outputs as today.
2. Medium run (20+ subjects): no exit 137.
3. Label integrity check:
   - only 2 labels in W_C (`0/1`)
   - Group→label mapping remains clean.
4. Reproducibility:
   - same config hash behavior
   - same split seed behavior.

---

## 7) Suggested first config defaults for Mac Mini

```yaml
pyspark:
  master: 4
  driver_memory: 6
  executor_memory: 6
  executor_cores: 2
  shuffle_partitions: 8
  auto_batch_size: 'Yes'
  max_subjects_per_batch: 6
  memory_budget_percent: 45.0
  memory_safety_buffer_mb: 1024
  allow_swap_for_budget: 'Yes'
  batch_target_mb: 180.0

  # Optional override path (legacy compatibility)
  # subject_batch_size: 6
```

These are conservative and should be stable.

---

## 8) Staged rollout (to avoid debugging collisions)

1. Implement batching with memory-based target only (`memory_budget_percent` path).
2. Validate stability + label integrity.
3. Add `memory_safety_buffer_mb`.
4. Add `max_subjects_per_batch`.
5. Keep `allow_swap_for_budget` disabled by default.
