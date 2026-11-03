"""HTML fragments and Plotly charts used by the dashboard."""

from __future__ import annotations

import html
import math
from datetime import datetime
from typing import Iterable, Sequence

import plotly.graph_objects as go

from .cities import City, weather_code_info

UNIT_LABEL = {"°C": "°C", "°F": "°F"}


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


def wind_direction_name(degrees: float | int) -> str:
    names = [
        "N",
        "NNE",
        "NE",
        "ENE",
        "E",
        "ESE",
        "SE",
        "SSE",
        "S",
        "SSW",
        "SW",
        "WSW",
        "W",
        "WNW",
        "NW",
        "NNW",
    ]
    return names[int((float(degrees) % 360) / 22.5 + 0.5) % 16]


def aqi_info(aqi: int) -> tuple[str, str]:
    if aqi <= 20:
        return "Good", "#6ee7b7"
    if aqi <= 40:
        return "Fair", "#a3e635"
    if aqi <= 60:
        return "Moderate", "#fbbf24"
    if aqi <= 80:
        return "Poor", "#fb923c"
    if aqi <= 100:
        return "Very poor", "#f87171"
    return "Extremely poor", "#c084fc"


def uv_info(uv: float) -> tuple[str, str]:
    if uv < 3:
        return "Low", "#6ee7b7"
    if uv < 6:
        return "Moderate", "#fbbf24"
    if uv < 8:
        return "High", "#fb923c"
    if uv < 11:
        return "Very high", "#f87171"
    return "Extreme", "#c084fc"


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


def hero_html(now: datetime, live: bool, city_count: int) -> str:
    status = (
        '<span class="pill"><span class="live-dot"></span> Live data</span>'
        if live
        else '<span class="pill"><span class="demo-dot"></span> Demo data</span>'
    )
    return f"""
<div class="hero">
  <div class="hero-kicker"><span class="dot"></span> China Weather Atlas · 中国城市天气</div>
  <h1>Weather across <span class="grad">China</span>,<br/>city by city.</h1>
  <p class="hero-sub">
    A living forecast for {city_count} major cities — from Harbin's frost to Sanya's
    tropical breeze. Click any city card to open its current conditions, next 24 hours,
    7-day outlook, air quality and map.
  </p>
  <div class="hero-meta">
    <span class="pill">🗓️ <strong>{_safe(now.strftime("%A, %B %d, %Y"))}</strong></span>
    <span class="pill">🕘 <strong>{_safe(now.strftime("%H:%M"))}</strong> China Standard Time</span>
    {status}
    <span class="pill">📍 <strong>{city_count}</strong> cities tracked</span>
  </div>
</div>
"""


def stats_html(overview: dict[str, dict], by_slug: dict[str, City], unit: str) -> str:
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
        return city.name_en if city else slug

    items = [
        ("🔥", "Hottest right now", f"{city_name(hottest_slug)} · {temp_text(hottest['temp'], unit)}", f"Feels like {temp_text(hottest['feels'], unit)}"),
        ("🧊", "Coldest right now", f"{city_name(coldest_slug)} · {temp_text(coldest['temp'], unit)}", f"Low tonight {temp_text(coldest['low'], unit)}"),
        ("🌧️", "Highest rain chance", f"{city_name(wettest_slug)} · {wettest['rain_chance']}%", f"Today's maximum probability"),
        ("🛰️", "Live coverage", f"{len(overview)} cities", "Open-Meteo · refreshed every 10 min"),
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
    t = max(0.0, min(1.0, (value - low) / span))
    stops = [(0.0, (90, 169, 255)), (0.45, (110, 231, 216)), (0.7, (251, 191, 36)), (1.0, (255, 95, 126))]
    for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
        if t <= p1:
            f = (t - p0) / (p1 - p0)
            rgb = tuple(round(a + (b - a) * f) for a, b in zip(c0, c1))
            return f"rgb{rgb}"
    return "rgb(255, 95, 126)"


def extremes_html(cities: Sequence[City], overview: dict[str, dict], unit: str) -> str:
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
        return (
            f'<div class="ladder-row"><span class="ladder-rank">{rank:02d}</span>'
            f'<span class="ladder-name">{_safe(city.name_zh)}'
            f'<small>{_safe(city.name_en)} · {_safe(info.get("emoji", ""))}</small></span>'
            f'<span class="ladder-val" style="color:{color}">{temp_text(temp, unit)}</span>'
            f'<span class="ladder-bar"><i style="width:{width:.0f}%;background:{color}"></i></span>'
            "</div>"
        )

    warm_rows = "".join(row(city) for city in warm)
    cold_rows = "".join(row(city) for city in cold)
    return (
        '<div class="map-side">'
        '<div class="map-side-head"><h3>Temperature ladder</h3>'
        f'<p>Warmest and coldest of the {len(shown)} cities shown.</p></div>'
        f'<div class="ladder-label"><span>🔥 Warmest</span><span>{temp_text(high, unit)}</span></div>'
        f'{warm_rows}'
        f'<div class="ladder-label cold"><span>🧊 Coldest</span><span>{temp_text(low, unit)}</span></div>'
        f'{cold_rows}'
        '<div class="map-side-foot">Click any city card above for its full forecast.</div>'
        "</div>"
    )


def city_card_css(overview: dict[str, dict], cities: Sequence[City]) -> str:
    """Per-city gradients generated from live temperature and condition."""

    palettes = {
        "clear": ("rgba(255, 184, 107, 0.20)", "rgba(255, 122, 138, 0.07)", "rgba(255, 184, 107, 0.42)"),
        "cloudy": ("rgba(124, 155, 255, 0.20)", "rgba(110, 231, 216, 0.06)", "rgba(124, 155, 255, 0.42)"),
        "rain": ("rgba(96, 165, 250, 0.22)", "rgba(110, 231, 216, 0.07)", "rgba(96, 165, 250, 0.48)"),
        "storm": ("rgba(167, 139, 250, 0.24)", "rgba(96, 165, 250, 0.08)", "rgba(167, 139, 250, 0.5)"),
        "snow": ("rgba(186, 230, 253, 0.20)", "rgba(124, 155, 255, 0.07)", "rgba(186, 230, 253, 0.44)"),
        "fog": ("rgba(148, 163, 184, 0.18)", "rgba(124, 155, 255, 0.06)", "rgba(148, 163, 184, 0.38)"),
    }
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
    linear-gradient(152deg, rgba(26, 34, 66, 0.94), rgba(11, 16, 35, 0.9));
  border-color: rgba(148, 163, 255, 0.18);
}}
.st-key-city_{city.slug} button:hover {{
  border-color: {border};
  box-shadow: 0 16px 40px rgba(5, 9, 24, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.08);
}}"""
        )
    return "<style>" + "".join(rules) + "</style>"


def city_labels(city: City, weather: dict, unit: str) -> tuple[str, str]:
    info = weather.get("condition") or weather_code_info(weather.get("code", 0), True)
    label = (
        f"{info['emoji']} {city.name_zh}  \n"
        f"{temp_text(weather['temp'], unit)} · {info['label_zh']}"
    )
    foot = (
        f"<div class='city-foot'><span>{_safe(city.name_en)}</span>"
        f"<span>{temp_text(weather['high'], unit)} / {temp_text(weather['low'], unit)}"
        f" · 💧 {weather['humidity']}%</span></div>"
    )
    return label, foot


# ---------------------------------------------------------------------------
# Detail header and alerts
# ---------------------------------------------------------------------------


def detail_hero_html(city: City, detail: dict, unit: str) -> str:
    current = detail["current"]
    info = current["condition"]
    updated = current.get("time", "")[11:16]
    return f"""
<div class="detail-hero" style="--glow: {_kind_glow(info['kind'])};">
  <div>
    <div class="crumb">{_safe(city.region)} China · {_safe(city.province)}</div>
    <h1>{_safe(city.name_zh)}<span>{_safe(city.name_en)}</span></h1>
    <div class="detail-cond">
      <span>{info['emoji']}</span>
      <span class="zh">{_safe(info['label_zh'])}</span>
      <span class="en">{_safe(info['label_en'])}</span>
    </div>
    <div class="detail-chips">
      <span class="chip">Feels like <b>{temp_text(current['feels'], unit)}</b></span>
      <span class="chip">H <b>{temp_text(current['high'], unit)}</b> / L <b>{temp_text(current['low'], unit)}</b></span>
      <span class="chip">💧 <b>{current['humidity']}%</b> humidity</span>
      <span class="chip">💨 <b>{current['wind']:.0f} km/h</b> {_safe(wind_direction_name(current['wind_dir']))}</span>
      <span class="chip">🌧️ <b>{current['rain_chance']}%</b> rain</span>
    </div>
  </div>
  <div class="now-panel">
    <div class="now-emoji">{info['emoji']}</div>
    <div class="temp-now">{temp_text(current['temp'], unit)}<sup>{unit}</sup></div>
    <div class="updated">Updated {_safe(updated)} CST · {_safe(weather_code_info(current['code'], True)['label_en'])}</div>
  </div>
</div>
"""


def alerts_html(city: City, detail: dict, unit: str) -> str:
    current = detail["current"]
    daily = detail["daily"]
    air = detail.get("air") or {}
    alerts: list[tuple[str, str, str, str]] = []

    high = daily["high"][0] if daily["high"] else current["high"]
    low = daily["low"][0] if daily["low"] else current["low"]
    rain = daily["rain_chance"][0] if daily["rain_chance"] else current["rain_chance"]
    wind = daily["wind_max"][0] if daily["wind_max"] else current["wind"]

    if current["condition"]["kind"] == "storm":
        alerts.append(("danger", "⛈️", "Thunderstorms in the area", "Lightning and heavy showers are possible. Keep an eye on local alerts before heading out."))
    if high >= 35:
        alerts.append(("danger", "🥵", "Heat advisory", f"Today's high reaches {temp_text(high, unit)}. Hydrate often and avoid the midday sun."))
    elif high >= 32:
        alerts.append(("info", "☀️", "A hot one", f"Today's high is {temp_text(high, unit)}. Plan outdoor time for the morning or evening."))
    if low <= -5:
        alerts.append(("info", "🧣", "Bundle up", f"Tonight drops to {temp_text(low, unit)}. Wind chill will make it feel colder."))
    if rain >= 60:
        alerts.append(("info", "☔", "Rain likely", f"{rain}% chance of precipitation today — an umbrella is a good idea."))
    if wind >= 40:
        alerts.append(("info", "💨", "Windy conditions", f"Gusts up to {wind:.0f} km/h are forecast. Secure loose items outdoors."))
    aqi = air.get("european_aqi", 0)
    if aqi >= 80:
        label, _ = aqi_info(aqi)
        alerts.append(("danger", "😷", f"Air quality: {label}", f"European AQI is {aqi}. Consider reducing strenuous outdoor activity."))

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


def metrics_html(detail: dict, unit: str) -> str:
    current = detail["current"]
    daily = detail["daily"]
    air = detail.get("air") or {}
    uv = current.get("uv", 0)
    uv_label, uv_color = uv_info(uv)
    aqi = air.get("european_aqi")
    aqi_label, aqi_color = aqi_info(aqi) if aqi is not None else ("—", "#96a2c8")
    rain = current.get("rain_chance", 0)
    visibility = current.get("visibility", 0)

    items = [
        _metric("🌡️", "Feels like", f"{temp_text(current['feels'], unit)}<small>{unit}</small>", f"Actual {temp_text(current['temp'], unit)}", None),
        _metric("💧", "Humidity", f"{current['humidity']}%", "Relative humidity", current["humidity"]),
        _metric("💨", "Wind", f"{current['wind']:.0f}<small> km/h</small>", f"From {wind_direction_name(current['wind_dir'])} · {current['wind_dir']}°", min(100, current["wind"] * 2.2)),
        _metric("🧭", "Pressure", f"{current['pressure']:.0f}<small> hPa</small>", "Surface pressure", (current["pressure"] - 980) / 60 * 100),
        _metric("👁️", "Visibility", f"{visibility:.0f}<small> km</small>", "Horizontal visibility", min(100, visibility / 25 * 100)),
        _metric("🕶️", "UV index", f"{uv:.1f}", f"{uv_label} exposure", min(100, uv / 11 * 100), uv_color),
        _metric("☔", "Rain chance", f"{rain}%", "Maximum today", rain),
        _metric("🍃", "Air quality", f"{aqi if aqi is not None else '—'}<small> EAQI</small>", aqi_label, min(100, (aqi or 0) / 160 * 100), aqi_color),
    ]
    return f'<div class="metrics">{"".join(items)}</div>'


# ---------------------------------------------------------------------------
# 7-day forecast
# ---------------------------------------------------------------------------


def daily_html(detail: dict, unit: str) -> str:
    daily = detail["daily"]
    if not daily["time"]:
        return "<p>No daily forecast available.</p>"

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
        name = "Today" if index == 0 else (day.strftime("%a") if day else date_text)
        date_label = day.strftime("%b %d") if day else ""
        rain = daily["rain_chance"][index]
        cards.append(
            f"""
        <div class="day-card{' today' if index == 0 else ''}">
          <div class="day-name">{_safe(name)}</div>
          <div class="day-date">{_safe(date_label)}</div>
          <div class="day-icon">{info['day_emoji']}</div>
          <div class="day-cond" title="{_safe(info['label_en'])}">{_safe(info['label_en'])}</div>
          <div class="day-temps">{temp_text(high, unit)} <span class="lo">/ {temp_text(low, unit)}</span></div>
          <div class="day-range"><span style="left:{left:.0f}%;width:{width:.0f}%"></span></div>
          <div class="day-rain">💧 {rain}%</div>
        </div>"""
        )
    return f'<div class="forecast-strip">{"".join(cards)}</div>'


# ---------------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------------


def _base_layout(height: int = 370) -> dict:
    return dict(
        height=height,
        margin=dict(l=12, r=12, t=22, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, -apple-system, Segoe UI, sans-serif", color="#aab5d8", size=12),
        hoverlabel=dict(
            bgcolor="#111832",
            bordercolor="rgba(148,163,255,0.25)",
            font=dict(color="#eef2ff", size=12),
        ),
        hovermode="x unified",
        showlegend=False,
    )


def hourly_chart(detail: dict, unit: str = "°C") -> go.Figure:
    hourly = detail["hourly"]
    times = [datetime.fromisoformat(t) for t in hourly["time"]]
    temps = hourly["temp"]
    rain = hourly["rain_chance"]
    feels = hourly["feels"]
    humidity = hourly["humidity"]
    wind = hourly["wind"]
    precip = hourly["precip"]
    is_day = hourly["is_day"]

    fig = go.Figure()

    # Shade night-time stretches.
    night_start = None
    for index, daylight in enumerate(is_day):
        if not daylight and night_start is None:
            night_start = index
        if daylight and night_start is not None:
            fig.add_vrect(x0=times[night_start], x1=times[index], fillcolor="rgba(8, 12, 30, 0.42)", line_width=0, layer="below")
            night_start = None
    if night_start is not None:
        fig.add_vrect(x0=times[night_start], x1=times[-1], fillcolor="rgba(8, 12, 30, 0.42)", line_width=0, layer="below")

    fig.add_trace(
        go.Bar(
            x=times,
            y=rain,
            name="Rain chance",
            marker=dict(color="rgba(110, 231, 216, 0.20)", line=dict(width=0)),
            yaxis="y2",
            hovertemplate="Rain chance %{y}%<extra></extra>",
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
            name="Temperature",
            line=dict(color="#8fa8ff", width=3, shape="spline"),
            marker=dict(size=4, color="#c9d6ff", line=dict(color="#8fa8ff", width=1)),
            fill="tonexty",
            fillcolor="rgba(124, 155, 255, 0.13)",
            customdata=list(zip(feels_converted, humidity, wind, precip)),
            hovertemplate=(
                f"<b>%{{x|%H:%M}}</b><br>Temperature %{{y:.0f}}{unit}<br>"
                f"Feels like %{{customdata[0]:.0f}}{unit}<br>"
                "Humidity %{customdata[1]}%<br>"
                "Wind %{customdata[2]:.0f} km/h<br>"
                "Rain %{customdata[3]:.1f} mm<extra></extra>"
            ),
        )
    )
    # Current-hour marker.
    fig.add_trace(
        go.Scatter(
            x=[times[0]],
            y=[converted[0]],
            mode="markers",
            marker=dict(size=12, color="#6ee7d8", line=dict(color="#0a1024", width=3)),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    layout = _base_layout(380)
    layout.update(
        yaxis=dict(
            title=dict(text=f"Temperature ({unit})", font=dict(size=11, color="#6c789e")),
            gridcolor="rgba(148,163,255,0.09)",
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
            gridcolor="rgba(148,163,255,0.05)",
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
) -> go.Figure:
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
                    title=dict(text=unit, font=dict(size=11, color="#96a2c8")),
                    thickness=9,
                    len=0.55,
                    outlinewidth=0,
                    tickfont=dict(size=10, color="#96a2c8"),
                ),
                line=dict(color="rgba(255,255,255,0.55)", width=0.8),
            ),
            text=[city.name_en for city in shown],
            customdata=[
                [
                    overview[city.slug]["condition"]["label_en"],
                    temp_text(overview[city.slug]["high"], unit),
                    temp_text(overview[city.slug]["low"], unit),
                    overview[city.slug]["humidity"],
                ]
                for city in shown
            ],
            hovertemplate=(
                "<b>%{text}</b><br>%{customdata[0]}<br>"
                "Now %{marker.color:.0f}" + unit + "<br>"
                "H %{customdata[1]} / L %{customdata[2]} · 💧 %{customdata[3]}%<extra></extra>"
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
                    line=dict(color="#ffd06b", width=2),
                ),
                text=[selected.name_zh],
                textposition="top center",
                textfont=dict(color="#ffffff", size=13),
                hovertext=f"{selected.name_en} · {temp_text(weather['temp'], unit)}",
                hoverinfo="text",
                showlegend=False,
            )
        )

    fig.update_geos(
        projection=dict(type="mercator"),
        lonaxis=dict(range=[72, 140], showgrid=False),
        lataxis=dict(range=[15, 55], showgrid=False),
        showland=True,
        landcolor="#141b36",
        showocean=True,
        oceancolor="#080d1d",
        showlakes=True,
        lakecolor="#0b1226",
        showcountries=True,
        countrycolor="rgba(148,163,255,0.22)",
        showcoastlines=True,
        coastlinecolor="rgba(148,163,255,0.25)",
        showframe=False,
        bgcolor="rgba(0,0,0,0)",
    )
    fig.update_layout(
        height=520,
        margin=dict(l=0, r=0, t=6, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#aab5d8", size=11),
        hoverlabel=dict(
            bgcolor="#111832",
            bordercolor="rgba(148,163,255,0.25)",
            font=dict(color="#eef2ff", size=12),
        ),
    )
    return fig


# ---------------------------------------------------------------------------
# Sun and air quality
# ---------------------------------------------------------------------------


def sun_air_html(detail: dict, unit: str) -> str:
    daily = detail["daily"]
    air = detail.get("air")

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
      <h3>🌅 Sun & daylight</h3>
      <div class="sub">Today's solar window in {_safe(detail['current']['condition']['label_en'].lower())} skies</div>
      <div class="sun-row">
        <div class="sun-item"><span class="k">Sunrise</span><span class="v">{sunrise.strftime('%H:%M') if sunrise else '—'}</span></div>
        <div class="sun-item" style="text-align:right"><span class="k">Sunset</span><span class="v">{sunset.strftime('%H:%M') if sunset else '—'}</span></div>
      </div>
      <div class="sun-track"><div class="sun-dot" style="left:{progress:.1f}%"></div></div>
      <div class="sun-row" style="margin-top:8px">
        <div class="sun-item"><span class="k">Daylight</span><span class="v">{daylight:.1f} hours</span></div>
        <div class="sun-item" style="text-align:right"><span class="k">UV peak</span><span class="v">{daily['uv'][0] if daily['uv'] else 0:.1f}</span></div>
      </div>
    </div>"""

    if air:
        aqi = air.get("european_aqi", 0)
        label, color = aqi_info(aqi)
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
          <h3>🍃 Air quality</h3>
          <div class="sub">European AQI · updated hourly</div>
          <div class="aqi-head">
            <div class="aqi-value" style="color:{color}">{aqi}</div>
            <div class="aqi-tag" style="color:{color}">{label}</div>
          </div>
          <div class="sub" style="margin-top:6px">US AQI {air.get('us_aqi', '—')} · {air.get('time', '')[11:16]} CST</div>
          {rows}
        </div>"""
    else:
        air_html = """<div class="info-card">
          <h3>🍃 Air quality</h3>
          <div class="sub">Air quality data is unavailable right now.</div>
          <div class="aqi-head"><div class="aqi-value" style="color:#96a2c8">—</div></div>
          <div class="sub" style="margin-top:10px">The forecast above is still live.</div>
        </div>"""

    return f'<div class="duo">{sun_html}{air_html}</div>'


def footer_html(source: str, updated: str) -> str:
    mode = "Demo data" if source == "demo" else "Live Open-Meteo data"
    return f"""
<div class="app-footer">
  <span>Data: <b>{mode}</b> · Updated {_safe(updated)} CST · Cached for 10 minutes</span>
  <span>Built with <b>Streamlit</b> + <b>Plotly</b> · 中国城市天气</span>
</div>"""
