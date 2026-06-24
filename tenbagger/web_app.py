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

    @app.get("/", response_class=HTMLResponse)
    def index() -> str:
        report = _load_report(report_path)
        factor_report = _load_report(factor_report_path)
        screener_report = _load_report(screener_report_path)
        backtest_report = _load_report(backtest_report_path)
        optimization_report = _load_report(optimization_report_path)
        monetization_report = _load_report(monetization_report_path)
        structural_report = _load_report(structural_report_path)
        return _render_dashboard(
            report,
            factor_report,
            screener_report,
            backtest_report,
            optimization_report,
            monetization_report,
            structural_report,
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
