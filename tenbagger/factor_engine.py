"""Factor engine for TASK 2."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from tenbagger.config import DEFAULT_DATA_DIR
from tenbagger.schema import ensure_standard_schema


FACTOR_COLUMNS = [
    "ts_code",
    "date",
    "value_score",
    "growth_score",
    "quality_score",
    "risk_score",
    "momentum_score",
    "industry_score",
    "tenbagger_score",
]


@dataclass(frozen=True)
class FactorValidation:
    future_leak_rows: int
    nan_cells: int
    score_std: float
    score_min: float
    score_max: float


class FactorEngine:
    """Compute cross-sectional TenBagger factors from TASK 1 data."""

    def __init__(self, neutral_score: float = 50.0) -> None:
        self.neutral_score = neutral_score

    @classmethod
    def read_task1_parquet(cls, data_dir: Path | str = DEFAULT_DATA_DIR) -> pd.DataFrame:
        by_stock = Path(data_dir) / "parquet" / "by_stock"
        if not by_stock.exists():
            raise FileNotFoundError(f"TASK 1 by-stock parquet directory not found: {by_stock}")

        frames = [pd.read_parquet(path) for path in sorted(by_stock.glob("*.parquet"))]
        if not frames:
            raise FileNotFoundError(f"No TASK 1 parquet files found under: {by_stock}")
        return ensure_standard_schema(pd.concat(frames, ignore_index=True))

    def compute(self, df: pd.DataFrame) -> pd.DataFrame:
        """Return a complete factor dataframe with no score NaN propagation."""

        data = ensure_standard_schema(df)
        data = data.copy()
        data["date"] = pd.to_datetime(data["date"], errors="coerce")
        data = data.dropna(subset=["ts_code", "date"]).sort_values(["ts_code", "date"])

        for column in ["close", "revenue", "net_profit", "roe", "pe", "pb", "market_cap", "debt_ratio"]:
            data[column] = pd.to_numeric(data[column], errors="coerce")

        data = self._add_time_series_features(data)
        data = self._add_cross_sectional_scores(data)
        data["tenbagger_score"] = (
            0.35 * data["growth_score"]
            + 0.25 * data["quality_score"]
            + 0.15 * data["value_score"]
            + 0.10 * data["industry_score"]
            + 0.10 * data["momentum_score"]
            + 0.05 * data["risk_score"]
        )
        data["tenbagger_score"] = data["tenbagger_score"].clip(0, 100).round(4)

        output_columns = FACTOR_COLUMNS + [
            "revenue_growth_yoy",
            "net_profit_growth_yoy",
            "roe_trend_yoy",
            "profit_margin",
            "volatility_60d",
            "max_drawdown_120d",
            "momentum_1m",
            "momentum_3m",
            "momentum_6m",
            "momentum_120d",
            "industry",
            "industry_growth_score",
            "industry_valuation_score",
            "industry_flow_score",
            "pe",
            "pb",
            "roe",
            "market_cap",
            "debt_ratio",
            "ann_date",
            "report_period",
        ]
        for column in output_columns:
            if column not in data.columns:
                data[column] = pd.NA

        result = data[output_columns].copy()
        result["date"] = result["date"].dt.strftime("%Y-%m-%d")

        score_columns = [column for column in FACTOR_COLUMNS if column.endswith("_score")]
        result[score_columns] = result[score_columns].fillna(self.neutral_score).clip(0, 100).round(4)
        result = result.fillna(
            {
                "revenue_growth_yoy": 0.0,
                "net_profit_growth_yoy": 0.0,
                "roe_trend_yoy": 0.0,
                "profit_margin": 0.0,
                "volatility_60d": 0.0,
                "max_drawdown_120d": 0.0,
                "momentum_1m": 0.0,
                "momentum_3m": 0.0,
                "momentum_6m": 0.0,
                "momentum_120d": 0.0,
                "debt_ratio": 0.0,
            }
        )
        return result.sort_values(["date", "tenbagger_score", "ts_code"], ascending=[True, False, True])

    def validate(self, factors: pd.DataFrame) -> FactorValidation:
        score_columns = [column for column in FACTOR_COLUMNS if column.endswith("_score")]
        future_leak_rows = 0
        if {"date", "ann_date"}.issubset(factors.columns):
            dates = pd.to_datetime(factors["date"], errors="coerce")
            ann_dates = pd.to_datetime(factors["ann_date"], format="%Y%m%d", errors="coerce")
            future_leak_rows = int((ann_dates.notna() & dates.notna() & (ann_dates > dates)).sum())

        nan_cells = int(factors[score_columns].isna().sum().sum())
        score_std = float(factors["tenbagger_score"].std(ddof=0) or 0)
        return FactorValidation(
            future_leak_rows=future_leak_rows,
            nan_cells=nan_cells,
            score_std=score_std,
            score_min=float(factors["tenbagger_score"].min()),
            score_max=float(factors["tenbagger_score"].max()),
        )

    def compute_value_factors(self, df: pd.DataFrame) -> pd.DataFrame:
        result = df.copy()
        result["value_score"] = self._blend_scores(
            [
                self._cross_sectional_rank(result, "pe", higher_is_better=False),
                self._cross_sectional_rank(result, "pb", higher_is_better=False),
            ]
        )
        return result

    def compute_growth_factors(self, df: pd.DataFrame) -> pd.DataFrame:
        result = df.copy()
        result["growth_score"] = self._blend_scores(
            [
                self._cross_sectional_rank(result, "revenue_growth_yoy", higher_is_better=True),
                self._cross_sectional_rank(result, "net_profit_growth_yoy", higher_is_better=True),
            ]
        )
        return result

    def compute_quality_factors(self, df: pd.DataFrame) -> pd.DataFrame:
        result = df.copy()
        result["quality_score"] = self._blend_scores(
            [
                self._cross_sectional_rank(result, "roe", higher_is_better=True),
                self._cross_sectional_rank(result, "roe_trend_yoy", higher_is_better=True),
                self._cross_sectional_rank(result, "profit_margin", higher_is_better=True),
            ]
        )
        return result

    def compute_risk_factors(self, df: pd.DataFrame) -> pd.DataFrame:
        result = df.copy()
        result["risk_score"] = self._cross_sectional_rank(
            result,
            "volatility_60d",
            higher_is_better=False,
        )
        return result

    def _add_time_series_features(self, data: pd.DataFrame) -> pd.DataFrame:
        result = data.copy()
        result["daily_return"] = result.groupby("ts_code")["close"].pct_change()
        result["momentum_120d"] = result.groupby("ts_code")["close"].pct_change(120)
        result["momentum_1m"] = result.groupby("ts_code")["close"].pct_change(21)
        result["momentum_3m"] = result.groupby("ts_code")["close"].pct_change(63)
        result["momentum_6m"] = result.groupby("ts_code")["close"].pct_change(126)
        result["volatility_60d"] = (
            result.groupby("ts_code")["daily_return"]
            .rolling(60, min_periods=20)
            .std()
            .reset_index(level=0, drop=True)
        )
        rolling_peak = (
            result.groupby("ts_code")["close"]
            .rolling(120, min_periods=20)
            .max()
            .reset_index(level=0, drop=True)
        )
        drawdown = result["close"] / rolling_peak - 1
        result["max_drawdown_120d"] = (
            drawdown.groupby(result["ts_code"])
            .rolling(120, min_periods=20)
            .min()
            .reset_index(level=0, drop=True)
        )
        result["profit_margin"] = result["net_profit"] / result["revenue"].replace({0: pd.NA})

        result = self._attach_fundamental_growth(result)
        return result

    def _attach_fundamental_growth(self, data: pd.DataFrame) -> pd.DataFrame:
        if "report_period" not in data.columns:
            data["revenue_growth_yoy"] = 0.0
            data["net_profit_growth_yoy"] = 0.0
            data["roe_trend_yoy"] = 0.0
            return data

        fundamentals = (
            data.dropna(subset=["report_period"])
            .sort_values(["ts_code", "report_period", "date"])
            .drop_duplicates(["ts_code", "report_period"], keep="last")
            .loc[:, ["ts_code", "report_period", "revenue", "net_profit", "roe"]]
        )

        if fundamentals.empty:
            data["revenue_growth_yoy"] = 0.0
            data["net_profit_growth_yoy"] = 0.0
            data["roe_trend_yoy"] = 0.0
            return data

        grouped = fundamentals.groupby("ts_code", group_keys=False)
        fundamentals["revenue_growth_yoy"] = grouped["revenue"].pct_change(4)
        fundamentals["net_profit_growth_yoy"] = grouped["net_profit"].pct_change(4)
        fundamentals["roe_trend_yoy"] = grouped["roe"].diff(4)
        enriched = data.merge(
            fundamentals[
                [
                    "ts_code",
                    "report_period",
                    "revenue_growth_yoy",
                    "net_profit_growth_yoy",
                    "roe_trend_yoy",
                ]
            ],
            on=["ts_code", "report_period"],
            how="left",
        )
        for column in ["revenue_growth_yoy", "net_profit_growth_yoy", "roe_trend_yoy"]:
            enriched[column] = pd.to_numeric(enriched[column], errors="coerce").fillna(0.0)
        return enriched

    def _add_cross_sectional_scores(self, data: pd.DataFrame) -> pd.DataFrame:
        result = data.copy()
        result = self.compute_value_factors(result)
        result = self.compute_growth_factors(result)
        result = self.compute_quality_factors(result)
        result = self.compute_risk_factors(result)
        result["momentum_v2_raw"] = (
            0.2 * result["momentum_1m"].fillna(0.0)
            + 0.3 * result["momentum_3m"].fillna(0.0)
            + 0.5 * result["momentum_6m"].fillna(0.0)
        )
        result["momentum_score"] = self._cross_sectional_rank(
            result,
            "momentum_v2_raw",
            higher_is_better=True,
        )
        result = self._add_industry_scores(result)

        for column in [
            "value_score",
            "growth_score",
            "quality_score",
            "risk_score",
            "momentum_score",
            "industry_score",
        ]:
            result[column] = result[column].fillna(self.neutral_score).clip(0, 100)
        return result

    def _add_industry_scores(self, data: pd.DataFrame) -> pd.DataFrame:
        result = data.copy()
        if "industry" not in result.columns:
            result["industry_score"] = self.neutral_score
            return result

        result["industry"] = result["industry"].fillna("unknown").astype(str)
        grouped = (
            result.groupby(["date", "industry"], as_index=False)
            .agg(
                industry_growth_raw=("revenue_growth_yoy", "mean"),
                industry_pe_raw=("pe", "mean"),
                industry_flow_raw=("momentum_6m", "mean"),
            )
        )
        grouped["industry_growth_score"] = self._cross_sectional_rank(
            grouped,
            "industry_growth_raw",
            higher_is_better=True,
        )
        grouped["industry_valuation_score"] = self._cross_sectional_rank(
            grouped,
            "industry_pe_raw",
            higher_is_better=False,
        )
        grouped["industry_flow_score"] = self._cross_sectional_rank(
            grouped,
            "industry_flow_raw",
            higher_is_better=True,
        )
        grouped["industry_score"] = self._blend_scores(
            [
                grouped["industry_growth_score"],
                grouped["industry_valuation_score"],
                grouped["industry_flow_score"],
            ]
        )
        result = result.merge(
            grouped[
                [
                    "date",
                    "industry",
                    "industry_growth_score",
                    "industry_valuation_score",
                    "industry_flow_score",
                    "industry_score",
                ]
            ],
            on=["date", "industry"],
            how="left",
        )
        return result

    def _cross_sectional_rank(
        self,
        df: pd.DataFrame,
        column: str,
        higher_is_better: bool,
    ) -> pd.Series:
        values = pd.to_numeric(df[column], errors="coerce")
        ranked = values.groupby(df["date"]).rank(pct=True, ascending=higher_is_better)
        return (ranked * 100).fillna(self.neutral_score)

    def _blend_scores(self, scores: list[pd.Series]) -> pd.Series:
        if not scores:
            raise ValueError("At least one score series is required.")
        frame = pd.concat(scores, axis=1)
        return frame.mean(axis=1).fillna(self.neutral_score).clip(0, 100)
