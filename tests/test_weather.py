"""Offline tests for data shaping and HTML fragments."""

from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from weather_dashboard import CITIES, demo_detail, demo_overview
from weather_dashboard.api import _normalise_overview
from weather_dashboard.cities import weather_code_info
from weather_dashboard.components import (
    convert_temp,
    daily_html,
    detail_hero_html,
    extremes_html,
    footer_html,
    hero_html,
    hourly_chart,
    map_chart,
    metrics_html,
    stats_html,
    sun_air_html,
    temp_text,
)

NOW = datetime(2026, 7, 15, 14, 30, tzinfo=ZoneInfo("Asia/Shanghai"))
BY_SLUG = {city.slug: city for city in CITIES}


def _markdown_breaks(html: str) -> list[int]:
    """Lines that would make Streamlit's markdown parser drop out of HTML."""

    lines = html.splitlines()
    return [
        index
        for index, line in enumerate(lines)
        if 0 < index < len(lines) - 1 and not line.strip()
    ]


def test_city_catalogue_is_consistent() -> None:
    assert len(CITIES) == 35
    assert len(BY_SLUG) == len(CITIES)
    for city in CITIES:
        assert -90 <= city.lat <= 90
        assert -180 <= city.lon <= 180
        assert city.name_zh and city.name_en


def test_demo_overview_shapes() -> None:
    overview = demo_overview(CITIES, NOW)
    assert set(overview) == {city.slug for city in CITIES}
    for weather in overview.values():
        assert weather["low"] <= weather["high"]
        assert 0 <= weather["rain_chance"] <= 100
        assert 0 <= weather["humidity"] <= 100
        assert weather["condition"]["emoji"]


def test_demo_detail_windows() -> None:
    for city in CITIES:
        detail = demo_detail(city, NOW)
        assert len(detail["hourly"]["time"]) == 24
        assert len(detail["daily"]["time"]) == 7
        assert detail["current"]["condition"]["label_en"]
        assert detail["air"] and detail["air"]["european_aqi"] >= 0
        assert len(hourly_chart(detail).data) >= 3


@pytest.mark.parametrize(
    "code,expected",
    [(0, "Clear sky"), (95, "Thunderstorm"), (999, "Unknown"), (None, "Clear sky")],
)
def test_weather_code_labels(code: int | None, expected: str) -> None:
    assert weather_code_info(code)["label_en"] == expected


def test_normalise_overview_tolerates_missing_fields() -> None:
    weather = _normalise_overview({"current": {}, "daily": {}})
    assert weather["temp"] == 0
    assert weather["high"] == 0
    assert weather["condition"]["label_en"] == "Clear sky"


def test_temperature_conversion() -> None:
    assert convert_temp(0, "°C") == 0
    assert convert_temp(0, "°F") == 32
    assert temp_text(20, "°C") == "20°"
    assert temp_text(20, "°F") == "68°"


@pytest.mark.parametrize("unit", ["°C", "°F"])
def test_html_fragments_have_no_blank_lines(unit: str) -> None:
    overview = demo_overview(CITIES, NOW)
    detail = demo_detail(BY_SLUG["shanghai"], NOW)
    city = BY_SLUG["shanghai"]

    fragments = [
        hero_html(NOW, True, len(CITIES)),
        stats_html(overview, BY_SLUG, unit),
        extremes_html(CITIES, overview, unit),
        detail_hero_html(city, detail, unit),
        metrics_html(detail, unit),
        daily_html(detail, unit),
        sun_air_html(detail, unit),
        footer_html("live", "14:30"),
    ]
    for fragment in fragments:
        assert not _markdown_breaks(fragment), "blank line would break the HTML block"


def test_charts_render() -> None:
    overview = demo_overview(CITIES, NOW)
    detail = demo_detail(BY_SLUG["beijing"], NOW)
    assert len(map_chart(CITIES, overview, "beijing", "°C").data) == 2
    assert len(hourly_chart(detail, "°F").data) >= 4
