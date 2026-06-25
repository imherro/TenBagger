from __future__ import annotations

from tenbagger.web_app import _page


def test_page_embeds_unified_myinvest_chrome() -> None:
    page = _page("<main class='shell'>content</main>")

    assert "data-myinvest-header" in page
    assert "data-myinvest-footer" in page
    assert "https://invest.okbbc.com/header.js" in page
    assert "https://invest.okbbc.com/footer.js" in page
    assert "https://invest.okbbc.com/api/header" in page
    assert "https://invest.okbbc.com/api/footer" in page
