from __future__ import annotations

from tenbagger.web_app import _page, _stock_code_link, _xueqiu_symbol


def test_page_embeds_unified_myinvest_chrome() -> None:
    page = _page("<main class='shell'>content</main>")

    assert "data-myinvest-header" in page
    assert "data-myinvest-footer" in page
    assert "https://invest.okbbc.com/header.js" in page
    assert "https://invest.okbbc.com/footer.js" in page
    assert "https://invest.okbbc.com/api/header" in page
    assert "https://invest.okbbc.com/api/footer" in page


def test_xueqiu_symbol_converts_a_share_codes() -> None:
    assert _xueqiu_symbol("603259.SH") == "SH603259"
    assert _xueqiu_symbol("000001.SZ") == "SZ000001"
    assert _xueqiu_symbol("SH603259") == "SH603259"
    assert _xueqiu_symbol("S0") is None


def test_stock_code_link_uses_code_for_xueqiu_and_name_for_research() -> None:
    linked = _stock_code_link("603259.SH", "药明康德")

    assert ">603259.SH</a>" in linked
    assert 'href="https://xueqiu.com/S/SH603259"' in linked
    assert 'href="https://stock.okbbc.com/research?stock=603259.SH"' in linked
    assert 'target="_blank"' in linked
    assert 'rel="noopener noreferrer"' in linked
    assert ">药明康德</a>" in linked
    assert ">Xueqiu</a>" not in linked


def test_page_adds_chinese_hover_explanations() -> None:
    page = _page(
        """
        <main class="shell">
          <h1>TenBagger</h1>
          <section class="metrics"><div class="metric"><span>Stocks</span><strong>10</strong></div></section>
          <h2>Missing Rates</h2>
          <table>
            <thead><tr><th>ROE</th><th>RankIC</th></tr></thead>
            <tbody><tr><td>annual_return</td><td>0.1</td></tr></tbody>
          </table>
        </main>
        """
    )

    assert 'class="help"' in page
    assert "十倍股寻找系统" in page
    assert 'title="字段缺失率；越低说明基础数据越完整。"' in page
    assert 'title="净资产收益率，衡量公司赚钱效率。"' in page
    assert 'title="年化收益率；把区间收益换算成年维度。"' in page
