# TenBagger

TenBagger is a local A-share research system for building a verifiable
structural tenbagger screening pipeline.

Current milestones:

- TASK 1: data layer and stock universe construction.
- TASK 2: factor engine and cross-sectional structural scores.
- TASK 3: hard-filter screener and alpha validation.
- TASK 4: portfolio simulation backtest.
- TASK 5: factor neutralization and walk-forward weight optimization.
- TASK 6: alpha monetization and execution optimization.
- TASK 7: structural alpha validation and final alpha classification.
- TASK 8: market regime and behavioral state engine.
- TASK 9: market behavior and flow pressure engine.
- TASK 10: market structure decomposition engine.
- TASK 11: market structural anomaly detection engine.

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

## Run TASK 3

Run TASK 1 and TASK 2 first, then:

```powershell
python scripts/run_task3.py
```

TASK 3 writes screener parquet files under `data/screener/` and the screener
report under `reports/task3_screener_summary.json`.

## Run TASK 4

Run TASK 1 through TASK 3 first, then:

```powershell
python scripts/run_task4.py --top-k 10 --weight-mode score
```

TASK 4 writes portfolio NAV, holdings, and factor attribution parquet files
under `data/backtest/` and the backtest report under
`reports/task4_backtest_summary.json`.

## Run TASK 5

Run TASK 1 through TASK 4 first, then:

```powershell
python scripts/run_task5.py
```

TASK 5 writes the optimization report under
`reports/task5_optimization_summary.json`.

## Run TASK 6

Run TASK 1 through TASK 5 first, then:

```powershell
python scripts/run_task6.py
```

TASK 6 writes the monetization report under
`reports/task6_monetization_summary.json`.

## Run TASK 7

Run TASK 1 through TASK 6 first, then:

```powershell
python scripts/run_task7.py
```

TASK 7 writes the structural alpha validation report under
`reports/task7_structural_validation_summary.json`. The output classifies the
system as `REAL`, `PSEUDO`, or `NO ALPHA`.

## Run TASK 8

Run TASK 1 first so local market data exists, then:

```powershell
python scripts/run_task8.py
```

TASK 8 writes market regime reports under `reports/` and daily regime data under
`data/regime/`. It adds `GET /api/task8/regime` and a Market Regime Dashboard on
the local web display.

## Run TASK 9

Run TASK 8 first, then:

```powershell
python scripts/run_task9.py
```

TASK 9 writes behavioral flow reports under `reports/` and daily behavior data
under `data/behavior/`. It adds `GET /api/task9/behavior` and a Behavioral Flow
Dashboard on the local web display.

## Run TASK 10

Run TASK 9 first, then:

```powershell
python scripts/run_task10.py
```

TASK 10 writes market structure reports under `reports/` and daily structure
data under `data/structure/`. It adds `GET /api/task10/structure` and a Market
Structure Dashboard on the local web display.

## Run TASK 11

Run TASK 10 first, then:

```powershell
python scripts/run_task11.py
```

TASK 11 writes anomaly reports under `reports/` and daily anomaly data under
`data/anomaly/`. It adds `GET /api/task11/anomaly` and a Structural Anomaly
Dashboard on the local web display.

## Tests

```powershell
python -m pytest -q
```
