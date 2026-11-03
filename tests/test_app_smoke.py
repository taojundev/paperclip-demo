"""End-to-end smoke tests that drive the Streamlit app headlessly."""

from __future__ import annotations

from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"


def _run() -> AppTest:
    app = AppTest.from_file(str(APP), default_timeout=120)
    app.run()
    assert not app.exception, [e.value for e in app.exception]
    return app


def test_overview_renders() -> None:
    app = _run()
    assert any("北京" in button.label for button in app.button)
    assert app.markdown, "expected custom HTML sections"


def test_open_city_and_go_back() -> None:
    app = _run()
    next(button for button in app.button if "北京" in button.label).click().run()
    assert not app.exception, [e.value for e in app.exception]
    assert dict(app.query_params).get("city") == "beijing"
    assert [tab.label for tab in app.tabs] == [
        "📈 Next 24 hours",
        "🗺️ Weather map",
        "🌅 Sun & air",
    ]

    next(button for button in app.button if "All cities" in button.label).click().run()
    assert not app.exception
    assert not dict(app.query_params)


def test_search_and_unit_switch() -> None:
    app = _run()
    app.text_input[0].set_value("上海").run()
    assert not app.exception
    city_buttons = [b for b in app.button if "上海" in b.label]
    assert city_buttons

    app.text_input[0].set_value("no-such-city").run()
    assert not app.exception
    assert app.info and "No cities match" in app.info[0].value

    app.segmented_control[0].set_value("°F").run()
    assert not app.exception
