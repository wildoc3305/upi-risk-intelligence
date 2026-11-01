"""Audit the transaction CSV before feature engineering or model training.

Run from the repository root:
    python -m src.data.inspect_dataset
or:
    python -m src.data.inspect_dataset --csv "D:\\path\\to\\dataset.csv"

This script reports dataset quality; it does not train a model.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CSV = PROJECT_ROOT / "data" / "raw" / "indian_banking_transactions.csv"
REPORTS_DIR = PROJECT_ROOT / "reports"

REQUIRED_COLUMNS = {
    "transaction_id",
    "customer_id",
    "transaction_date",
    "transaction_time",
    "transaction_type",
    "transaction_amount",
    "is_fraud",
}


def _percent(rate: float) -> float:
    """Convert a proportion into a percentage rounded to three decimals."""
    return round(float(rate) * 100, 3)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit the UPI Risk Intelligence transaction dataset."
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=DEFAULT_CSV,
        help=f"CSV path (default: {DEFAULT_CSV})",
    )
    args = parser.parse_args()
    csv_path = args.csv.expanduser().resolve()

    if not csv_path.is_file():
        raise FileNotFoundError(
            f"Dataset not found: {csv_path}\n"
            "Place it at data/raw/indian_banking_transactions.csv or pass --csv."
        )

    # Read the source once so every statistic is based on the same file snapshot.
    df = pd.read_csv(csv_path)

    missing_required = sorted(REQUIRED_COLUMNS - set(df.columns))
    if missing_required:
        raise ValueError(
            "Missing required columns: " + ", ".join(missing_required)
        )

    target_values = df["is_fraud"].dropna().unique().tolist()
    is_binary_target = set(target_values).issubset({0, 1, False, True})
    if not is_binary_target:
        raise ValueError(
            "is_fraud must use binary labels 0 and 1. "
            f"Found values: {target_values[:10]}"
        )

    upi_mask = (
        df["transaction_type"].astype("string").str.strip().str.upper().eq("UPI")
    )
    upi_df = df.loc[upi_mask]

    missing = df.isna().sum().sort_values(ascending=False)
    overall_rate = float(df["is_fraud"].mean())
    upi_rate = float(upi_df["is_fraud"].mean()) if not upi_df.empty else None

    fraud_counts = df["is_fraud"].value_counts(dropna=False).to_dict()
    summary = {
        "source_file": str(csv_path),
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": df.columns.tolist(),
        "fraud_label_counts": {
            str(key): int(value) for key, value in fraud_counts.items()
        },
        "overall_fraud_rate_percent": _percent(overall_rate),
        "upi_rows": int(len(upi_df)),
        "upi_fraud_label_counts": {
            str(key): int(value)
            for key, value in upi_df["is_fraud"].value_counts(dropna=False).items()
        },
        "upi_fraud_rate_percent": (
            _percent(upi_rate) if upi_rate is not None else None
        ),
        "fully_duplicated_rows": int(df.duplicated().sum()),
        "duplicate_transaction_ids": int(df["transaction_id"].duplicated().sum()),
        "missing_values_by_column": {
            str(key): int(value) for key, value in missing.items()
        },
        "dtypes": {str(key): str(value) for key, value in df.dtypes.items()},
    }

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "dataset_audit.json").write_text(
        json.dumps(summary, indent=2, default=str),
        encoding="utf-8",
    )

    # These grouped rates are descriptive only; they do not establish predictive power.
    group_columns = [
        ("transaction_type", "fraud_rate_by_transaction_type.csv"),
        ("channel", "fraud_rate_by_channel.csv"),
        ("transaction_hour", "fraud_rate_by_hour.csv"),
    ]
    for column, filename in group_columns:
        if column not in df.columns:
            continue
        grouped = (
            df.groupby(column, dropna=False)["is_fraud"]
            .agg(transaction_count="size", fraud_count="sum", fraud_rate="mean")
            .reset_index()
        )
        grouped["fraud_rate_percent"] = (grouped["fraud_rate"] * 100).round(3)
        grouped.sort_values("fraud_rate", ascending=False).to_csv(
            REPORTS_DIR / filename, index=False
        )

    print("\n=== DATASET READINESS AUDIT ===")
    print(f"File: {csv_path}")
    print(f"Shape: {df.shape[0]:,} rows x {df.shape[1]} columns")
    print(f"Fully duplicated rows: {summary['fully_duplicated_rows']:,}")
    print(f"Duplicate transaction IDs: {summary['duplicate_transaction_ids']:,}")
    print(f"UPI rows: {len(upi_df):,}")
    print(f"Overall fraud rate: {_percent(overall_rate):.3f}%")
    if upi_rate is not None:
        print(f"UPI fraud rate: {_percent(upi_rate):.3f}%")

    print("\nFraud label counts:")
    print(df["is_fraud"].value_counts(dropna=False).to_string())
    print("\nColumns with missing values:")
    nonzero_missing = missing[missing > 0]
    print(nonzero_missing.to_string() if not nonzero_missing.empty else "None")
    print(f"\nAudit reports written to: {REPORTS_DIR}")
    print("Review these findings before selecting model features.")


if __name__ == "__main__":
    main()
