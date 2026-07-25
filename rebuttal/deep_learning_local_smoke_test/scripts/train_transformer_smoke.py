#!/usr/bin/env python3
"""Train a small transformer encoder classifier on feature chunks."""

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


def build_model(torch, n_features: int, chunk_size: int, embed_dim: int, heads: int):
    n_tokens = int(np.ceil(n_features / chunk_size))
    padded_dim = n_tokens * chunk_size

    class TransformerFeatureSmoke(torch.nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.pad = padded_dim - n_features
            self.n_tokens = n_tokens
            self.chunk_size = chunk_size
            self.proj = torch.nn.Linear(chunk_size, embed_dim)
            encoder_layer = torch.nn.TransformerEncoderLayer(
                d_model=embed_dim,
                nhead=heads,
                dim_feedforward=embed_dim * 2,
                dropout=0.1,
                activation="gelu",
                batch_first=True,
            )
            self.encoder = torch.nn.TransformerEncoder(encoder_layer, num_layers=1)
            self.classifier = torch.nn.Sequential(
                torch.nn.LayerNorm(embed_dim),
                torch.nn.Linear(embed_dim, 2),
            )

        def forward(self, x):
            if self.pad:
                x = torch.nn.functional.pad(x, (0, self.pad))
            x = x.view(x.shape[0], self.n_tokens, self.chunk_size)
            tokens = self.proj(x)
            encoded = self.encoder(tokens)
            return self.classifier(encoded.mean(dim=1))

    return TransformerFeatureSmoke(), {"n_tokens": n_tokens, "chunk_size": chunk_size, "embed_dim": embed_dim}


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

    model, model_info = build_model(torch, x.shape[1], args.chunk_size, args.embed_dim, args.heads)
    optimizer = torch.optim.Adam(model.parameters(), lr=args.learning_rate)
    loss_fn = torch.nn.CrossEntropyLoss()
    train_ds = torch.utils.data.TensorDataset(torch.from_numpy(x_train), torch.from_numpy(y_train))
    train_loader = torch.utils.data.DataLoader(train_ds, batch_size=args.batch_size, shuffle=True)

    log = {
        "epochs": [],
        "model_info": model_info,
        "note": "Small feature-token transformer smoke test, not a full raw-signal transformer baseline.",
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
            "run_id": f"transformer_feature_smoke_{args.split}",
            "model": "transformer_feature_smoke",
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
    parser.add_argument("--chunk-size", type=int, default=8)
    parser.add_argument("--embed-dim", type=int, default=32)
    parser.add_argument("--heads", type=int, default=4)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
