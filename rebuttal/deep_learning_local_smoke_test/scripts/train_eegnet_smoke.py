#!/usr/bin/env python3
"""Train a compact EEGNet-inspired classifier on feature vectors."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from dl_smoke_common import (
    binary_metrics,
    finite_metrics,
    load_npz,
    require_torch,
    save_run_outputs,
    set_seed,
    split_indices,
    standardize_train_test,
    subject_majority_accuracy,
)


def factor_shape(n_features: int) -> tuple[int, int]:
    rows = int(np.floor(np.sqrt(n_features)))
    while rows > 1 and n_features % rows != 0:
        rows -= 1
    return rows, n_features // rows


def build_model(torch, n_features: int):
    rows, cols = factor_shape(n_features)

    class EEGNetFeatureSmoke(torch.nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.rows = rows
            self.cols = cols
            self.net = torch.nn.Sequential(
                torch.nn.Conv2d(1, 8, kernel_size=(1, 5), padding=(0, 2), bias=False),
                torch.nn.BatchNorm2d(8),
                torch.nn.ELU(),
                torch.nn.Conv2d(8, 16, kernel_size=(rows, 1), groups=8, bias=False),
                torch.nn.BatchNorm2d(16),
                torch.nn.ELU(),
                torch.nn.AvgPool2d(kernel_size=(1, 2)),
                torch.nn.Dropout(0.25),
                torch.nn.Conv2d(16, 16, kernel_size=(1, 3), padding=(0, 1), groups=16, bias=False),
                torch.nn.Conv2d(16, 16, kernel_size=1, bias=False),
                torch.nn.BatchNorm2d(16),
                torch.nn.ELU(),
                torch.nn.AdaptiveAvgPool2d((1, 1)),
                torch.nn.Flatten(),
                torch.nn.Linear(16, 2),
            )

        def forward(self, x):
            return self.net(x.view(x.shape[0], 1, self.rows, self.cols))

    return EEGNetFeatureSmoke(), {"feature_tensor_shape": [1, rows, cols]}


def run(args: argparse.Namespace) -> None:
    torch = require_torch()
    set_seed(args.seed)
    data = load_npz(args.data)
    x = data["x"]
    y = data["y"]
    subjects = data["SubjectID"]
    epochs = data["EpochID"]
    meta = json.loads(str(data["meta"].item()))

    train_idx, test_idx, split_info = split_indices(y, subjects, args.split, args.seed)
    x_train, x_test = standardize_train_test(x, train_idx, test_idx)
    y_train = y[train_idx]
    y_test = y[test_idx]

    model, model_info = build_model(torch, x.shape[1])
    optimizer = torch.optim.Adam(model.parameters(), lr=args.learning_rate)
    loss_fn = torch.nn.CrossEntropyLoss()
    train_ds = torch.utils.data.TensorDataset(torch.from_numpy(x_train), torch.from_numpy(y_train))
    train_loader = torch.utils.data.DataLoader(train_ds, batch_size=args.batch_size, shuffle=True)

    log = {
        "epochs": [],
        "model_info": model_info,
        "note": "Feature-vector EEGNet-style smoke test, not canonical raw-signal EEGNet.",
    }
    for epoch in range(1, args.epochs + 1):
        model.train()
        total_loss = 0.0
        total_correct = 0
        total = 0
        for xb, yb in train_loader:
            optimizer.zero_grad()
            logits = model(xb)
            loss = loss_fn(logits, yb)
            loss.backward()
            optimizer.step()
            total_loss += float(loss.item()) * len(yb)
            total_correct += int((logits.argmax(dim=1) == yb).sum().item())
            total += int(len(yb))
        log["epochs"].append({"epoch": epoch, "loss": total_loss / total, "accuracy": total_correct / total})

    model.eval()
    with torch.no_grad():
        logits = model(torch.from_numpy(x_test))
        probs = torch.softmax(logits, dim=1)[:, 1].numpy()
        pred = logits.argmax(dim=1).numpy()

    metrics = binary_metrics(y_test, pred)
    metrics["subject_majority_accuracy"] = subject_majority_accuracy(y_test, pred, subjects[test_idx])
    metrics.update(
        {
            "run_id": f"eegnet_feature_smoke_{args.split}",
            "model": "eegnet_feature_smoke",
            "split": args.split,
            **{k: split_info[k] for k in ["train_rows", "test_rows", "train_subject_count", "test_subject_count", "shared_subject_count"]},
            "epochs": args.epochs,
            "batch_size": args.batch_size,
            "feature_dim": int(x.shape[1]),
        }
    )
    finite_metrics(metrics)

    predictions = [
        {
            "row_index": int(i),
            "SubjectID": str(subjects[i]),
            "EpochID": str(epochs[i]),
            "true_label": int(y[i]),
            "pred_label": int(p),
            "prob_class_1": float(prob),
        }
        for i, p, prob in zip(test_idx, pred, probs)
    ]
    save_run_outputs(metrics["run_id"], metrics, predictions, split_info, log, meta)
    print(json.dumps(metrics, indent=2, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, type=Path)
    parser.add_argument("--split", required=True, choices=["subject_disjoint_smoke", "subject_overlap_smoke"])
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    parser.add_argument("--seed", type=int, default=42)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
