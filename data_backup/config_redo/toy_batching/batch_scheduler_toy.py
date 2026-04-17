from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SubjectItem:
    subject_id: str
    size_mb: float


def schedule_batches_ffd(
    items: List[SubjectItem],
    target_batch_mb: float,
    max_subjects_per_batch: Optional[int] = None,
) -> List[List[SubjectItem]]:
    """First-Fit Decreasing: sort large->small, place each item in first fitting batch."""
    if target_batch_mb <= 0:
        raise ValueError("target_batch_mb must be > 0")

    sorted_items = sorted(items, key=lambda x: x.size_mb, reverse=True)
    batches: List[List[SubjectItem]] = []
    batch_totals: List[float] = []

    for item in sorted_items:
        placed = False

        for i, batch in enumerate(batches):
            total = batch_totals[i]
            room_ok = (total + item.size_mb) <= target_batch_mb
            count_ok = True if max_subjects_per_batch is None else len(batch) < max_subjects_per_batch
            if room_ok and count_ok:
                batch.append(item)
                batch_totals[i] += item.size_mb
                placed = True
                break

        if not placed:
            # singleton batch for oversized subject is allowed
            batches.append([item])
            batch_totals.append(item.size_mb)

    return batches


def print_batches(title: str, batches: List[List[SubjectItem]], target_mb: float) -> None:
    print(f"\n=== {title} ===")
    print(f"target_batch_mb={target_mb}")
    print(f"num_batches={len(batches)}")
    for i, b in enumerate(batches, start=1):
        total = sum(x.size_mb for x in b)
        ids = [x.subject_id for x in b]
        warn = "  <-- OVERSIZED SINGLETON" if total > target_mb and len(b) == 1 else ""
        print(f"batch_{i:02d}: total={total:7.2f} MB | n={len(b):2d} | {ids}{warn}")


def scenario_synthetic() -> None:
    # intentionally skewed
    sizes = [52, 49, 44, 40, 39, 35, 31, 31, 30, 28, 24, 20, 18, 12]
    items = [SubjectItem(f"sub-{i+1:03d}", s) for i, s in enumerate(sizes)]
    batches = schedule_batches_ffd(items, target_batch_mb=120, max_subjects_per_batch=5)
    print_batches("Synthetic skewed set", batches, target_mb=120)


def scenario_realish() -> None:
    # resembles your raw distribution-ish
    sizes = [49.3,44.2,41.2,38.8,38.7,37.6,37.2,37.1,36.1,35.6,34.8,34.2,33.5,32.9,32.0,31.1,30.8,30.1,29.4,28.6,27.8,26.9,25.7,24.8,23.6,21.1,18.3,11.8]
    items = [SubjectItem(f"sub-{i+1:03d}", s) for i, s in enumerate(sizes)]
    batches = schedule_batches_ffd(items, target_batch_mb=160, max_subjects_per_batch=6)
    print_batches("Real-ish 28-subject example", batches, target_mb=160)


def scenario_oversized_singleton() -> None:
    sizes = [210, 80, 72, 67, 50, 45, 43]
    items = [SubjectItem(f"sub-{i+1:03d}", s) for i, s in enumerate(sizes)]
    batches = schedule_batches_ffd(items, target_batch_mb=160, max_subjects_per_batch=4)
    print_batches("Oversized singleton case", batches, target_mb=160)


if __name__ == "__main__":
    scenario_synthetic()
    scenario_realish()
    scenario_oversized_singleton()
