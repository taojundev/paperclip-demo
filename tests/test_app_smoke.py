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


def _language_toggle(app: AppTest) -> None:
    next(
        button for button in app.button if "🌐" in button.label
    ).click().run()
    assert not app.exception, [e.value for e in app.exception]


def test_overview_renders_in_english_by_default() -> None:
    app = _run()
    assert any("Beijing" in button.label for button in app.button)
    assert any("🌐 中文" in button.label for button in app.button)
    assert any("☀️ Light mode" in button.label for button in app.button)
    assert app.session_state["theme"] == "dark"
    assert app.markdown, "expected custom HTML sections"
    assert "Weather across" in " ".join(section.value for section in app.markdown)


def test_theme_toggle_switches_light_and_dark() -> None:
    app = _run()
    assert app.session_state["theme"] == "dark"

    next(button for button in app.button if "Light mode" in button.label).click().run()
    assert not app.exception, [e.value for e in app.exception]
    assert app.session_state["theme"] == "light"
    assert any("Dark mode" in button.label for button in app.button)
    assert not any("Light mode" in button.label for button in app.button)
    assert "--bg: #f6f8ff" in " ".join(section.value for section in app.markdown)

    # The light theme survives navigation and can be switched back.
    next(button for button in app.button if "Beijing" in button.label).click().run()
    assert not app.exception
    assert app.session_state["theme"] == "light"
    assert "--bg: #f6f8ff" in " ".join(section.value for section in app.markdown)

    next(button for button in app.button if "Dark mode" in button.label).click().run()
    assert not app.exception
    assert app.session_state["theme"] == "dark"
    assert any("Light mode" in button.label for button in app.button)
    assert "--bg: #f6f8ff" not in " ".join(section.value for section in app.markdown)


def test_chinese_toggle_switches_interface() -> None:
    app = _run()
    _language_toggle(app)

    assert any("北京" in button.label for button in app.button)
    assert any("🌐 English" in button.label for button in app.button)
    assert not any("Beijing" in button.label for button in app.button)
    assert "看遍" in " ".join(section.value for section in app.markdown)

    # Toggling back restores the English interface.
    _language_toggle(app)
    assert any("Beijing" in button.label for button in app.button)


def test_open_city_and_go_back() -> None:
    app = _run()
    next(button for button in app.button if "Beijing" in button.label).click().run()
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


def test_chinese_detail_page() -> None:
    app = _run()
    _language_toggle(app)
    next(button for button in app.button if "北京" in button.label).click().run()
    assert not app.exception, [e.value for e in app.exception]
    assert dict(app.query_params).get("city") == "beijing"
    assert [tab.label for tab in app.tabs] == [
        "📈 未来 24 小时",
        "🗺️ 天气地图",
        "🌅 日出与空气",
    ]

    next(button for button in app.button if "所有城市" in button.label).click().run()
    assert not app.exception
    assert not dict(app.query_params)


def test_search_and_unit_switch() -> None:
    app = _run()
    app.text_input[0].set_value("上海").run()
    assert not app.exception
    city_buttons = [b for b in app.button if "Shanghai" in b.label]
    assert city_buttons

    app.text_input[0].set_value("no-such-city").run()
    assert not app.exception
    assert app.info and "No cities match" in app.info[0].value

    app.segmented_control[0].set_value("°F").run()
    assert not app.exception
    assert app.segmented_control[0].value == "°F"


def test_language_toggle_keeps_search_results() -> None:
    app = _run()
    app.text_input[0].set_value("上海").run()
    _language_toggle(app)
    assert not app.exception
    assert any("上海" in button.label for button in app.button)
