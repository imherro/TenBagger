"""TASK 1 orchestration."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from tenbagger.config import DEFAULT_DATA_DIR, DEFAULT_REPORT_DIR
from tenbagger.data_loader import TenBaggerDataLoader
from tenbagger.reporting import build_task1_report
from tenbagger.storage import ParquetStorage


def run_task1(
    ts_codes: Iterable[str] | None = None,
    limit: int = 10,
    start_date: str | None = None,
    end_date: str | None = None,
    data_dir: Path | str = DEFAULT_DATA_DIR,
    report_dir: Path | str = DEFAULT_REPORT_DIR,
) -> dict:
    loader = TenBaggerDataLoader(start_date=start_date, end_date=end_date)
    load_result = loader.load_all(ts_codes=ts_codes, limit=limit)

    storage_result = ParquetStorage(data_dir).write(load_result.frame)
    storage = {
        "source": load_result.source,
        "requested_codes": load_result.requested_codes,
        "loaded_codes": load_result.loaded_codes,
        "by_stock_files": storage_result.by_stock_files,
        "by_date_root": storage_result.by_date_root,
        "row_count": storage_result.row_count,
        "load_errors": load_result.frame.attrs.get("load_errors", {}),
    }
    return build_task1_report(load_result.frame, storage, report_dir)
