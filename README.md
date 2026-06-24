# TenBagger

TenBagger is a local A-share research system for building a verifiable
structural tenbagger screening pipeline.

Current milestones:

- TASK 1: data layer and stock universe construction.
- TASK 2: factor engine and cross-sectional structural scores.

## TASK 1 Scope

- Unified `TenBaggerDataLoader` interface.
- TuShare primary data ingestion for stock basics, daily bars, daily valuation,
  income, cash flow, and ROE data.
- Placeholder multi-source methods for BaoStock, QMT positions, and yfinance.
- Standard dataframe schema:
  `ts_code`, `date`, `open`, `high`, `low`, `close`, `revenue`, `net_profit`,
  `roe`, `pe`, `pb`, `market_cap`.
- Parquet storage by stock and by date partition.
- Local task report with stock count, coverage, missing-rate stats, and latest
  trading snapshot.
- Web display on port `8020`.

## Setup

Create a local `.env` file with:

```text
TUSHARE_TOKEN=your_token
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Run TASK 1

```powershell
python scripts/run_task1.py --limit 10 --start-date 20230101
```

Generated parquet files are written under `data/parquet/` and reports under
`reports/`. Both folders are local runtime outputs and are not committed.

## Web Display

```powershell
python scripts/serve_web.py --port 8020
```

Then open:

```text
http://127.0.0.1:8020
```

The dashboard reads local TASK 1 and TASK 2 reports when they exist.

## Run TASK 2

Run TASK 1 first, then:

```powershell
python scripts/run_task2.py
```

TASK 2 writes factor parquet files under `data/factors/` and the factor report
under `reports/task2_factor_summary.json`.

## Tests

```powershell
python -m pytest -q
```
