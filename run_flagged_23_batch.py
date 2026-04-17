#!/usr/bin/env python3
"""Batch runner for the 23 flagged intrasubject configs on Mac mini.

Features:
- Fixed run order (impact-first) for the 23 flagged configs
- Resume-safe via JSON state file
- Per-config retries and timeout
- Per-config and master logs
- Success criterion: pipeline exit code 0 + model_comparison.csv exists
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import signal
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

try:
    import yaml
except Exception as exc:  # pragma: no cover
    print(f"ERROR: PyYAML is required for this runner: {exc}")
    sys.exit(1)


RUN_ORDER = [
    "ANOVA_W_C_v1_config_20260112_164738_macmini.yaml",
    "ANOVA_W_C_v2_config_20260112_170553_macmini.yaml",
    "ANOVA_W_C_v3_config_20260112_170713_macmini.yaml",
    "ANOVA_W_C_v4_config_20260112_170747_macmini.yaml",
    "ANOVA_W_C_v5_config_20260112_170812_macmini.yaml",
    "ANOVA_W_C_v6_config_20260112_170812_macmini.yaml",
    "ANOVA_W_C_v7_config_20260112_171606_macmini.yaml",
    "ANOVA_W_C_v8_config_20260112_171612_macmini.yaml",
    "ANOVA_W_C_v9_config_20260112_171616_macmini.yaml",
    "ANOVA_W_C_v10_config_20260113_182942_macmini.yaml",
    "PCA_W_C_v0_config_20251030_180900_macmini.yaml",
    "PCA_W_C_v1_config_20260112_180710_macmini.yaml",
    "PCA_W_C_v2_config_20260112_180718_macmini.yaml",
    "PCA_W_C_v3_config_20260112_180718_macmini.yaml",
    "PCA_W_C_v4_config_20260112_180723_macmini.yaml",
    "PCA_W_C_v5_config_20260112_181138_macmini.yaml",
    "PCA_W_C_v6_config_20260112_181140_macmini.yaml",
    "PCA_W_C_v7_config_20260113_004848_macmini.yaml",
    "PCA_W_C_v8_config_20260113_005509_macmini.yaml",
    "PCA_W_C_v9_config_20260112_181148_macmini.yaml",
    "PCA_W_F_v7_config_20260113_011109_macmini.yaml",
    "PCA_W_F_v8_config_20260113_011109_macmini.yaml",
    "PCA_W_F_v10_config_20260113_183005_macmini.yaml",
]


@dataclass
class ConfigMeta:
    path: Path
    project_name: str
    output_dir: Path


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def extract_meta(path: Path) -> ConfigMeta:
    cfg = load_yaml(path)
    project = cfg.get("project", {})
    project_name = project.get("name")
    output_dir = project.get("output_dir", "./data")
    if not project_name:
        raise ValueError(f"Missing project.name in {path}")
    return ConfigMeta(path=path, project_name=str(project_name), output_dir=Path(str(output_dir)))


def success_marker(meta: ConfigMeta) -> Path:
    # From project output conventions: <output_dir>/<project_name>/ml_results_grid_search/model_comparison.csv
    return (meta.output_dir / meta.project_name / "ml_results_grid_search" / "model_comparison.csv").resolve()


def atomic_write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    tmp.replace(path)


def load_state(path: Path) -> dict:
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "started_at": now_iso(),
        "updated_at": now_iso(),
        "status": "initialized",
        "current": None,
        "runs": [],
    }


def latest_by_config(state: dict) -> Dict[str, dict]:
    latest: Dict[str, dict] = {}
    for r in state.get("runs", []):
        key = r["config_name"]
        cur = latest.get(key)
        if cur is None or int(r.get("attempt", 1)) >= int(cur.get("attempt", 1)):
            latest[key] = r
    return latest


def write_summary_csv(path: Path, state: dict) -> None:
    latest = latest_by_config(state)
    rows = []
    for cfg_name in RUN_ORDER:
        rec = latest.get(cfg_name, {})
        rows.append(
            {
                "config_name": cfg_name,
                "status": rec.get("status", "not_started"),
                "attempt": rec.get("attempt", ""),
                "started_at": rec.get("started_at", ""),
                "ended_at": rec.get("ended_at", ""),
                "duration_sec": rec.get("duration_sec", ""),
                "return_code": rec.get("return_code", ""),
                "success_marker": rec.get("success_marker", ""),
                "error": rec.get("error", ""),
                "log_path": rec.get("log_path", ""),
            }
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "config_name",
                "status",
                "attempt",
                "started_at",
                "ended_at",
                "duration_sec",
                "return_code",
                "success_marker",
                "error",
                "log_path",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def append_master_log(master_log: Path, msg: str) -> None:
    master_log.parent.mkdir(parents=True, exist_ok=True)
    line = f"[{now_iso()}] {msg}"
    print(line, flush=True)
    with master_log.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def attempts_for(state: dict, cfg_name: str) -> int:
    return sum(1 for r in state.get("runs", []) if r.get("config_name") == cfg_name)


def is_completed(state: dict, cfg_name: str) -> bool:
    latest = latest_by_config(state).get(cfg_name)
    return bool(latest and latest.get("status") == "completed")


def run_one(
    cfg_path: Path,
    timeout_sec: int,
    logs_dir: Path,
    master_log: Path,
    state: dict,
    state_file: Path,
    summary_csv: Path,
) -> dict:
    cfg_name = cfg_path.name
    attempt = attempts_for(state, cfg_name) + 1
    meta = extract_meta(cfg_path)
    marker = success_marker(meta)

    per_cfg_log = logs_dir / cfg_name.replace(".yaml", "") / f"attempt_{attempt}.log"
    per_cfg_log.parent.mkdir(parents=True, exist_ok=True)

    rec = {
        "config_name": cfg_name,
        "config_path": str(cfg_path.resolve()),
        "attempt": attempt,
        "started_at": now_iso(),
        "ended_at": None,
        "duration_sec": None,
        "return_code": None,
        "status": "running",
        "success_marker": str(marker),
        "error": "",
        "log_path": str(per_cfg_log),
    }

    state["current"] = {"config_name": cfg_name, "attempt": attempt, "started_at": rec["started_at"]}
    state["status"] = "running"
    state["runs"].append(rec)
    state["updated_at"] = now_iso()
    atomic_write_json(state_file, state)
    write_summary_csv(summary_csv, state)

    cmd = [sys.executable, "start-pipelines.py", str(cfg_path.resolve())]
    append_master_log(master_log, f"START {cfg_name} attempt={attempt}")
    append_master_log(master_log, f"CMD {' '.join(cmd)}")

    start_ts = time.time()
    timed_out = False

    with per_cfg_log.open("a", encoding="utf-8") as lf:
        lf.write(f"[{now_iso()}] START attempt={attempt} cmd={' '.join(cmd)}\n")
        lf.flush()
        proc = subprocess.Popen(cmd, stdout=lf, stderr=subprocess.STDOUT, text=True)
        try:
            rc = proc.wait(timeout=timeout_sec)
        except subprocess.TimeoutExpired:
            timed_out = True
            proc.kill()
            rc = proc.wait()

    duration = int(time.time() - start_ts)

    rec["return_code"] = rc
    rec["ended_at"] = now_iso()
    rec["duration_sec"] = duration

    marker_ok = marker.exists()
    if timed_out:
        rec["status"] = "timeout"
        rec["error"] = f"Timed out after {timeout_sec}s"
    elif rc != 0:
        rec["status"] = "failed"
        rec["error"] = f"Non-zero exit code: {rc}"
    elif not marker_ok:
        rec["status"] = "failed"
        rec["error"] = f"Success marker missing: {marker}"
    else:
        rec["status"] = "completed"

    state["current"] = None
    state["updated_at"] = now_iso()
    atomic_write_json(state_file, state)
    write_summary_csv(summary_csv, state)

    append_master_log(
        master_log,
        f"END {cfg_name} attempt={attempt} status={rec['status']} rc={rc} duration_sec={duration} marker_ok={marker_ok}",
    )
    return rec


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run flagged 23 configs sequentially with resume/retry.")
    p.add_argument(
        "--config-dir",
        default="data_backup/config_redo/new/flagged_23_macmini",
        help="Directory containing *_macmini.yaml configs",
    )
    p.add_argument("--state-file", default="logs/batch_runs/flagged23_state.json")
    p.add_argument("--summary-csv", default="logs/batch_runs/flagged23_summary.csv")
    p.add_argument("--logs-dir", default="logs/batch_runs/flagged23")
    p.add_argument("--master-log", default="logs/batch_runs/flagged23_master.log")
    p.add_argument("--timeout-min", type=int, default=90)
    p.add_argument("--max-retries", type=int, default=1)
    p.add_argument("--start-at", default="", help="Config filename to start from")
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    config_dir = Path(args.config_dir)
    state_file = Path(args.state_file)
    summary_csv = Path(args.summary_csv)
    logs_dir = Path(args.logs_dir)
    master_log = Path(args.master_log)
    timeout_sec = int(args.timeout_min * 60)

    state = load_state(state_file)
    state["status"] = "running"
    state["updated_at"] = now_iso()
    atomic_write_json(state_file, state)

    append_master_log(master_log, "=" * 70)
    append_master_log(master_log, "Batch run starting")
    append_master_log(master_log, f"config_dir={config_dir.resolve()}")
    append_master_log(master_log, f"timeout_min={args.timeout_min} max_retries={args.max_retries}")

    run_list = RUN_ORDER[:]
    if args.start_at:
        if args.start_at not in run_list:
            append_master_log(master_log, f"ERROR start-at not found in run order: {args.start_at}")
            return 2
        run_list = run_list[run_list.index(args.start_at) :]

    missing = [name for name in run_list if not (config_dir / name).exists()]
    if missing:
        append_master_log(master_log, f"ERROR missing config files: {missing}")
        return 2

    if args.dry_run:
        append_master_log(master_log, "DRY RUN: would execute configs in this order:")
        for i, name in enumerate(run_list, start=1):
            append_master_log(master_log, f"  {i:02d}. {name}")
        state["status"] = "dry_run_completed"
        state["updated_at"] = now_iso()
        atomic_write_json(state_file, state)
        write_summary_csv(summary_csv, state)
        return 0

    should_stop = False

    def _sigint_handler(signum, frame):
        nonlocal should_stop
        should_stop = True
        append_master_log(master_log, f"Received signal {signum}. Will stop after current config.")

    signal.signal(signal.SIGINT, _sigint_handler)
    signal.signal(signal.SIGTERM, _sigint_handler)

    for idx, cfg_name in enumerate(run_list, start=1):
        if should_stop:
            break

        cfg_path = config_dir / cfg_name

        if is_completed(state, cfg_name):
            append_master_log(master_log, f"SKIP already completed: {cfg_name}")
            continue

        max_attempts = args.max_retries + 1
        done = False
        for _ in range(max_attempts):
            if should_stop:
                break
            rec = run_one(
                cfg_path=cfg_path,
                timeout_sec=timeout_sec,
                logs_dir=logs_dir,
                master_log=master_log,
                state=state,
                state_file=state_file,
                summary_csv=summary_csv,
            )
            if rec["status"] == "completed":
                done = True
                break
            if attempts_for(state, cfg_name) < max_attempts:
                append_master_log(master_log, f"RETRY scheduled for {cfg_name}")

        if not done:
            append_master_log(master_log, f"GIVE UP after {max_attempts} attempts: {cfg_name}")

        append_master_log(master_log, f"Progress {idx}/{len(run_list)}")

    latest = latest_by_config(state)
    statuses = [latest.get(name, {}).get("status", "not_started") for name in run_list]
    if all(s == "completed" for s in statuses):
        final_status = "completed"
        code = 0
    elif should_stop:
        final_status = "interrupted"
        code = 130
    else:
        final_status = "completed_with_failures"
        code = 1

    state["status"] = final_status
    state["current"] = None
    state["finished_at"] = now_iso()
    state["updated_at"] = now_iso()
    atomic_write_json(state_file, state)
    write_summary_csv(summary_csv, state)

    done_count = statuses.count("completed")
    fail_count = len([s for s in statuses if s in {"failed", "timeout"}])
    append_master_log(master_log, f"Batch finished: status={final_status} completed={done_count}/{len(run_list)} failed={fail_count}")

    return code


if __name__ == "__main__":
    raise SystemExit(main())
