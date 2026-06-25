"""FastAPI web display for local TASK 1 results."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

from tenbagger.config import DEFAULT_REPORT_DIR


def create_app(report_dir: Path | str = DEFAULT_REPORT_DIR) -> FastAPI:
    app = FastAPI(title="TenBagger")
    report_path = Path(report_dir) / "task1_summary.json"
    factor_report_path = Path(report_dir) / "task2_factor_summary.json"
    screener_report_path = Path(report_dir) / "task3_screener_summary.json"
    backtest_report_path = Path(report_dir) / "task4_backtest_summary.json"
    optimization_report_path = Path(report_dir) / "task5_optimization_summary.json"
    monetization_report_path = Path(report_dir) / "task6_monetization_summary.json"
    structural_report_path = Path(report_dir) / "task7_structural_validation_summary.json"
    regime_report_path = Path(report_dir) / "task8_regime_summary.json"
    behavior_report_path = Path(report_dir) / "task9_behavior_summary.json"
    structure_report_path = Path(report_dir) / "task10_structure_summary.json"
    anomaly_report_path = Path(report_dir) / "task11_anomaly_summary.json"

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/api/task1")
    def task1_api() -> JSONResponse:
        report = _load_report(report_path)
        status = 200 if report else 404
        return JSONResponse(report or {"error": "TASK 1 report not found"}, status_code=status)

    @app.get("/api/task2")
    def task2_api() -> JSONResponse:
        report = _load_report(factor_report_path)
        status = 200 if report else 404
        return JSONResponse(report or {"error": "TASK 2 report not found"}, status_code=status)

    @app.get("/api/task3")
    def task3_api() -> JSONResponse:
        report = _load_report(screener_report_path)
        status = 200 if report else 404
        return JSONResponse(report or {"error": "TASK 3 report not found"}, status_code=status)

    @app.get("/api/task4")
    def task4_api() -> JSONResponse:
        report = _load_report(backtest_report_path)
        status = 200 if report else 404
        return JSONResponse(report or {"error": "TASK 4 report not found"}, status_code=status)

    @app.get("/api/task5")
    def task5_api() -> JSONResponse:
        report = _load_report(optimization_report_path)
        status = 200 if report else 404
        return JSONResponse(report or {"error": "TASK 5 report not found"}, status_code=status)

    @app.get("/api/task6")
    def task6_api() -> JSONResponse:
        report = _load_report(monetization_report_path)
        status = 200 if report else 404
        return JSONResponse(report or {"error": "TASK 6 report not found"}, status_code=status)

    @app.get("/api/task7")
    def task7_api() -> JSONResponse:
        report = _load_report(structural_report_path)
        status = 200 if report else 404
        return JSONResponse(report or {"error": "TASK 7 report not found"}, status_code=status)

    @app.get("/api/task8")
    def task8_api() -> JSONResponse:
        report = _load_report(regime_report_path)
        status = 200 if report else 404
        return JSONResponse(report or {"error": "TASK 8 report not found"}, status_code=status)

    @app.get("/api/task8/regime")
    def task8_regime_api() -> JSONResponse:
        report = _load_report(regime_report_path)
        status = 200 if report else 404
        return JSONResponse(report.get("api_response", {}) if report else {"error": "TASK 8 report not found"}, status_code=status)

    @app.get("/api/task9")
    def task9_api() -> JSONResponse:
        report = _load_report(behavior_report_path)
        status = 200 if report else 404
        return JSONResponse(report or {"error": "TASK 9 report not found"}, status_code=status)

    @app.get("/api/task9/behavior")
    def task9_behavior_api() -> JSONResponse:
        report = _load_report(behavior_report_path)
        status = 200 if report else 404
        return JSONResponse(report.get("api_response", {}) if report else {"error": "TASK 9 report not found"}, status_code=status)

    @app.get("/api/task10")
    def task10_api() -> JSONResponse:
        report = _load_report(structure_report_path)
        status = 200 if report else 404
        return JSONResponse(report or {"error": "TASK 10 report not found"}, status_code=status)

    @app.get("/api/task10/structure")
    def task10_structure_api() -> JSONResponse:
        report = _load_report(structure_report_path)
        status = 200 if report else 404
        return JSONResponse(report.get("api_response", {}) if report else {"error": "TASK 10 report not found"}, status_code=status)

    @app.get("/api/task11")
    def task11_api() -> JSONResponse:
        report = _load_report(anomaly_report_path)
        status = 200 if report else 404
        return JSONResponse(report or {"error": "TASK 11 report not found"}, status_code=status)

    @app.get("/api/task11/anomaly")
    def task11_anomaly_api() -> JSONResponse:
        report = _load_report(anomaly_report_path)
        status = 200 if report else 404
        return JSONResponse(report.get("api_response", {}) if report else {"error": "TASK 11 report not found"}, status_code=status)

    @app.get("/", response_class=HTMLResponse)
    def index() -> str:
        report = _load_report(report_path)
        factor_report = _load_report(factor_report_path)
        screener_report = _load_report(screener_report_path)
        backtest_report = _load_report(backtest_report_path)
        optimization_report = _load_report(optimization_report_path)
        monetization_report = _load_report(monetization_report_path)
        structural_report = _load_report(structural_report_path)
        regime_report = _load_report(regime_report_path)
        behavior_report = _load_report(behavior_report_path)
        structure_report = _load_report(structure_report_path)
        anomaly_report = _load_report(anomaly_report_path)
        return _render_dashboard(
            report,
            factor_report,
            screener_report,
            backtest_report,
            optimization_report,
            monetization_report,
            structural_report,
            regime_report,
            behavior_report,
            structure_report,
            anomaly_report,
        )

    return app


app = create_app()


def _load_report(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _render_dashboard(
    report: dict[str, Any] | None,
    factor_report: dict[str, Any] | None,
    screener_report: dict[str, Any] | None,
    backtest_report: dict[str, Any] | None,
    optimization_report: dict[str, Any] | None,
    monetization_report: dict[str, Any] | None,
    structural_report: dict[str, Any] | None,
    regime_report: dict[str, Any] | None,
    behavior_report: dict[str, Any] | None,
    structure_report: dict[str, Any] | None,
    anomaly_report: dict[str, Any] | None,
) -> str:
    if report is None:
        content = """
        <main class="shell">
          <section class="empty">
            <h1>TenBagger</h1>
            <p>TASK 1 report not found. Run the data loader first.</p>
          </section>
        </main>
        """
        return _page(content)

    missing = report.get("missing_rates", {})
    coverage = report.get("stock_coverage", [])
    snapshot = report.get("latest_snapshot", [])

    metric_cards = [
        ("Stocks", report.get("stock_count")),
        ("Rows", report.get("row_count")),
        ("Latest Date", report.get("latest_trading_date")),
        ("Date Range", f"{report.get('date_range', {}).get('start')} to {report.get('date_range', {}).get('end')}"),
    ]

    cards_html = "\n".join(
        f"<div class='metric'><span>{html.escape(str(label))}</span><strong>{html.escape(str(value))}</strong></div>"
        for label, value in metric_cards
    )
    missing_html = "\n".join(
        f"<tr><td>{html.escape(str(key))}</td><td>{float(value):.2%}</td></tr>"
        for key, value in missing.items()
    )
    coverage_html = "\n".join(
        "<tr><td>{ts_code}</td><td>{rows}</td><td>{start_date}</td><td>{end_date}</td><td>{coverage_ratio:.2%}</td></tr>".format(
            **item
        )
        for item in coverage
    )
    snapshot_html = "\n".join(
        "<tr><td>{ts_code}</td><td>{close}</td><td>{revenue}</td><td>{net_profit}</td><td>{roe}</td><td>{pe}</td><td>{pb}</td><td>{market_cap}</td></tr>".format(
            **{key: html.escape(str(row.get(key, ""))) for key in ["ts_code", "close", "revenue", "net_profit", "roe", "pe", "pb", "market_cap"]}
        )
        for row in snapshot
    )

    factor_section = _render_factor_section(factor_report)
    screener_section = _render_screener_section(screener_report)
    backtest_section = _render_backtest_section(backtest_report)
    optimization_section = _render_optimization_section(optimization_report)
    monetization_section = _render_monetization_section(monetization_report)
    structural_section = _render_structural_section(structural_report)
    regime_section = _render_regime_section(regime_report)
    behavior_section = _render_behavior_section(behavior_report)
    structure_section = _render_structure_section(structure_report)
    anomaly_section = _render_anomaly_section(anomaly_report)

    content = f"""
    <main class="shell">
      <header class="topbar">
        <div>
          <h1>TenBagger</h1>
          <p>TASK 1 data layer dashboard</p>
        </div>
        <div class="stamp">Generated {html.escape(str(report.get("generated_at")))}</div>
      </header>
      <section class="metrics">{cards_html}</section>
      <section class="grid">
        <div>
          <h2>Missing Rates</h2>
          <table><thead><tr><th>Column</th><th>Missing</th></tr></thead><tbody>{missing_html}</tbody></table>
        </div>
        <div>
          <h2>Stock Coverage</h2>
          <table><thead><tr><th>Code</th><th>Rows</th><th>Start</th><th>End</th><th>Coverage</th></tr></thead><tbody>{coverage_html}</tbody></table>
        </div>
      </section>
      <section>
        <h2>Latest Snapshot</h2>
        <table><thead><tr><th>Code</th><th>Close</th><th>Revenue</th><th>Net Profit</th><th>ROE</th><th>PE</th><th>PB</th><th>Market Cap</th></tr></thead><tbody>{snapshot_html}</tbody></table>
      </section>
      {factor_section}
      {screener_section}
      {backtest_section}
      {optimization_section}
      {monetization_section}
      {structural_section}
      {regime_section}
      {behavior_section}
      {structure_section}
      {anomaly_section}
    </main>
    """
    return _page(content)


def _render_factor_section(report: dict[str, Any] | None) -> str:
    if report is None:
        return """
        <section>
          <h2>Factor Engine</h2>
          <table><tbody><tr><td>TASK 2 report not found</td></tr></tbody></table>
        </section>
        """

    validation = report.get("validation", {})
    top_scores = report.get("latest_top_scores", [])
    validation_html = "\n".join(
        f"<tr><td>{html.escape(str(key))}</td><td>{html.escape(str(value))}</td></tr>"
        for key, value in validation.items()
    )
    scores_html = "\n".join(
        "<tr><td>{ts_code}</td><td>{tenbagger_score}</td><td>{growth_score}</td><td>{quality_score}</td><td>{value_score}</td><td>{risk_score}</td><td>{momentum_score}</td></tr>".format(
            **{key: html.escape(str(row.get(key, ""))) for key in ["ts_code", "tenbagger_score", "growth_score", "quality_score", "value_score", "risk_score", "momentum_score"]}
        )
        for row in top_scores
    )
    return f"""
    <section>
      <h2>Factor Engine</h2>
    </section>
    <section class="grid">
      <div>
        <h2>Factor Validation</h2>
        <table><thead><tr><th>Check</th><th>Value</th></tr></thead><tbody>{validation_html}</tbody></table>
      </div>
      <div>
        <h2>Latest Factor Scores</h2>
        <table><thead><tr><th>Code</th><th>TenBagger</th><th>Growth</th><th>Quality</th><th>Value</th><th>Risk</th><th>Momentum</th></tr></thead><tbody>{scores_html}</tbody></table>
      </div>
    </section>
    """


def _render_screener_section(report: dict[str, Any] | None) -> str:
    if report is None:
        return """
        <section>
          <h2>Screener</h2>
          <table><tbody><tr><td>TASK 3 report not found</td></tr></tbody></table>
        </section>
        """

    preview = report.get("backtest_preview", {})
    decay = report.get("ic_decay_curve", [])
    candidates = report.get("top_candidates", [])
    near_misses = report.get("near_misses", [])

    preview_html = "\n".join(
        f"<tr><td>{html.escape(str(key))}</td><td>{html.escape(str(value))}</td></tr>"
        for key, value in preview.items()
    )
    decay_html = "\n".join(
        "<tr><td>{horizon_days}</td><td>{ic_mean}</td><td>{rank_ic_mean}</td><td>{observations}</td></tr>".format(
            **{key: html.escape(str(row.get(key, ""))) for key in ["horizon_days", "ic_mean", "rank_ic_mean", "observations"]}
        )
        for row in decay
    )
    candidate_rows = candidates or near_misses
    candidate_title = "Top Candidates" if candidates else "Near Misses"
    candidate_html = "\n".join(
        "<tr><td>{ts_code}</td><td>{tenbagger_score}</td><td>{industry}</td><td>{revenue_growth_yoy}</td><td>{roe}</td><td>{debt_ratio}</td><td>{fail_reasons}</td></tr>".format(
            **{key: html.escape(str(row.get(key, ""))) for key in ["ts_code", "tenbagger_score", "industry", "revenue_growth_yoy", "roe", "debt_ratio", "fail_reasons"]}
        )
        for row in candidate_rows
    )
    return f"""
    <section>
      <h2>Screener</h2>
      <p>Candidate count: {html.escape(str(report.get("candidate_count")))}</p>
    </section>
    <section class="grid">
      <div>
        <h2>Backtest Preview</h2>
        <table><thead><tr><th>Metric</th><th>Value</th></tr></thead><tbody>{preview_html}</tbody></table>
      </div>
      <div>
        <h2>IC Decay</h2>
        <table><thead><tr><th>Days</th><th>IC</th><th>RankIC</th><th>Obs</th></tr></thead><tbody>{decay_html}</tbody></table>
      </div>
    </section>
    <section>
      <h2>{candidate_title}</h2>
      <table><thead><tr><th>Code</th><th>Score</th><th>Industry</th><th>Growth</th><th>ROE</th><th>Debt</th><th>Fail Reasons</th></tr></thead><tbody>{candidate_html}</tbody></table>
    </section>
    """


def _render_backtest_section(report: dict[str, Any] | None) -> str:
    if report is None:
        return """
        <section>
          <h2>Portfolio Backtest</h2>
          <table><tbody><tr><td>TASK 4 report not found</td></tr></tbody></table>
        </section>
        """

    metrics = report.get("metrics", {})
    benchmarks = metrics.get("benchmarks", {})
    attribution = report.get("factor_attribution", {})
    holdings = report.get("latest_holdings", [])

    metric_keys = [
        "annual_return",
        "sharpe",
        "max_drawdown",
        "volatility",
        "win_rate",
        "turnover_rate",
        "total_transaction_cost",
    ]
    metrics_html = "\n".join(
        f"<tr><td>{html.escape(str(key))}</td><td>{html.escape(str(metrics.get(key, '')))}</td></tr>"
        for key in metric_keys
    )
    benchmark_html = "\n".join(
        "<tr><td>{name}</td><td>{annual_return}</td><td>{excess_return}</td><td>{beta}</td><td>{max_drawdown}</td></tr>".format(
            name=html.escape(str(name)),
            **{key: html.escape(str(value.get(key, ""))) for key in ["annual_return", "excess_return", "beta", "max_drawdown"]},
        )
        for name, value in benchmarks.items()
    )
    holding_html = "\n".join(
        "<tr><td>{ts_code}</td><td>{weight}</td><td>{rebalance_date}</td></tr>".format(
            **{key: html.escape(str(row.get(key, ""))) for key in ["ts_code", "weight", "rebalance_date"]}
        )
        for row in holdings
    )
    return f"""
    <section>
      <h2>Portfolio Backtest</h2>
      <p>Final NAV: {html.escape(str(report.get("final_nav")))} | Dominant factor: {html.escape(str(attribution.get("dominant_factor")))}</p>
    </section>
    <section class="grid">
      <div>
        <h2>Risk Metrics</h2>
        <table><thead><tr><th>Metric</th><th>Value</th></tr></thead><tbody>{metrics_html}</tbody></table>
      </div>
      <div>
        <h2>Benchmarks</h2>
        <table><thead><tr><th>Name</th><th>Annual</th><th>Excess</th><th>Beta</th><th>Drawdown</th></tr></thead><tbody>{benchmark_html}</tbody></table>
      </div>
    </section>
    <section>
      <h2>Latest Holdings</h2>
      <table><thead><tr><th>Code</th><th>Weight</th><th>Rebalance Date</th></tr></thead><tbody>{holding_html}</tbody></table>
    </section>
    """


def _render_optimization_section(report: dict[str, Any] | None) -> str:
    if report is None:
        return """
        <section>
          <h2>Factor Optimization</h2>
          <table><tbody><tr><td>TASK 5 report not found</td></tr></tbody></table>
        </section>
        """

    baseline = report.get("baseline_test_metrics", {})
    optimized = report.get("test_metrics", {})
    weights = report.get("best_weights", {})
    ic = report.get("ic_comparison", {})
    weight_html = "\n".join(
        f"<tr><td>{html.escape(str(key))}</td><td>{html.escape(str(value))}</td></tr>"
        for key, value in weights.items()
    )
    metrics_html = "\n".join(
        "<tr><td>{metric}</td><td>{base}</td><td>{opt}</td></tr>".format(
            metric=html.escape(metric),
            base=html.escape(str(baseline.get(metric, ""))),
            opt=html.escape(str(optimized.get(metric, ""))),
        )
        for metric in ["annual_return", "sharpe", "max_drawdown", "volatility", "win_rate"]
    )
    ic_html = "\n".join(
        "<tr><td>{key}</td><td>{baseline_rank_ic}</td><td>{optimized_rank_ic}</td><td>{delta}</td></tr>".format(
            key=html.escape(str(key)),
            **{field: html.escape(str(value.get(field, ""))) for field in ["baseline_rank_ic", "optimized_rank_ic", "delta"]},
        )
        for key, value in ic.items()
    )
    return f"""
    <section>
      <h2>Factor Optimization</h2>
      <p>Candidates evaluated: {html.escape(str(report.get("candidates_evaluated")))}</p>
    </section>
    <section class="grid">
      <div>
        <h2>Best Weights</h2>
        <table><thead><tr><th>Factor</th><th>Weight</th></tr></thead><tbody>{weight_html}</tbody></table>
      </div>
      <div>
        <h2>Baseline vs Optimized</h2>
        <table><thead><tr><th>Metric</th><th>Baseline</th><th>Optimized</th></tr></thead><tbody>{metrics_html}</tbody></table>
      </div>
    </section>
    <section>
      <h2>IC Improvement</h2>
      <table><thead><tr><th>Horizon</th><th>Baseline RankIC</th><th>Optimized RankIC</th><th>Delta</th></tr></thead><tbody>{ic_html}</tbody></table>
    </section>
    """


def _render_monetization_section(report: dict[str, Any] | None) -> str:
    if report is None:
        return """
        <section>
          <h2>Alpha Monetization</h2>
          <table><tbody><tr><td>TASK 6 report not found</td></tr></tbody></table>
        </section>
        """

    best = report.get("best_config", {})
    test = report.get("test_metrics", {})
    divergence = report.get("ic_pnl_divergence", {})
    costs = report.get("cost_sensitivity", [])
    best_html = "\n".join(
        f"<tr><td>{html.escape(str(key))}</td><td>{html.escape(str(value))}</td></tr>"
        for key, value in best.items()
    )
    test_html = "\n".join(
        f"<tr><td>{html.escape(str(key))}</td><td>{html.escape(str(test.get(key, '')))}</td></tr>"
        for key in ["annual_return", "sharpe", "max_drawdown", "turnover_rate"]
    )
    cost_html = "\n".join(
        "<tr><td>{transaction_cost_rate}</td><td>{sharpe}</td><td>{annual_return}</td><td>{turnover_rate}</td></tr>".format(
            **{key: html.escape(str(row.get(key, ""))) for key in ["transaction_cost_rate", "sharpe", "annual_return", "turnover_rate"]}
        )
        for row in costs
    )
    return f"""
    <section>
      <h2>Alpha Monetization</h2>
      <p>{html.escape(str(divergence.get("interpretation")))}</p>
    </section>
    <section class="grid">
      <div>
        <h2>Best Config</h2>
        <table><thead><tr><th>Setting</th><th>Value</th></tr></thead><tbody>{best_html}</tbody></table>
      </div>
      <div>
        <h2>Test Metrics</h2>
        <table><thead><tr><th>Metric</th><th>Value</th></tr></thead><tbody>{test_html}</tbody></table>
      </div>
    </section>
    <section>
      <h2>Cost Sensitivity</h2>
      <table><thead><tr><th>Cost</th><th>Sharpe</th><th>Annual</th><th>Turnover</th></tr></thead><tbody>{cost_html}</tbody></table>
    </section>
    """


def _render_structural_section(report: dict[str, Any] | None) -> str:
    if report is None:
        return """
        <section>
          <h2>Structural Validation</h2>
          <table><tbody><tr><td>TASK 7 report not found</td></tr></tbody></table>
        </section>
        """

    criteria = report.get("criteria", {})
    stability = report.get("stability_report", {})
    randomization = report.get("randomization_test", {})
    failure = report.get("failure_mode_diagnosis", {})
    metrics = report.get("oos_metrics", {})
    criteria_html = "\n".join(
        f"<tr><td>{html.escape(str(key))}</td><td>{html.escape(str(value))}</td></tr>"
        for key, value in criteria.items()
    )
    stability_html = "\n".join(
        f"<tr><td>{html.escape(str(key))}</td><td>{html.escape(str(stability.get(key, '')))}</td></tr>"
        for key in ["score", "ic_variance", "sharpe_variance", "positive_sharpe_ratio", "decay_slow"]
    )
    random_html = "\n".join(
        "<tr><td>{name}</td><td>{mean}</td><td>{p95}</td><td>{p_value}</td><td>{significant}</td></tr>".format(
            name=html.escape(str(name)),
            **{key: html.escape(str(value.get(key, ""))) for key in ["mean", "p95", "p_value", "significant"]},
        )
        for name, value in {
            "label_shuffle": randomization.get("label_shuffle", {}),
            "feature_permutation": randomization.get("feature_permutation", {}),
        }.items()
    )
    metric_html = "\n".join(
        f"<tr><td>{html.escape(str(key))}</td><td>{html.escape(str(metrics.get(key, '')))}</td></tr>"
        for key in ["annual_return", "sharpe", "max_drawdown", "turnover_rate"]
    )
    return f"""
    <section>
      <h2>Structural Validation</h2>
      <p>Classification: {html.escape(str(report.get("classification")))} | Primary failure: {html.escape(str(failure.get("primary_failure")))}</p>
    </section>
    <section class="grid">
      <div>
        <h2>OOS Metrics</h2>
        <table><thead><tr><th>Metric</th><th>Value</th></tr></thead><tbody>{metric_html}</tbody></table>
      </div>
      <div>
        <h2>Stability</h2>
        <table><thead><tr><th>Metric</th><th>Value</th></tr></thead><tbody>{stability_html}</tbody></table>
      </div>
    </section>
    <section class="grid">
      <div>
        <h2>Real Alpha Criteria</h2>
        <table><thead><tr><th>Criterion</th><th>Value</th></tr></thead><tbody>{criteria_html}</tbody></table>
      </div>
      <div>
        <h2>Randomization</h2>
        <table><thead><tr><th>Test</th><th>Mean</th><th>P95</th><th>P Value</th><th>Significant</th></tr></thead><tbody>{random_html}</tbody></table>
      </div>
    </section>
    """


def _render_regime_section(report: dict[str, Any] | None) -> str:
    if report is None:
        return """
        <section>
          <h2>Market Regime Dashboard</h2>
          <table><tbody><tr><td>TASK 8 report not found</td></tr></tbody></table>
        </section>
        """

    latest = report.get("latest", {})
    api = report.get("api_response", {})
    validation = report.get("validation", {})
    history = report.get("history", {})
    chart_tail = history.get("chart_tail", [])
    recent_changes = history.get("recent_30_changes", [])

    metric_cards = [
        ("Behavior", api.get("behavior_state")),
        ("Trend", api.get("trend_regime")),
        ("Volatility", api.get("volatility_regime")),
        ("Liquidity", api.get("liquidity_regime")),
    ]
    cards_html = "\n".join(
        f"<div class='metric'><span>{html.escape(str(label))}</span><strong>{html.escape(str(value))}</strong></div>"
        for label, value in metric_cards
    )
    detail_html = "\n".join(
        f"<tr><td>{html.escape(str(key))}</td><td>{html.escape(_fmt(latest.get(key)))}</td></tr>"
        for key in [
            "date",
            "trend_strength",
            "volatility_percentile",
            "liquidity_score",
            "regime_change_probability",
            "stability_score",
        ]
    )
    validation_html = "\n".join(
        f"<tr><td>{html.escape(str(key))}</td><td>{html.escape(_fmt(validation.get(key)))}</td></tr>"
        for key in [
            "regime_autocorrelation",
            "transition_frequency",
            "recent_30d_transition_frequency",
            "mean_duration_days",
            "transition_not_overfit",
            "regime_has_continuity",
        ]
    )
    change_html = "\n".join(
        "<tr><td>{date}</td><td>{trend_regime}</td><td>{volatility_regime}</td><td>{liquidity_regime}</td><td>{behavior_state}</td></tr>".format(
            **{key: html.escape(str(row.get(key, ""))) for key in ["date", "trend_regime", "volatility_regime", "liquidity_regime", "behavior_state"]}
        )
        for row in recent_changes[-10:]
    )
    if not change_html:
        change_html = "<tr><td colspan='5'>No regime changes in the latest 30 observations</td></tr>"

    regime_strip = _regime_strip(chart_tail)
    trend_chart = _sparkline_svg(chart_tail, "trend_strength", "#0f766e")
    volatility_chart = _sparkline_svg(chart_tail, "realized_vol_20d", "#9f1239")
    liquidity_chart = _sparkline_svg(chart_tail, "liquidity_score", "#1d4ed8")

    return f"""
    <section>
      <h2>Market Regime Dashboard</h2>
      <p>Behavioral state engine for route 2. Data source: {html.escape(str(report.get("data_source", {}).get("source")))}</p>
    </section>
    <section class="metrics">{cards_html}</section>
    <section>
      <h2>Regime History</h2>
      {regime_strip}
    </section>
    <section class="grid">
      <div>
        <h2>Current Regime Detail</h2>
        <table><thead><tr><th>Metric</th><th>Value</th></tr></thead><tbody>{detail_html}</tbody></table>
      </div>
      <div>
        <h2>Regime Validation</h2>
        <table><thead><tr><th>Check</th><th>Value</th></tr></thead><tbody>{validation_html}</tbody></table>
      </div>
    </section>
    <section class="grid">
      <div>
        <h2>Trend Strength</h2>
        {trend_chart}
      </div>
      <div>
        <h2>Volatility Curve</h2>
        {volatility_chart}
      </div>
    </section>
    <section>
      <h2>Liquidity Curve</h2>
      {liquidity_chart}
    </section>
    <section>
      <h2>Recent Regime Changes</h2>
      <table><thead><tr><th>Date</th><th>Trend</th><th>Volatility</th><th>Liquidity</th><th>Behavior</th></tr></thead><tbody>{change_html}</tbody></table>
    </section>
    """


def _render_behavior_section(report: dict[str, Any] | None) -> str:
    if report is None:
        return """
        <section>
          <h2>Behavioral Flow Dashboard</h2>
          <table><tbody><tr><td>TASK 9 report not found</td></tr></tbody></table>
        </section>
        """

    latest = report.get("latest", {})
    api = report.get("api_response", {})
    validation = report.get("validation", {})
    history = report.get("history", {})
    chart_tail = history.get("chart_tail", [])
    divergence_events = history.get("divergence_events", [])

    metric_cards = [
        ("Actor", latest.get("dominant_actor")),
        ("Crowding", api.get("crowding_level")),
        ("Divergence", api.get("flow_price_divergence")),
        ("Overlay", api.get("behavior_overlay_state")),
    ]
    cards_html = "\n".join(
        f"<div class='metric'><span>{html.escape(str(label))}</span><strong>{html.escape(str(value))}</strong></div>"
        for label, value in metric_cards
    )
    detail_html = "\n".join(
        f"<tr><td>{html.escape(str(key))}</td><td>{html.escape(_fmt(latest.get(key)))}</td></tr>"
        for key in [
            "date",
            "retail_pressure_index",
            "institutional_flow_index",
            "panic_index",
            "fomo_index",
            "positioning_crowdedness",
            "reversal_risk",
            "joint_regime_behavior",
        ]
    )
    validation_html = "\n".join(
        f"<tr><td>{html.escape(str(key))}</td><td>{html.escape(_fmt(validation.get(key)))}</td></tr>"
        for key in [
            "uses_future_return_labels",
            "uses_factor_alpha",
            "all_scores_bounded_0_1",
            "overlay_autocorrelation",
            "behavior_transition_frequency",
            "divergence_event_frequency",
            "recent_30d_mean_panic",
            "recent_30d_mean_fomo",
        ]
    )
    event_html = "\n".join(
        "<tr><td>{date}</td><td>{flow_price_divergence}</td><td>{divergence_score}</td><td>{dominant_actor}</td><td>{behavior_overlay_state}</td></tr>".format(
            **{key: html.escape(str(row.get(key, ""))) for key in ["date", "flow_price_divergence", "divergence_score", "dominant_actor", "behavior_overlay_state"]}
        )
        for row in divergence_events[-10:]
    )
    if not event_html:
        event_html = "<tr><td colspan='5'>No recent flow-price divergence events</td></tr>"

    retail_chart = _sparkline_svg(chart_tail, "retail_pressure_index", "#b45309")
    institutional_chart = _sparkline_svg(chart_tail, "institutional_flow_index", "#0f766e")
    panic_chart = _sparkline_svg(chart_tail, "panic_index", "#be123c")
    fomo_chart = _sparkline_svg(chart_tail, "fomo_index", "#1d4ed8")
    crowding_heatmap = _crowding_heatmap(chart_tail)

    return f"""
    <section>
      <h2>Behavioral Flow Dashboard</h2>
      <p>Market actors and behavior pressure. Source: {html.escape(str(report.get("source", {}).get("source")))}</p>
    </section>
    <section class="metrics">{cards_html}</section>
    <section>
      <h2>Crowding Heatmap</h2>
      {crowding_heatmap}
    </section>
    <section class="grid">
      <div>
        <h2>Behavior Detail</h2>
        <table><thead><tr><th>Metric</th><th>Value</th></tr></thead><tbody>{detail_html}</tbody></table>
      </div>
      <div>
        <h2>Behavior Validation</h2>
        <table><thead><tr><th>Check</th><th>Value</th></tr></thead><tbody>{validation_html}</tbody></table>
      </div>
    </section>
    <section class="grid">
      <div>
        <h2>Retail Pressure</h2>
        {retail_chart}
      </div>
      <div>
        <h2>Institutional Flow</h2>
        {institutional_chart}
      </div>
    </section>
    <section class="grid">
      <div>
        <h2>Panic Timeline</h2>
        {panic_chart}
      </div>
      <div>
        <h2>FOMO Timeline</h2>
        {fomo_chart}
      </div>
    </section>
    <section>
      <h2>Flow-Price Divergence</h2>
      <table><thead><tr><th>Date</th><th>Divergence</th><th>Score</th><th>Actor</th><th>Overlay</th></tr></thead><tbody>{event_html}</tbody></table>
    </section>
    """


def _render_structure_section(report: dict[str, Any] | None) -> str:
    if report is None:
        return """
        <section>
          <h2>Market Structure Dashboard</h2>
          <table><tbody><tr><td>TASK 10 report not found</td></tr></tbody></table>
        </section>
        """

    latest = report.get("latest", {})
    api = report.get("api_response", {})
    validation = report.get("validation", {})
    history = report.get("history", {})
    chart_tail = history.get("chart_tail", [])
    shocks = history.get("structural_shocks", [])

    metric_cards = [
        ("Structure", api.get("structure_state")),
        ("Correlation", api.get("correlation_regime")),
        ("Dispersion", _fmt(api.get("market_dispersion"))),
        ("Shock", _fmt(api.get("structural_shock_probability"))),
    ]
    cards_html = "\n".join(
        f"<div class='metric'><span>{html.escape(str(label))}</span><strong>{html.escape(str(value))}</strong></div>"
        for label, value in metric_cards
    )
    detail_html = "\n".join(
        f"<tr><td>{html.escape(str(key))}</td><td>{html.escape(_fmt(latest.get(key)))}</td></tr>"
        for key in [
            "date",
            "trend_component",
            "flow_component",
            "volatility_component",
            "noise_component",
            "cross_sectional_correlation",
            "structural_shock_type",
            "regime_behavior_structure",
        ]
    )
    validation_html = "\n".join(
        f"<tr><td>{html.escape(str(key))}</td><td>{html.escape(_fmt(validation.get(key)))}</td></tr>"
        for key in [
            "uses_future_return_labels",
            "uses_alpha_factors",
            "purely_observational",
            "components_sum_to_one",
            "all_scores_bounded_0_1",
            "structure_autocorrelation",
            "structure_transition_frequency",
            "shock_event_frequency",
        ]
    )
    shock_html = "\n".join(
        "<tr><td>{date}</td><td>{structural_shock_type}</td><td>{structural_shock_probability}</td><td>{structure_state}</td></tr>".format(
            **{key: html.escape(str(row.get(key, ""))) for key in ["date", "structural_shock_type", "structural_shock_probability", "structure_state"]}
        )
        for row in shocks[-10:]
    )
    if not shock_html:
        shock_html = "<tr><td colspan='4'>No recent structural shock events</td></tr>"

    decomposition = _decomposition_bars(latest)
    dispersion_heatmap = _value_heatmap(chart_tail, "market_dispersion", "#dbeafe", "#1d4ed8")
    correlation_chart = _sparkline_svg(chart_tail, "cross_sectional_correlation", "#7c3aed")
    structure_timeline = _structure_strip(chart_tail)

    return f"""
    <section>
      <h2>Market Structure Dashboard</h2>
      <p>Structure decomposition across trend, flow, volatility, and noise. Source: {html.escape(str(report.get("source", {}).get("source")))}</p>
    </section>
    <section class="metrics">{cards_html}</section>
    <section>
      <h2>Return Decomposition</h2>
      {decomposition}
    </section>
    <section>
      <h2>Structure State Timeline</h2>
      {structure_timeline}
    </section>
    <section class="grid">
      <div>
        <h2>Structure Detail</h2>
        <table><thead><tr><th>Metric</th><th>Value</th></tr></thead><tbody>{detail_html}</tbody></table>
      </div>
      <div>
        <h2>Structure Validation</h2>
        <table><thead><tr><th>Check</th><th>Value</th></tr></thead><tbody>{validation_html}</tbody></table>
      </div>
    </section>
    <section class="grid">
      <div>
        <h2>Dispersion Heatmap</h2>
        {dispersion_heatmap}
      </div>
      <div>
        <h2>Correlation Network</h2>
        {correlation_chart}
      </div>
    </section>
    <section>
      <h2>Structural Shock Events</h2>
      <table><thead><tr><th>Date</th><th>Type</th><th>Probability</th><th>State</th></tr></thead><tbody>{shock_html}</tbody></table>
    </section>
    """


def _render_anomaly_section(report: dict[str, Any] | None) -> str:
    if report is None:
        return """
        <section>
          <h2>Structural Anomaly Dashboard</h2>
          <table><tbody><tr><td>TASK 11 report not found</td></tr></tbody></table>
        </section>
        """

    latest = report.get("latest", {})
    api = report.get("api_response", {})
    validation = report.get("validation", {})
    history = report.get("history", {})
    chart_tail = history.get("chart_tail", [])
    anomaly_events = history.get("anomaly_events", [])
    flow_events = history.get("flow_shock_events", [])

    metric_cards = [
        ("Risk", api.get("systemic_risk_level")),
        ("Anomaly", _fmt(api.get("anomaly_score"))),
        ("Dominant", api.get("dominant_anomaly_type")),
        ("State", api.get("anomaly_state")),
    ]
    cards_html = "\n".join(
        f"<div class='metric'><span>{html.escape(str(label))}</span><strong>{html.escape(str(value))}</strong></div>"
        for label, value in metric_cards
    )
    detail_html = "\n".join(
        f"<tr><td>{html.escape(str(key))}</td><td>{html.escape(_fmt(latest.get(key)))}</td></tr>"
        for key in [
            "date",
            "structural_break_prob",
            "correlation_break_prob",
            "flow_shock_prob",
            "behavioral_anomaly_score",
            "cross_sector_decoupling_prob",
            "liquidity_vacuum_prob",
        ]
    )
    validation_html = "\n".join(
        f"<tr><td>{html.escape(str(key))}</td><td>{html.escape(_fmt(validation.get(key)))}</td></tr>"
        for key in [
            "uses_future_return_labels",
            "uses_alpha_model",
            "predicts_market_direction",
            "purely_observational",
            "all_scores_bounded_0_1",
            "anomaly_event_frequency",
            "high_risk_frequency",
            "recent_30d_mean_anomaly",
        ]
    )
    event_html = "\n".join(
        "<tr><td>{date}</td><td>{anomaly_state}</td><td>{anomaly_score}</td><td>{systemic_risk_level}</td></tr>".format(
            **{key: html.escape(str(row.get(key, ""))) for key in ["date", "anomaly_state", "anomaly_score", "systemic_risk_level"]}
        )
        for row in anomaly_events[-10:]
    )
    if not event_html:
        event_html = "<tr><td colspan='4'>No medium/high anomaly events in latest 120 observations</td></tr>"
    flow_html = "\n".join(
        "<tr><td>{date}</td><td>{flow_shock_prob}</td><td>{institutional_flow_shock_prob}</td><td>{retail_panic_cluster_prob}</td></tr>".format(
            **{key: html.escape(str(row.get(key, ""))) for key in ["date", "flow_shock_prob", "institutional_flow_shock_prob", "retail_panic_cluster_prob"]}
        )
        for row in flow_events[-10:]
    )
    if not flow_html:
        flow_html = "<tr><td colspan='4'>No recent flow shock events</td></tr>"

    anomaly_chart = _sparkline_svg(chart_tail, "anomaly_score", "#be123c")
    shock_heatmap = _value_heatmap(chart_tail, "anomaly_score", "#fee2e2", "#be123c")
    correlation_chart = _sparkline_svg(chart_tail, "correlation_break_prob", "#7c3aed")
    anomaly_strip = _anomaly_strip(chart_tail)

    return f"""
    <section>
      <h2>Structural Anomaly Dashboard</h2>
      <p>Purely observational anomaly detection across regime, behavior, and structure. Source: {html.escape(str(report.get("source", {}).get("source")))}</p>
    </section>
    <section class="metrics">{cards_html}</section>
    <section>
      <h2>Anomaly Timeline</h2>
      {anomaly_chart}
    </section>
    <section>
      <h2>Shock Detection Heatmap</h2>
      {shock_heatmap}
    </section>
    <section>
      <h2>Anomaly State Timeline</h2>
      {anomaly_strip}
    </section>
    <section class="grid">
      <div>
        <h2>Anomaly Detail</h2>
        <table><thead><tr><th>Metric</th><th>Value</th></tr></thead><tbody>{detail_html}</tbody></table>
      </div>
      <div>
        <h2>Anomaly Validation</h2>
        <table><thead><tr><th>Check</th><th>Value</th></tr></thead><tbody>{validation_html}</tbody></table>
      </div>
    </section>
    <section class="grid">
      <div>
        <h2>Correlation Breakdown</h2>
        {correlation_chart}
      </div>
      <div>
        <h2>Flow Shock Events</h2>
        <table><thead><tr><th>Date</th><th>Flow</th><th>Inst</th><th>Retail</th></tr></thead><tbody>{flow_html}</tbody></table>
      </div>
    </section>
    <section>
      <h2>Anomaly Events</h2>
      <table><thead><tr><th>Date</th><th>State</th><th>Score</th><th>Risk</th></tr></thead><tbody>{event_html}</tbody></table>
    </section>
    """


def _fmt(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def _sparkline_svg(rows: list[dict[str, Any]], key: str, color: str) -> str:
    values = [float(row.get(key) or 0.0) for row in rows if row.get(key) is not None]
    if len(values) < 2:
        return "<div class='chart empty'>Not enough data</div>"
    width = 760
    height = 150
    min_value = min(values)
    max_value = max(values)
    span = max(max_value - min_value, 1e-9)
    points = []
    for idx, value in enumerate(values):
        x = idx / max(len(values) - 1, 1) * width
        y = height - ((value - min_value) / span * (height - 20) + 10)
        points.append(f"{x:.2f},{y:.2f}")
    return f"""
    <svg class="chart" viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(key)} chart">
      <rect x="0" y="0" width="{width}" height="{height}" rx="8"></rect>
      <polyline points="{' '.join(points)}" fill="none" stroke="{color}" stroke-width="3"></polyline>
    </svg>
    """


def _regime_strip(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "<div class='regime-strip empty'>Not enough data</div>"
    colors = {
        "risk_on": "#0f766e",
        "risk_off": "#475569",
        "panic": "#be123c",
        "euphoria": "#b45309",
        "transition": "#64748b",
    }
    cells = []
    for row in rows[-90:]:
        state = str(row.get("behavior_state", "transition"))
        date = html.escape(str(row.get("date", "")))
        cells.append(
            f"<span title='{date} {html.escape(state)}' style='background:{colors.get(state, '#64748b')}'></span>"
        )
    return f"<div class='regime-strip'>{''.join(cells)}</div>"


def _crowding_heatmap(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "<div class='regime-strip empty'>Not enough data</div>"
    colors = {
        "low": "#d9f99d",
        "medium": "#fde68a",
        "high": "#fb923c",
        "extreme": "#be123c",
    }
    cells = []
    for row in rows[-90:]:
        level = str(row.get("crowding_level", "low"))
        score = html.escape(_fmt(row.get("positioning_crowdedness")))
        date = html.escape(str(row.get("date", "")))
        cells.append(
            f"<span title='{date} {html.escape(level)} {score}' style='background:{colors.get(level, '#fde68a')}'></span>"
        )
    return f"<div class='regime-strip'>{''.join(cells)}</div>"


def _decomposition_bars(latest: dict[str, Any]) -> str:
    parts = [
        ("Trend", latest.get("trend_component"), "#0f766e"),
        ("Flow", latest.get("flow_component"), "#1d4ed8"),
        ("Volatility", latest.get("volatility_component"), "#be123c"),
        ("Noise", latest.get("noise_component"), "#64748b"),
    ]
    rows = []
    for label, value, color in parts:
        score = float(value or 0.0)
        rows.append(
            f"<div class='bar-row'><span>{html.escape(label)}</span><div><i style='width:{score * 100:.1f}%;background:{color}'></i></div><b>{score:.3f}</b></div>"
        )
    return f"<div class='bars'>{''.join(rows)}</div>"


def _value_heatmap(rows: list[dict[str, Any]], key: str, low_color: str, high_color: str) -> str:
    if not rows:
        return "<div class='regime-strip empty'>Not enough data</div>"
    cells = []
    for row in rows[-90:]:
        value = max(0.0, min(1.0, float(row.get(key) or 0.0)))
        alpha = 0.25 + value * 0.75
        date = html.escape(str(row.get("date", "")))
        cells.append(
            f"<span title='{date} {_fmt(value)}' style='background:{high_color};opacity:{alpha:.2f}'></span>"
        )
    return f"<div class='regime-strip'>{''.join(cells)}</div>"


def _structure_strip(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "<div class='regime-strip empty'>Not enough data</div>"
    colors = {
        "balanced_structure": "#0f766e",
        "systemic_stress": "#be123c",
        "fragmented_dispersion": "#b45309",
        "flow_led_accumulation": "#1d4ed8",
        "noisy_transition": "#64748b",
        "trend_flow_aligned": "#7c3aed",
    }
    cells = []
    for row in rows[-90:]:
        state = str(row.get("structure_state", "balanced_structure"))
        date = html.escape(str(row.get("date", "")))
        cells.append(
            f"<span title='{date} {html.escape(state)}' style='background:{colors.get(state, '#64748b')}'></span>"
        )
    return f"<div class='regime-strip'>{''.join(cells)}</div>"


def _anomaly_strip(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "<div class='regime-strip empty'>Not enough data</div>"
    colors = {
        "low": "#0f766e",
        "medium": "#b45309",
        "high": "#be123c",
    }
    cells = []
    for row in rows[-90:]:
        risk = str(row.get("systemic_risk_level", "low"))
        state = html.escape(str(row.get("anomaly_state", "")))
        date = html.escape(str(row.get("date", "")))
        cells.append(
            f"<span title='{date} {state}' style='background:{colors.get(risk, '#64748b')}'></span>"
        )
    return f"<div class='regime-strip'>{''.join(cells)}</div>"


def _page(content: str) -> str:
    return f"""
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>TenBagger</title>
      <style>
        :root {{
          color-scheme: light;
          --ink: #18202a;
          --muted: #647184;
          --line: #d8dee8;
          --panel: #ffffff;
          --bg: #f4f6f8;
          --accent: #0f766e;
        }}
        * {{ box-sizing: border-box; }}
        body {{
          margin: 0;
          font-family: Inter, "Segoe UI", Arial, sans-serif;
          background: var(--bg);
          color: var(--ink);
        }}
        .shell {{
          max-width: 1180px;
          margin: 0 auto;
          padding: 28px;
        }}
        .topbar {{
          display: flex;
          align-items: flex-end;
          justify-content: space-between;
          gap: 24px;
          margin-bottom: 20px;
        }}
        h1, h2, p {{ margin: 0; }}
        h1 {{ font-size: 30px; line-height: 1.1; }}
        h2 {{ font-size: 18px; margin: 24px 0 10px; }}
        p, .stamp {{ color: var(--muted); }}
        .metrics {{
          display: grid;
          grid-template-columns: repeat(4, minmax(0, 1fr));
          gap: 12px;
        }}
        .metric {{
          background: var(--panel);
          border: 1px solid var(--line);
          border-radius: 8px;
          padding: 16px;
          min-height: 88px;
        }}
        .metric span {{
          display: block;
          color: var(--muted);
          font-size: 13px;
          margin-bottom: 8px;
        }}
        .metric strong {{
          display: block;
          font-size: 22px;
          overflow-wrap: anywhere;
        }}
        .grid {{
          display: grid;
          grid-template-columns: 0.8fr 1.2fr;
          gap: 18px;
        }}
        table {{
          width: 100%;
          border-collapse: collapse;
          background: var(--panel);
          border: 1px solid var(--line);
          border-radius: 8px;
          overflow: hidden;
        }}
        th, td {{
          text-align: left;
          padding: 10px 12px;
          border-bottom: 1px solid var(--line);
          font-size: 13px;
          white-space: nowrap;
        }}
        th {{
          color: var(--muted);
          font-weight: 600;
          background: #eef2f5;
        }}
        tr:last-child td {{ border-bottom: 0; }}
        .empty {{
          background: var(--panel);
          border: 1px solid var(--line);
          border-radius: 8px;
          padding: 24px;
        }}
        .chart {{
          display: block;
          width: 100%;
          height: 150px;
          background: var(--panel);
          border: 1px solid var(--line);
          border-radius: 8px;
        }}
        .chart rect {{
          fill: #ffffff;
        }}
        .regime-strip {{
          display: grid;
          grid-template-columns: repeat(90, minmax(4px, 1fr));
          gap: 2px;
          background: var(--panel);
          border: 1px solid var(--line);
          border-radius: 8px;
          padding: 12px;
        }}
        .regime-strip span {{
          display: block;
          min-height: 26px;
          border-radius: 3px;
        }}
        .bars {{
          background: var(--panel);
          border: 1px solid var(--line);
          border-radius: 8px;
          padding: 14px;
        }}
        .bar-row {{
          display: grid;
          grid-template-columns: 110px 1fr 64px;
          align-items: center;
          gap: 10px;
          margin: 10px 0;
          font-size: 13px;
        }}
        .bar-row div {{
          height: 14px;
          background: #e5e7eb;
          border-radius: 999px;
          overflow: hidden;
        }}
        .bar-row i {{
          display: block;
          height: 100%;
        }}
        @media (max-width: 860px) {{
          .shell {{ padding: 18px; }}
          .topbar {{ display: block; }}
          .stamp {{ margin-top: 8px; }}
          .metrics, .grid {{ grid-template-columns: 1fr; }}
          table {{ display: block; overflow-x: auto; }}
        }}
      </style>
    </head>
    <body>{content}</body>
    </html>
    """
