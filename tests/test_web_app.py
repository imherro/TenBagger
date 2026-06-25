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


def test_stock_code_link_opens_xueqiu_in_new_window() -> None:
    linked = _stock_code_link("603259.SH")

    assert "603259.SH" in linked
    assert 'href="https://xueqiu.com/S/SH603259"' in linked
    assert 'target="_blank"' in linked
    assert 'rel="noopener noreferrer"' in linked
    assert ">Xueqiu</a>" in linked
