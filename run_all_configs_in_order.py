#!/usr/bin/env python3
"""Run start-pipelines.py sequentially for a folder of YAML configs."""

from __future__ import annotations

import argparse
import csv
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from subprocess import PIPE, STDOUT, Popen
from typing import Iterable, List


def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@dataclass
class RunRecord:
    index: int
    total: int
    config: str
    status: str
    return_code: int
    duration_sec: int
    log_path: str
    started_at: str
    ended_at: str


def discover_configs(config_root: Path, recursive: bool) -> List[Path]:
    pattern_iter: Iterable[Path]
    if recursive:
        pattern_iter = config_root.rglob("*.yaml")
    else:
        pattern_iter = config_root.glob("*.yaml")

    configs = [p.resolve() for p in pattern_iter if p.is_file()]
    configs.sort(key=lambda p: p.as_posix())
    return configs


def resolve_start_index(configs: List[Path], start_at: str) -> int:
    if not start_at:
        return 0

    # Accept either a full path, a relative suffix, or plain filename.
    for idx, cfg in enumerate(configs):
        if cfg.as_posix() == start_at:
            return idx
        if cfg.as_posix().endswith(start_at):
            return idx
        if cfg.name == start_at:
            return idx

    raise ValueError(f"--start-at not found: {start_at}")


def stream_command_to_console_and_log(cmd: List[str], log_file: Path) -> int:
    proc = Popen(cmd, stdout=PIPE, stderr=STDOUT, text=True, bufsize=1)

    assert proc.stdout is not None
    with log_file.open("w", encoding="utf-8") as lf:
        lf.write(f"[{now_str()}] CMD: {' '.join(cmd)}\n")
        lf.flush()
        for line in proc.stdout:
            print(line, end="")
            lf.write(line)
        rc = proc.wait()
        lf.write(f"\n[{now_str()}] EXIT CODE: {rc}\n")

    return rc


def write_summary(summary_csv: Path, rows: List[RunRecord]) -> None:
    summary_csv.parent.mkdir(parents=True, exist_ok=True)
    with summary_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "index",
                "total",
                "config",
                "status",
                "return_code",
                "duration_sec",
                "started_at",
                "ended_at",
                "log_path",
            ]
        )
        for r in rows:
            writer.writerow(
                [
                    r.index,
                    r.total,
                    r.config,
                    r.status,
                    r.return_code,
                    r.duration_sec,
                    r.started_at,
                    r.ended_at,
                    r.log_path,
                ]
            )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Run start-pipelines.py sequentially for every YAML config."
    )
    p.add_argument(
        "--config-root",
        default="configs_ftd_vs_cntrl_google_cloud",
        help="Folder containing YAML configs",
    )
    p.add_argument(
        "--recursive",
        action="store_true",
        default=True,
        help="Search config-root recursively (default: true)",
    )
    p.add_argument(
        "--non-recursive",
        action="store_true",
        help="Search only top-level of config-root",
    )
    p.add_argument(
        "--start-at",
        default="",
        help="Start from this config (filename, suffix, or full path)",
    )
    p.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Run only first N configs after start-at (0 = all)",
    )
    p.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Keep running even if a config fails",
    )
    p.add_argument(
        "--sleep-sec",
        type=int,
        default=0,
        help="Optional pause between runs",
    )
    p.add_argument(
        "--python-bin",
        default=sys.executable,
        help="Python executable used to call start-pipelines.py",
    )
    p.add_argument(
        "--start-script",
        default="start-pipelines.py",
        help="Path to start-pipelines.py",
    )
    p.add_argument(
        "--logs-dir",
        default="logs/config_batch_runner",
        help="Directory for per-config logs",
    )
    p.add_argument(
        "--summary-csv",
        default="logs/config_batch_runner/summary.csv",
        help="Summary CSV output path",
    )
    p.add_argument("--dry-run", action="store_true", help="Print order, do not execute")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    recursive = not args.non_recursive

    config_root = Path(args.config_root).resolve()
    start_script = Path(args.start_script).resolve()
    logs_dir = Path(args.logs_dir).resolve()
    summary_csv = Path(args.summary_csv).resolve()

    if not config_root.exists():
        print(f"ERROR: config root not found: {config_root}")
        return 2
    if not start_script.exists():
        print(f"ERROR: start script not found: {start_script}")
        return 2

    configs = discover_configs(config_root, recursive=recursive)
    if not configs:
        print(f"ERROR: no .yaml files found under {config_root}")
        return 2

    start_idx = resolve_start_index(configs, args.start_at)
    configs = configs[start_idx:]

    if args.limit and args.limit > 0:
        configs = configs[: args.limit]

    print(f"[{now_str()}] Found {len(configs)} configs to run")
    for i, cfg in enumerate(configs, start=1):
        print(f"  {i:03d}. {cfg}")

    if args.dry_run:
        return 0

    logs_dir.mkdir(parents=True, exist_ok=True)

    rows: List[RunRecord] = []
    total = len(configs)

    try:
        for idx, cfg in enumerate(configs, start=1):
            started_at = now_str()
            cfg_slug = cfg.stem.replace("/", "_")
            log_file = logs_dir / f"{idx:03d}_{cfg_slug}.log"

            print(f"\n[{started_at}] RUN {idx}/{total}: {cfg}")
            cmd = [args.python_bin, str(start_script), str(cfg)]
            t0 = time.time()
            rc = stream_command_to_console_and_log(cmd, log_file)
            duration = int(time.time() - t0)
            ended_at = now_str()

            status = "completed" if rc == 0 else "failed"
            print(
                f"[{ended_at}] {status.upper()} {idx}/{total} rc={rc} duration={duration}s log={log_file}"
            )

            rows.append(
                RunRecord(
                    index=idx,
                    total=total,
                    config=str(cfg),
                    status=status,
                    return_code=rc,
                    duration_sec=duration,
                    log_path=str(log_file),
                    started_at=started_at,
                    ended_at=ended_at,
                )
            )
            write_summary(summary_csv, rows)

            if rc != 0 and not args.continue_on_error:
                print("Stopping due to failure (use --continue-on-error to keep going).")
                return 1

            if args.sleep_sec > 0 and idx < total:
                time.sleep(args.sleep_sec)
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        write_summary(summary_csv, rows)
        return 130

    failed = [r for r in rows if r.status != "completed"]
    print(
        f"\n[{now_str()}] Finished. completed={len(rows) - len(failed)}/{len(rows)} failed={len(failed)}"
    )
    print(f"Summary: {summary_csv}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
