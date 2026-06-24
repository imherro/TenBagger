# TASK 2 Result

TASK 2 implements the Factor Engine for the TenBagger system.

## Implemented

- `FactorEngine` with explicit methods:
  - `compute_value_factors()`
  - `compute_growth_factors()`
  - `compute_quality_factors()`
  - `compute_risk_factors()`
- Cross-sectional percentile ranking by date.
- TenBagger score V1:
  - 0.30 growth
  - 0.25 industry placeholder
  - 0.25 quality
  - 0.15 valuation
  - 0.05 momentum
- Output columns:
  `ts_code`, `date`, `value_score`, `growth_score`, `quality_score`,
  `risk_score`, `tenbagger_score`.
- Factor parquet storage:
  - `data/factors/by_date/`
  - `data/factors/by_stock/`
- Validation for:
  - future leak rows
  - NaN score cells
  - non-flat score distribution
- Web dashboard support for factor validation and latest factor scores.
- Tests for factor output schema, score ranges, non-flat distribution, and
  future-leak validation.

## Validation Run

Command:

```powershell
python scripts/run_task2.py
```

Result:

```json
{
  "stock_count": 10,
  "row_count": 8390,
  "date_range": {
    "start": "2023-01-03",
    "end": "2026-06-24"
  },
  "latest_trading_date": "2026-06-24",
  "validation": {
    "future_leak_rows": 0,
    "nan_cells": 0,
    "score_std": 9.358743930327051,
    "score_min": 32.25,
    "score_max": 82.0833
  }
}
```

Latest top scores:

```text
000651.SZ  tenbagger=70.50  growth=100.00 quality=80.00 value=40.00 risk=20.00 momentum=40.00
000858.SZ  tenbagger=67.58  growth=85.00  quality=53.33 value=75.00 risk=40.00 momentum=100.00
002594.SZ  tenbagger=67.42  growth=65.00  quality=86.67 value=75.00 risk=70.00 momentum=50.00
002415.SZ  tenbagger=65.58  growth=85.00  quality=63.33 value=75.00 risk=90.00 momentum=10.00
600887.SH  tenbagger=57.92  growth=65.00  quality=56.67 value=55.00 risk=50.00 momentum=70.00
```

Test command:

```powershell
python -m pytest -q
```

Result:

```text
4 passed
```
