"""Factor parquet storage and reporting."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

from tenbagger.config import DEFAULT_DATA_DIR, DEFAULT_REPORT_DIR
from tenbagger.factor_engine import FACTOR_COLUMNS, FactorValidation


@dataclass(frozen=True)
class FactorStorageResult:
    by_date_root: str
    by_stock_files: list[str]
    row_count: int


class FactorStorage:
    def __init__(self, root: Path | str = DEFAULT_DATA_DIR) -> None:
        self.root = Path(root)
        self.by_date_dir = self.root / "factors" / "by_date"
        self.by_stock_dir = self.root / "factors" / "by_stock"

    def write(self, factors: pd.DataFrame) -> FactorStorageResult:
        if factors.empty:
            raise ValueError("Cannot write empty factor dataframe.")

        self.by_date_dir.mkdir(parents=True, exist_ok=True)
        self.by_stock_dir.mkdir(parents=True, exist_ok=True)

        normalized = factors.copy()
        normalized["date"] = normalized["date"].astype(str)

        normalized.to_parquet(
            self.by_date_dir,
            index=False,
            partition_cols=["date"],
            engine="pyarrow",
        )

        by_stock_files: list[str] = []
        for ts_code, stock_df in normalized.groupby("ts_code", sort=True):
            path = self.by_stock_dir / f"{str(ts_code).replace('.', '_')}.parquet"
            stock_df.sort_values("date").to_parquet(path, index=False)
            by_stock_files.append(str(path))

        return FactorStorageResult(
            by_date_root=str(self.by_date_dir),
            by_stock_files=by_stock_files,
            row_count=len(normalized),
        )


def build_task2_report(
    factors: pd.DataFrame,
    validation: FactorValidation,
    storage: FactorStorageResult,
    report_dir: Path | str = DEFAULT_REPORT_DIR,
    universe: dict[str, Any] | None = None,
) -> dict[str, Any]:
    report_path = Path(report_dir)
    report_path.mkdir(parents=True, exist_ok=True)

    latest_date = str(factors["date"].max())
    latest = factors[factors["date"] == latest_date].sort_values(
        "tenbagger_score",
        ascending=False,
    )
    score_columns = [column for column in FACTOR_COLUMNS if column.endswith("_score")]

    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "task": "TASK 2 - Factor Engine",
        "stock_count": int(factors["ts_code"].nunique()),
        "row_count": int(len(factors)),
        "date_range": {
            "start": str(factors["date"].min()),
            "end": str(factors["date"].max()),
        },
        "latest_trading_date": latest_date,
        "universe": universe or {},
        "validation": asdict(validation),
        "score_distribution": {
            column: {
                "min": float(factors[column].min()),
                "max": float(factors[column].max()),
                "mean": float(factors[column].mean()),
                "std": float(factors[column].std(ddof=0) or 0),
            }
            for column in score_columns
        },
        "latest_top_scores": latest[FACTOR_COLUMNS].head(20).to_dict(orient="records"),
        "storage": {
            "by_date_root": storage.by_date_root,
            "by_stock_files": storage.by_stock_files,
            "row_count": storage.row_count,
        },
    }

    (report_path / "task2_factor_summary.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    markdown = [
        "# TASK 2 Factor Report",
        "",
        f"- Generated at: {report['generated_at']}",
        f"- Stock count: {report['stock_count']}",
        f"- Row count: {report['row_count']}",
        f"- Date range: {report['date_range']['start']} to {report['date_range']['end']}",
        f"- Latest trading date: {report['latest_trading_date']}",
        f"- Future leak rows: {validation.future_leak_rows}",
        f"- NaN score cells: {validation.nan_cells}",
        f"- TenBagger score std: {validation.score_std:.4f}",
        "",
        "## Latest Top Scores",
        "",
    ]
    for row in report["latest_top_scores"][:10]:
        markdown.append(
            "- {ts_code}: tenbagger={tenbagger_score:.2f}, growth={growth_score:.2f}, quality={quality_score:.2f}, value={value_score:.2f}, risk={risk_score:.2f}".format(
                **row
            )
        )

    (report_path / "task2_factor_summary.md").write_text(
        "\n".join(markdown) + "\n",
        encoding="utf-8",
    )
    return report
