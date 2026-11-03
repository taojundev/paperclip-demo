"""HTML fragments and Plotly charts used by the dashboard."""

from __future__ import annotations

import html
import math
from datetime import datetime
from typing import Iterable, Sequence

import plotly.graph_objects as go

from .cities import City, weather_code_info
from .i18n import (
    condition_label,
    format_date,
    month_day,
    province_label,
    region_label,
    t,
    weekday_short,
    wind_direction_name as _wind_direction_name,
)

UNIT_LABEL = {"°C": "°C", "°F": "°F"}


# Chart colours for each UI theme. Plotly charts are rendered server-side, so
# they need an explicit palette rather than inheriting the page CSS.
_CHART_PALETTES = {
    "dark": {
        "text": "#aab5d8",
        "tick": "#96a2c8",
        "axis_title": "#6c789e",
        "grid_y": "rgba(148,163,255,0.09)",
        "grid_x": "rgba(148,163,255,0.05)",
        "night": "rgba(8, 12, 30, 0.42)",
        "rain_bar": "rgba(110, 231, 216, 0.20)",
        "temp_line": "#8fa8ff",
        "temp_marker": "#c9d6ff",
        "temp_fill": "rgba(124, 155, 255, 0.13)",
        "now_marker": "#6ee7d8",
        "now_marker_line": "#0a1024",
        "hover_bg": "#111832",
        "hover_border": "rgba(148,163,255,0.25)",
        "hover_text": "#eef2ff",
        "land": "#141b36",
        "ocean": "#080d1d",
        "lake": "#0b1226",
        "country": "rgba(148,163,255,0.22)",
        "coastline": "rgba(148,163,255,0.25)",
        "colorbar": "#96a2c8",
        "selected_text": "#ffffff",
        "selected_line": "#ffd06b",
    },
    "light": {
        "text": "#44527a",
        "tick": "#5c6a91",
        "axis_title": "#6b789a",
        "grid_y": "rgba(59,78,140,0.10)",
        "grid_x": "rgba(59,78,140,0.06)",
        "night": "rgba(59,78,140,0.07)",
        "rain_bar": "rgba(15, 156, 143, 0.18)",
        "temp_line": "#4f6bed",
        "temp_marker": "#ffffff",
        "temp_fill": "rgba(79, 107, 237, 0.10)",
        "now_marker": "#0f9c8f",
        "now_marker_line": "#ffffff",
        "hover_bg": "#ffffff",
        "hover_border": "rgba(59,78,140,0.18)",
        "hover_text": "#17203a",
        "land": "#e8eef9",
        "ocean": "#dbe8f7",
        "lake": "#d3e3f5",
        "country": "rgba(59,78,140,0.20)",
        "coastline": "rgba(59,78,140,0.26)",
        "colorbar": "#5c6a91",
        "selected_text": "#17203a",
        "selected_line": "#e0a200",
    },
}


def _chart_palette(theme: str = "dark") -> dict[str, str]:
    return _CHART_PALETTES["light" if theme == "light" else "dark"]


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------


def _safe(value: object) -> str:
    return html.escape(str(value))


def convert_temp(celsius: float, unit: str) -> float:
    return celsius if unit == "°C" else celsius * 9 / 5 + 32


def temp_text(celsius: float, unit: str, include_unit: bool = False) -> str:
    value = convert_temp(celsius, unit)
    suffix = unit if include_unit else "°"
    return f"{value:.0f}{suffix}"


def temp_decimal(celsius: float, unit: str) -> str:
    value = convert_temp(celsius, unit)
    return f"{value:.1f}"


def wind_direction_name(degrees: float | int, lang: str = "en") -> str:
    return _wind_direction_name(degrees, lang)


def aqi_info(aqi: int, lang: str = "en") -> tuple[str, str]:
    if aqi <= 20:
        return t("aqi_good", lang), "#6ee7b7"
    if aqi <= 40:
        return t("aqi_fair", lang), "#a3e635"
    if aqi <= 60:
        return t("aqi_moderate", lang), "#fbbf24"
    if aqi <= 80:
        return t("aqi_poor", lang), "#fb923c"
    if aqi <= 100:
        return t("aqi_very_poor", lang), "#f87171"
    return t("aqi_extremely_poor", lang), "#c084fc"


def uv_info(uv: float, lang: str = "en") -> tuple[str, str]:
    if uv < 3:
        return t("uv_low", lang), "#6ee7b7"
    if uv < 6:
        return t("uv_moderate", lang), "#fbbf24"
    if uv < 8:
        return t("uv_high", lang), "#fb923c"
    if uv < 11:
        return t("uv_very_high", lang), "#f87171"
    return t("uv_extreme", lang), "#c084fc"


def _kind_glow(kind: str) -> str:
    return {
        "clear": "rgba(255, 184, 107, 0.30)",
        "cloudy": "rgba(124, 155, 255, 0.24)",
        "rain": "rgba(96, 165, 250, 0.30)",
        "storm": "rgba(167, 139, 250, 0.32)",
        "snow": "rgba(186, 230, 253, 0.28)",
        "fog": "rgba(148, 163, 184, 0.26)",
    }.get(kind, "rgba(124, 155, 255, 0.24)")


# ---------------------------------------------------------------------------
# Overview
# ---------------------------------------------------------------------------


def hero_html(
    now: datetime,
    live: bool,
    city_count: int,
    lang: str = "en",
) -> str:
    status = (
        f'<span class="pill"><span class="live-dot"></span> {t("hero_live", lang)}</span>'
        if live
        else f'<span class="pill"><span class="demo-dot"></span> {t("hero_demo", lang)}</span>'
    )
    return f"""
<div class="hero">
  <div class="hero-kicker"><span class="dot"></span> {t('hero_kicker', lang)}</div>
  <h1>{t('hero_title', lang)}</h1>
  <p class="hero-sub">
    {t('hero_sub', lang, city_count=city_count)}
  </p>
  <div class="hero-meta">
    <span class="pill">🗓️ <strong>{_safe(format_date(now, lang))}</strong></span>
    <span class="pill">🕘 <strong>{_safe(now.strftime("%H:%M"))}</strong> {t('hero_timezone', lang)}</span>
    {status}
    <span class="pill">📍 <strong>{city_count}</strong> {t('hero_cities', lang)}</span>
  </div>
</div>
"""


def stats_html(
    overview: dict[str, dict],
    by_slug: dict[str, City],
    unit: str,
    lang: str = "en",
) -> str:
    if not overview:
        return ""
    hottest_slug = max(overview, key=lambda slug: overview[slug].get("temp", -99))
    coldest_slug = min(overview, key=lambda slug: overview[slug].get("temp", 99))
    wettest_slug = max(overview, key=lambda slug: overview[slug].get("rain_chance", 0))
    hottest = overview[hottest_slug]
    coldest = overview[coldest_slug]
    wettest = overview[wettest_slug]

    def city_name(slug: str) -> str:
        city = by_slug.get(slug)
        if not city:
            return slug
        return city.name_zh if lang == "zh" else city.name_en

    city_count = f"{len(overview)} {t('hero_cities', lang)}"
    items = [
        (
            "🔥",
            t("stat_hottest", lang),
            f"{city_name(hottest_slug)} · {temp_text(hottest['temp'], unit)}",
            t("stat_feels", lang, temp=temp_text(hottest["feels"], unit)),
        ),
        (
            "🧊",
            t("stat_coldest", lang),
            f"{city_name(coldest_slug)} · {temp_text(coldest['temp'], unit)}",
            t("stat_low_tonight", lang, temp=temp_text(coldest["low"], unit)),
        ),
        (
            "🌧️",
            t("stat_wettest", lang),
            f"{city_name(wettest_slug)} · {wettest['rain_chance']}%",
            t("stat_max_prob", lang),
        ),
        (
            "🛰️",
            t("stat_coverage", lang),
            city_count,
            t("stat_coverage_sub", lang),
        ),
    ]
    cards = "".join(
        f"""
        <div class="stat">
          <div class="stat-icon">{icon}</div>
          <div>
            <div class="stat-label">{_safe(label)}</div>
            <div class="stat-value">{_safe(value)}</div>
            <div class="stat-sub">{_safe(sub)}</div>
          </div>
        </div>"""
        for icon, label, value, sub in items
    )
    return f'<div class="stats">{cards}</div>'


def _heat_color(value: float, low: float, high: float) -> str:
    """Interpolate a cold-to-hot colour for a temperature value."""
    span = max(0.01, high - low)
    ratio = max(0.0, min(1.0, (value - low) / span))
    stops = [(0.0, (90, 169, 255)), (0.45, (110, 231, 216)), (0.7, (251, 191, 36)), (1.0, (255, 95, 126))]
    for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
        if ratio <= p1:
            f = (ratio - p0) / (p1 - p0)
            rgb = tuple(round(a + (b - a) * f) for a, b in zip(c0, c1))
            return f"rgb{rgb}"
    return "rgb(255, 95, 126)"


def extremes_html(
    cities: Sequence[City],
    overview: dict[str, dict],
    unit: str,
    lang: str = "en",
) -> str:
    """A compact warmest/coldest ladder that sits beside the map."""

    shown = [city for city in cities if city.slug in overview]
    if not shown:
        return ""
    temps = [overview[city.slug]["temp"] for city in shown]
    low, high = min(temps), max(temps)
    ranked = sorted(shown, key=lambda city: overview[city.slug]["temp"], reverse=True)
    warm = ranked[:4]
    cold = list(reversed(ranked[-4:]))

    def row(city: City) -> str:
        weather = overview[city.slug]
        temp = weather["temp"]
        color = _heat_color(temp, low, high)
        width = 8 + 92 * (temp - low) / max(0.01, high - low)
        info = weather.get("condition") or {}
        rank = ranked.index(city) + 1
        name = city.name_zh if lang == "zh" else city.name_en
        condition = condition_label(info, lang)
        return (
            f'<div class="ladder-row"><span class="ladder-rank">{rank:02d}</span>'
            f'<span class="ladder-name">{_safe(name)}'
            f'<small>{_safe(info.get("emoji", ""))} {_safe(condition)}</small></span>'
            f'<span class="ladder-val" style="color:{color}">{temp_text(temp, unit)}</span>'
            f'<span class="ladder-bar"><i style="width:{width:.0f}%;background:{color}"></i></span>'
            "</div>"
        )

    warm_rows = "".join(row(city) for city in warm)
    cold_rows = "".join(row(city) for city in cold)
    return (
        '<div class="map-side">'
        f'<div class="map-side-head"><h3>{t("ladder_title", lang)}</h3>'
        f'<p>{t("ladder_sub", lang, count=len(shown))}</p></div>'
        f'<div class="ladder-label"><span>{t("ladder_warm", lang)}</span><span>{temp_text(high, unit)}</span></div>'
        f'{warm_rows}'
        f'<div class="ladder-label cold"><span>{t("ladder_cold", lang)}</span><span>{temp_text(low, unit)}</span></div>'
        f'{cold_rows}'
        f'<div class="map-side-foot">{t("ladder_foot", lang)}</div>'
        "</div>"
    )


def city_card_css(
    overview: dict[str, dict],
    cities: Sequence[City],
    theme: str = "dark",
) -> str:
    """Per-city gradients generated from live temperature and condition."""

    palettes = {
        "clear": ("rgba(255, 184, 107, 0.20)", "rgba(255, 122, 138, 0.07)", "rgba(255, 184, 107, 0.42)"),
        "cloudy": ("rgba(124, 155, 255, 0.20)", "rgba(110, 231, 216, 0.06)", "rgba(124, 155, 255, 0.42)"),
        "rain": ("rgba(96, 165, 250, 0.22)", "rgba(110, 231, 216, 0.07)", "rgba(96, 165, 250, 0.48)"),
        "storm": ("rgba(167, 139, 250, 0.24)", "rgba(96, 165, 250, 0.08)", "rgba(167, 139, 250, 0.5)"),
        "snow": ("rgba(186, 230, 253, 0.20)", "rgba(124, 155, 255, 0.07)", "rgba(186, 230, 253, 0.44)"),
        "fog": ("rgba(148, 163, 184, 0.18)", "rgba(124, 155, 255, 0.06)", "rgba(148, 163, 184, 0.38)"),
    }
    light = theme == "light"
    card_bg = (
        "linear-gradient(152deg, rgba(255, 255, 255, 0.97), rgba(242, 246, 255, 0.94))"
        if light
        else "linear-gradient(152deg, rgba(26, 34, 66, 0.94), rgba(11, 16, 35, 0.9))"
    )
    card_border = "rgba(59, 78, 140, 0.14)" if light else "rgba(148, 163, 255, 0.18)"
    hover_shadow = (
        "0 16px 34px rgba(40, 58, 120, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.9)"
        if light
        else "0 16px 40px rgba(5, 9, 24, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.08)"
    )
    rules = []
    for city in cities:
        weather = overview.get(city.slug)
        if not weather:
            continue
        kind = weather.get("condition", {}).get("kind", "cloudy")
        top, bottom, border = palettes.get(kind, palettes["cloudy"])
        rules.append(
            f"""
.st-key-city_{city.slug} button {{
  background:
    radial-gradient(220px 120px at 12% 0%, {top}, transparent 70%),
    {card_bg};
  border-color: {card_border};
}}
.st-key-city_{city.slug} button:hover {{
  border-color: {border};
  box-shadow: {hover_shadow};
}}"""
        )
    return "<style>" + "".join(rules) + "</style>"


def city_labels(
    city: City,
    weather: dict,
    unit: str,
    lang: str = "en",
) -> tuple[str, str]:
    info = weather.get("condition") or weather_code_info(weather.get("code", 0), True)
    name = city.name_zh if lang == "zh" else city.name_en
    condition = condition_label(info, lang)
    label = (
        f"{info['emoji']} {name}  \n"
        f"{temp_text(weather['temp'], unit)} · {condition}"
    )
    foot = (
        f"<div class='city-foot'><span>{_safe(province_label(city.province, lang))}</span>"
        f"<span>{temp_text(weather['high'], unit)} / {temp_text(weather['low'], unit)}"
        f" · 💧 {weather['humidity']}%</span></div>"
    )
    return label, foot


# ---------------------------------------------------------------------------
# Detail header and alerts
# ---------------------------------------------------------------------------


def detail_hero_html(
    city: City,
    detail: dict,
    unit: str,
    lang: str = "en",
) -> str:
    current = detail["current"]
    info = current["condition"]
    updated = current.get("time", "")[11:16]
    zh = lang == "zh"
    primary_name = city.name_zh if zh else city.name_en
    secondary_name = city.name_en if zh else city.name_zh
    primary_condition = info["label_zh"] if zh else info["label_en"]
    secondary_condition = info["label_en"] if zh else info["label_zh"]
    current_label = condition_label(weather_code_info(current["code"], True), lang)
    return f"""
<div class="detail-hero" style="--glow: {_kind_glow(info['kind'])};">
  <div>
    <div class="crumb">{t('crumb', lang, region=_safe(region_label(city.region, lang)), province=_safe(province_label(city.province, lang)))}</div>
    <h1>{_safe(primary_name)}<span>{_safe(secondary_name)}</span></h1>
    <div class="detail-cond">
      <span>{info['emoji']}</span>
      <span class="zh">{_safe(primary_condition)}</span>
      <span class="en">{_safe(secondary_condition)}</span>
    </div>
    <div class="detail-chips">
      <span class="chip">{t('chip_feels', lang, temp=temp_text(current['feels'], unit))}</span>
      <span class="chip">{t('chip_high_low', lang, high=temp_text(current['high'], unit), low=temp_text(current['low'], unit))}</span>
      <span class="chip">{t('chip_humidity', lang, value=current['humidity'])}</span>
      <span class="chip">{t('chip_wind', lang, value=f"{current['wind']:.0f}", direction=_safe(wind_direction_name(current['wind_dir'], lang)))}</span>
      <span class="chip">{t('chip_rain', lang, value=current['rain_chance'])}</span>
    </div>
  </div>
  <div class="now-panel">
    <div class="now-emoji">{info['emoji']}</div>
    <div class="temp-now">{temp_text(current['temp'], unit)}<sup>{unit}</sup></div>
    <div class="updated">{t('now_updated', lang, time=_safe(updated), condition=_safe(current_label))}</div>
  </div>
</div>
"""


def alerts_html(
    city: City,
    detail: dict,
    unit: str,
    lang: str = "en",
) -> str:
    current = detail["current"]
    daily = detail["daily"]
    air = detail.get("air") or {}
    alerts: list[tuple[str, str, str, str]] = []

    high = daily["high"][0] if daily["high"] else current["high"]
    low = daily["low"][0] if daily["low"] else current["low"]
    rain = daily["rain_chance"][0] if daily["rain_chance"] else current["rain_chance"]
    wind = daily["wind_max"][0] if daily["wind_max"] else current["wind"]

    if current["condition"]["kind"] == "storm":
        alerts.append(("danger", "⛈️", t("alert_storm_title", lang), t("alert_storm_body", lang)))
    if high >= 35:
        alerts.append(("danger", "🥵", t("alert_heat_title", lang), t("alert_heat_body", lang, temp=temp_text(high, unit))))
    elif high >= 32:
        alerts.append(("info", "☀️", t("alert_hot_title", lang), t("alert_hot_body", lang, temp=temp_text(high, unit))))
    if low <= -5:
        alerts.append(("info", "🧣", t("alert_cold_title", lang), t("alert_cold_body", lang, temp=temp_text(low, unit))))
    if rain >= 60:
        alerts.append(("info", "☔", t("alert_rain_title", lang), t("alert_rain_body", lang, rain=rain)))
    if wind >= 40:
        alerts.append(("info", "💨", t("alert_wind_title", lang), t("alert_wind_body", lang, wind=f"{wind:.0f}")))
    aqi = air.get("european_aqi", 0)
    if aqi >= 80:
        label, _ = aqi_info(aqi, lang)
        alerts.append(("danger", "😷", t("alert_aqi_title", lang, label=label), t("alert_aqi_body", lang, aqi=aqi)))

    if not alerts:
        return ""
    body = "".join(
        f'<div class="alert {level}"><span class="a-icon">{icon}</span>'
        f"<div><b>{_safe(title)}</b> — {_safe(message)}</div></div>"
        for level, icon, title, message in alerts[:2]
    )
    return body


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------


def _metric(
    icon: str,
    label: str,
    value: str,
    sub: str = "",
    bar: float | None = None,
    accent: str | None = None,
) -> str:
    bar_html = ""
    if bar is not None:
        width = max(0.0, min(100.0, bar))
        style = f"width:{width:.0f}%;"
        if accent:
            style += f"background:{accent};"
        bar_html = f'<div class="m-bar"><span style="{style}"></span></div>'
    return (
        '<div class="metric">'
        f'<div class="m-top"><span class="m-label">{_safe(label)}</span><span class="m-icon">{icon}</span></div>'
        f'<div class="m-value">{value}</div>'
        f'<div class="m-sub">{_safe(sub)}</div>'
        f'{bar_html}'
        "</div>"
    )


def metrics_html(detail: dict, unit: str, lang: str = "en") -> str:
    current = detail["current"]
    air = detail.get("air") or {}
    uv = current.get("uv", 0)
    uv_label, uv_color = uv_info(uv, lang)
    aqi = air.get("european_aqi")
    aqi_label, aqi_color = aqi_info(aqi, lang) if aqi is not None else ("—", "#96a2c8")
    rain = current.get("rain_chance", 0)
    visibility = current.get("visibility", 0)
    direction = wind_direction_name(current["wind_dir"], lang)

    items = [
        _metric("🌡️", t("metric_feels", lang), f"{temp_text(current['feels'], unit)}<small>{unit}</small>", t("metric_actual", lang, temp=temp_text(current['temp'], unit)), None),
        _metric("💧", t("metric_humidity", lang), f"{current['humidity']}%", t("metric_relative_humidity", lang), current["humidity"]),
        _metric("💨", t("metric_wind", lang), f"{current['wind']:.0f}<small> km/h</small>", t("metric_from", lang, direction=direction, degrees=current['wind_dir']), min(100, current["wind"] * 2.2)),
        _metric("🧭", t("metric_pressure", lang), f"{current['pressure']:.0f}<small> hPa</small>", t("metric_surface_pressure", lang), (current["pressure"] - 980) / 60 * 100),
        _metric("👁️", t("metric_visibility", lang), f"{visibility:.0f}<small> km</small>", t("metric_horizontal_visibility", lang), min(100, visibility / 25 * 100)),
        _metric("🕶️", t("metric_uv", lang), f"{uv:.1f}", t("metric_uv_sub", lang, label=uv_label), min(100, uv / 11 * 100), uv_color),
        _metric("☔", t("metric_rain", lang), f"{rain}%", t("metric_rain_sub", lang), rain),
        _metric("🍃", t("metric_air", lang), f"{aqi if aqi is not None else '—'}<small> EAQI</small>", aqi_label, min(100, (aqi or 0) / 160 * 100), aqi_color),
    ]
    return f'<div class="metrics">{"".join(items)}</div>'


# ---------------------------------------------------------------------------
# 7-day forecast
# ---------------------------------------------------------------------------


def daily_html(detail: dict, unit: str, lang: str = "en") -> str:
    daily = detail["daily"]
    if not daily["time"]:
        return f"<p>{t('no_daily', lang)}</p>"

    week_low = min(daily["low"])
    week_high = max(daily["high"])
    span = max(0.1, week_high - week_low)
    cards = []
    for index, date_text in enumerate(daily["time"]):
        try:
            day = datetime.fromisoformat(date_text)
        except ValueError:
            day = None
        info = weather_code_info(daily["code"][index], True)
        high = daily["high"][index]
        low = daily["low"][index]
        left = max(0.0, min(100.0, (low - week_low) / span * 100))
        width = max(5.0, min(100.0 - left, (high - low) / span * 100))
        if index == 0:
            name = t("day_today", lang)
        elif day:
            name = weekday_short(day, lang)
        else:
            name = date_text
        date_label = month_day(day, lang) if day else ""
        rain = daily["rain_chance"][index]
        condition = condition_label(info, lang)
        cards.append(
            f"""
        <div class="day-card{' today' if index == 0 else ''}">
          <div class="day-name">{_safe(name)}</div>
          <div class="day-date">{_safe(date_label)}</div>
          <div class="day-icon">{info['day_emoji']}</div>
          <div class="day-cond" title="{_safe(condition)}">{_safe(condition)}</div>
          <div class="day-temps">{temp_text(high, unit)} <span class="lo">/ {temp_text(low, unit)}</span></div>
          <div class="day-range"><span style="left:{left:.0f}%;width:{width:.0f}%"></span></div>
          <div class="day-rain">💧 {rain}%</div>
        </div>"""
        )
    return f'<div class="forecast-strip">{"".join(cards)}</div>'


# ---------------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------------


def _base_layout(height: int = 370, theme: str = "dark") -> dict:
    palette = _chart_palette(theme)
    return dict(
        height=height,
        margin=dict(l=12, r=12, t=22, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, -apple-system, Segoe UI, sans-serif", color=palette["text"], size=12),
        hoverlabel=dict(
            bgcolor=palette["hover_bg"],
            bordercolor=palette["hover_border"],
            font=dict(color=palette["hover_text"], size=12),
        ),
        hovermode="x unified",
        showlegend=False,
    )


def hourly_chart(
    detail: dict,
    unit: str = "°C",
    lang: str = "en",
    theme: str = "dark",
) -> go.Figure:
    hourly = detail["hourly"]
    times = [datetime.fromisoformat(t) for t in hourly["time"]]
    temps = hourly["temp"]
    rain = hourly["rain_chance"]
    feels = hourly["feels"]
    humidity = hourly["humidity"]
    wind = hourly["wind"]
    precip = hourly["precip"]
    is_day = hourly["is_day"]
    palette = _chart_palette(theme)

    fig = go.Figure()

    # Shade night-time stretches.
    night_start = None
    for index, daylight in enumerate(is_day):
        if not daylight and night_start is None:
            night_start = index
        if daylight and night_start is not None:
            fig.add_vrect(x0=times[night_start], x1=times[index], fillcolor=palette["night"], line_width=0, layer="below")
            night_start = None
    if night_start is not None:
        fig.add_vrect(x0=times[night_start], x1=times[-1], fillcolor=palette["night"], line_width=0, layer="below")

    fig.add_trace(
        go.Bar(
            x=times,
            y=rain,
            name=t("chart_rain_chance", lang),
            marker=dict(color=palette["rain_bar"], line=dict(width=0)),
            yaxis="y2",
            hovertemplate=f"{t('chart_rain_chance', lang)} %{{y}}%<extra></extra>",
        )
    )

    base = min(temps) - max(3.0, (max(temps) - min(temps)) * 0.25)
    fig.add_trace(
        go.Scatter(
            x=times,
            y=[base] * len(times),
            mode="lines",
            line=dict(width=0),
            hoverinfo="skip",
            showlegend=False,
        )
    )
    converted = [convert_temp(t, unit) for t in temps]
    feels_converted = [convert_temp(t, unit) for t in feels]
    fig.add_trace(
        go.Scatter(
            x=times,
            y=converted,
            mode="lines+markers",
            name=t("chart_temperature", lang),
            line=dict(color=palette["temp_line"], width=3, shape="spline"),
            marker=dict(size=4, color=palette["temp_marker"], line=dict(color=palette["temp_line"], width=1)),
            fill="tonexty",
            fillcolor=palette["temp_fill"],
            customdata=list(zip(feels_converted, humidity, wind, precip)),
            hovertemplate=(
                f"<b>%{{x|%H:%M}}</b><br>{t('chart_temperature', lang)} %{{y:.0f}}{unit}<br>"
                f"{t('chart_feels', lang)} %{{customdata[0]:.0f}}{unit}<br>"
                f"{t('chart_humidity', lang)} %{{customdata[1]}}%<br>"
                f"{t('chart_wind', lang)} %{{customdata[2]:.0f}} km/h<br>"
                f"{t('chart_rain', lang)} %{{customdata[3]:.1f}} mm<extra></extra>"
            ),
        )
    )
    # Current-hour marker.
    fig.add_trace(
        go.Scatter(
            x=[times[0]],
            y=[converted[0]],
            mode="markers",
            marker=dict(size=12, color=palette["now_marker"], line=dict(color=palette["now_marker_line"], width=3)),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    layout = _base_layout(380, theme)
    layout.update(
        yaxis=dict(
            title=dict(text=t("chart_temp_axis", lang, unit=unit), font=dict(size=11, color=palette["axis_title"])),
            gridcolor=palette["grid_y"],
            zeroline=False,
            tickfont=dict(size=11),
            fixedrange=False,
        ),
        yaxis2=dict(
            overlaying="y",
            side="right",
            # Bars are drawn at a compressed scale so the temperature line stays
            # the hero; 100% rain fills roughly the lower third of the plot.
            range=[0, 260],
            showgrid=False,
            showticklabels=False,
            zeroline=False,
        ),
        xaxis=dict(
            gridcolor=palette["grid_x"],
            tickformat="%H:%M",
            tickfont=dict(size=11),
            showline=False,
            nticks=10,
        ),
        bargap=0.55,
    )
    fig.update_layout(**layout)
    return fig


def map_chart(
    cities: Sequence[City],
    overview: dict[str, dict],
    selected_slug: str,
    unit: str,
    lang: str = "en",
    theme: str = "dark",
) -> go.Figure:
    palette = _chart_palette(theme)
    shown = [city for city in cities if city.slug in overview]
    temps = [convert_temp(overview[city.slug]["temp"], unit) for city in shown]
    if not temps:
        temps = [0]
    low, high = min(temps), max(temps)
    if high - low < 2:
        low -= 1
        high += 1
    selected = next((city for city in shown if city.slug == selected_slug), None)

    fig = go.Figure()
    fig.add_trace(
        go.Scattergeo(
            lon=[city.lon for city in shown],
            lat=[city.lat for city in shown],
            mode="markers",
            marker=dict(
                size=9,
                color=temps,
                colorscale=[
                    [0.0, "#5aa9ff"],
                    [0.25, "#6ee7d8"],
                    [0.5, "#fbbf24"],
                    [0.75, "#fb923c"],
                    [1.0, "#ff5f7e"],
                ],
                cmin=low,
                cmax=high,
                colorbar=dict(
                    title=dict(text=unit, font=dict(size=11, color=palette["colorbar"])),
                    thickness=9,
                    len=0.55,
                    outlinewidth=0,
                    tickfont=dict(size=10, color=palette["colorbar"]),
                ),
                line=dict(color="rgba(255,255,255,0.55)", width=0.8),
            ),
            text=[city.name_zh if lang == "zh" else city.name_en for city in shown],
            customdata=[
                [
                    condition_label(overview[city.slug]["condition"], lang),
                    temp_text(overview[city.slug]["high"], unit),
                    temp_text(overview[city.slug]["low"], unit),
                    overview[city.slug]["humidity"],
                ]
                for city in shown
            ],
            hovertemplate=(
                "<b>%{text}</b><br>%{customdata[0]}<br>"
                f"{t('chart_now', lang)} %{{marker.color:.0f}}" + unit + "<br>"
                f"{t('chart_high', lang)} %{{customdata[1]}} / {t('chart_low', lang)} %{{customdata[2]}} · 💧 %{{customdata[3]}}%<extra></extra>"
            ),
        )
    )

    if selected:
        weather = overview[selected.slug]
        fig.add_trace(
            go.Scattergeo(
                lon=[selected.lon],
                lat=[selected.lat],
                mode="markers+text",
                marker=dict(
                    size=19,
                    color="#ffffff",
                    symbol="star",
                    line=dict(color=palette["selected_line"], width=2),
                ),
                text=[selected.name_zh if lang == "zh" else selected.name_en],
                textposition="top center",
                textfont=dict(color=palette["selected_text"], size=13),
                hovertext=f"{selected.name_zh if lang == 'zh' else selected.name_en} · {temp_text(weather['temp'], unit)}",
                hoverinfo="text",
                showlegend=False,
            )
        )

    fig.update_geos(
        projection=dict(type="mercator"),
        lonaxis=dict(range=[72, 140], showgrid=False),
        lataxis=dict(range=[15, 55], showgrid=False),
        showland=True,
        landcolor=palette["land"],
        showocean=True,
        oceancolor=palette["ocean"],
        showlakes=True,
        lakecolor=palette["lake"],
        showcountries=True,
        countrycolor=palette["country"],
        showcoastlines=True,
        coastlinecolor=palette["coastline"],
        showframe=False,
        bgcolor="rgba(0,0,0,0)",
    )
    fig.update_layout(
        height=520,
        margin=dict(l=0, r=0, t=6, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=palette["text"], size=11),
        hoverlabel=dict(
            bgcolor=palette["hover_bg"],
            bordercolor=palette["hover_border"],
            font=dict(color=palette["hover_text"], size=12),
        ),
    )
    return fig


# ---------------------------------------------------------------------------
# Sun and air quality
# ---------------------------------------------------------------------------


def sun_air_html(detail: dict, unit: str, lang: str = "en") -> str:
    daily = detail["daily"]
    air = detail.get("air")
    condition = condition_label(detail["current"]["condition"], lang)
    if lang != "zh":
        condition = condition.lower()

    if daily["sunrise"] and daily["sunset"]:
        try:
            sunrise = datetime.fromisoformat(daily["sunrise"][0])
            sunset = datetime.fromisoformat(daily["sunset"][0])
            now = datetime.fromisoformat(detail["time"])
            total = max(1.0, (sunset - sunrise).total_seconds())
            progress = (now - sunrise).total_seconds() / total * 100
            progress = max(0.0, min(100.0, progress))
            daylight = total / 3600
        except (ValueError, TypeError):
            sunrise = sunset = None
            progress = 0
            daylight = 0
    else:
        sunrise = sunset = None
        progress = 0
        daylight = 0

    sun_html = f"""<div class="info-card">
      <h3>{t('sun_title', lang)}</h3>
      <div class="sub">{t('sun_sub', lang, condition=_safe(condition))}</div>
      <div class="sun-row">
        <div class="sun-item"><span class="k">{t('sunrise', lang)}</span><span class="v">{sunrise.strftime('%H:%M') if sunrise else '—'}</span></div>
        <div class="sun-item" style="text-align:right"><span class="k">{t('sunset', lang)}</span><span class="v">{sunset.strftime('%H:%M') if sunset else '—'}</span></div>
      </div>
      <div class="sun-track"><div class="sun-dot" style="left:{progress:.1f}%"></div></div>
      <div class="sun-row" style="margin-top:8px">
        <div class="sun-item"><span class="k">{t('daylight', lang)}</span><span class="v">{t('daylight_value', lang, hours=daylight)}</span></div>
        <div class="sun-item" style="text-align:right"><span class="k">{t('uv_peak', lang)}</span><span class="v">{daily['uv'][0] if daily['uv'] else 0:.1f}</span></div>
      </div>
    </div>"""

    if air:
        aqi = air.get("european_aqi", 0)
        label, color = aqi_info(aqi, lang)
        pollutants = [
            ("PM2.5", air.get("pm2_5", 0), 150, "#6ee7ff"),
            ("PM10", air.get("pm10", 0), 250, "#8fa8ff"),
            ("O₃", air.get("ozone", 0), 180, "#ffd06b"),
            ("NO₂", air.get("no2", 0), 200, "#ff9e7a"),
        ]
        rows = "".join(
            f'<div class="pollutant"><div class="p-row"><span>{name}</span><b>{value:.0f} µg/m³</b></div>'
            f'<div class="p-bar"><span style="width:{min(100, value / limit * 100):.0f}%;background:{bar_color};"></span></div></div>'
            for name, value, limit, bar_color in pollutants
        )
        air_html = f"""<div class="info-card">
          <h3>{t('air_title', lang)}</h3>
          <div class="sub">{t('air_sub', lang)}</div>
          <div class="aqi-head">
            <div class="aqi-value" style="color:{color}">{aqi}</div>
            <div class="aqi-tag" style="color:{color}">{label}</div>
          </div>
          <div class="sub" style="margin-top:6px">{t('air_us', lang, aqi=air.get('us_aqi', '—'), time=air.get('time', '')[11:16])}</div>
          {rows}
        </div>"""
    else:
        air_html = f"""<div class="info-card">
          <h3>{t('air_title', lang)}</h3>
          <div class="sub">{t('air_unavailable', lang)}</div>
          <div class="aqi-head"><div class="aqi-value" style="color:#96a2c8">—</div></div>
          <div class="sub" style="margin-top:10px">{t('air_still_live', lang)}</div>
        </div>"""

    return f'<div class="duo">{sun_html}{air_html}</div>'


def footer_html(source: str, updated: str, lang: str = "en") -> str:
    mode = t("footer_demo" if source == "demo" else "footer_live", lang)
    return f"""
<div class="app-footer">
  <span>{t('footer_line', lang, mode=mode, updated=_safe(updated))}</span>
  <span>{t('footer_built', lang)}</span>
</div>"""
