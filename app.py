"""China City Weather — a Streamlit dashboard for major Chinese cities."""

from __future__ import annotations

import random
from datetime import datetime
from typing import Sequence
from zoneinfo import ZoneInfo

import streamlit as st

from weather_dashboard import (
    CITIES,
    CITY_BY_SLUG,
    REGIONS,
    City,
    WeatherError,
    demo_detail,
    demo_overview,
    fetch_detail,
    fetch_overview,
)
from weather_dashboard.components import (
    alerts_html,
    city_card_css,
    city_labels,
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
)
from weather_dashboard.styles import CSS

TIMEZONE = ZoneInfo("Asia/Shanghai")
PLOT_CONFIG = {
    "displayModeBar": False,
    "scrollZoom": False,
    "responsive": True,
}


# ---------------------------------------------------------------------------
# Data loading (cached for ten minutes)
# ---------------------------------------------------------------------------


@st.cache_data(ttl=600, show_spinner=False)
def load_overview(slugs: tuple[str, ...]) -> tuple[dict[str, dict], str | None]:
    cities = [CITY_BY_SLUG[slug] for slug in slugs]
    try:
        return fetch_overview(cities), None
    except WeatherError as exc:
        return demo_overview(cities), str(exc)


@st.cache_data(ttl=600, show_spinner=False)
def load_detail(slug: str) -> tuple[dict, str | None]:
    city = CITY_BY_SLUG[slug]
    try:
        return fetch_detail(city), None
    except WeatherError as exc:
        return demo_detail(city), str(exc)


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------


def now_china() -> datetime:
    return datetime.now(TIMEZONE)


def selected_city_from_query() -> City | None:
    raw = st.query_params.get("city")
    if isinstance(raw, (list, tuple)):
        raw = raw[0] if raw else None
    if not raw:
        return None
    return CITY_BY_SLUG.get(str(raw).strip().lower())


def open_city(slug: str) -> None:
    st.query_params["city"] = slug
    st.rerun()


def matches_query(city: City, query: str) -> bool:
    query = (query or "").strip().lower()
    if not query:
        return True
    haystack = " ".join(
        [city.name_zh, city.name_en, city.province, city.region, city.slug]
    ).lower()
    return all(part in haystack for part in query.split())


def filtered_cities(query: str, regions: list[str]) -> list[City]:
    result = []
    for city in CITIES:
        if regions and city.region not in regions:
            continue
        if not matches_query(city, query):
            continue
        result.append(city)
    return result


def render_map_section(
    cities: Sequence[City],
    overview: dict[str, dict],
    unit: str,
    selected_slug: str = "",
) -> None:
    """Show the weather map beside the warmest/coldest ladder."""

    map_column, side_column = st.columns([2.15, 1], gap="medium")
    with map_column:
        st.plotly_chart(
            map_chart(cities, overview, selected_slug, unit),
            width="stretch",
            theme=None,
            config=PLOT_CONFIG,
        )
    with side_column:
        st.markdown(extremes_html(cities, overview, unit), unsafe_allow_html=True)


def source_alert(error: str | None) -> None:
    if not error:
        return
    st.markdown(
        """
        <div class="alert info">
          <span class="a-icon">🛰️</span>
          <div><b>Showing demo weather.</b> Live Open-Meteo data could not be reached,
          so this page is using a realistic offline fallback. Try refreshing in a moment.</div>
        </div>""",
        unsafe_allow_html=True,
    )
    with st.expander("Technical details"):
        st.code(error)


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------


def render_sidebar(
    overview: dict[str, dict],
    error: str | None,
    unit: str,
) -> tuple[str, str, list[str]]:
    with st.sidebar:
        st.markdown(
            """
            <div class="side-brand">
              <div class="side-logo">🌤️</div>
              <div class="side-title">China Weather<span>Atlas · 中国城市天气</span></div>
            </div>
            <div class="side-copy">Current conditions and forecasts for major cities,
            from the northeast frontier to the tropical south.</div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="side-label">Temperature unit</div>', unsafe_allow_html=True)
        picked_unit = st.segmented_control(
            "Temperature unit",
            options=["°C", "°F"],
            default=unit,
            required=True,
            key="unit",
            label_visibility="collapsed",
        )
        unit = picked_unit or "°C"

        st.markdown('<div class="side-label">Search cities</div>', unsafe_allow_html=True)
        query = st.text_input(
            "Search cities",
            placeholder="Beijing, 上海, Chengdu…",
            label_visibility="collapsed",
        )

        st.markdown('<div class="side-label">Regions</div>', unsafe_allow_html=True)
        regions = st.multiselect(
            "Regions",
            options=list(REGIONS),
            default=[],
            placeholder="All regions",
            label_visibility="collapsed",
        )

        status_class = "live" if not error else "demo"
        status_text = "Live · Open-Meteo" if not error else "Demo fallback"
        updated = next(iter(overview.values()), {}).get("time", "")[11:16] if overview else "—"
        st.markdown(
            f"""
            <div class="side-status">
              <div class="row"><span>Source</span><b class="{status_class}">{status_text}</b></div>
              <div class="row"><span>Cities</span><b>{len(overview)}</b></div>
              <div class="row"><span>Updated</span><b>{updated or '—'} CST</b></div>
              <div class="row"><span>Cache</span><b>10 minutes</b></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("↻ Refresh live data", width="stretch"):
            st.cache_data.clear()
            st.rerun()

        if st.button("🎲 Surprise me", width="stretch"):
            open_city(random.choice(CITIES).slug)

        st.markdown(
            """
            <div class="side-foot">
              Powered by <a href="https://open-meteo.com/" target="_blank">Open-Meteo</a>.
              Forecasts cover the next 24 hours and 7 days.
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.expander("About this dashboard"):
            st.markdown(
                """
                **35 major cities**, one dashboard.

                - Click any city card to open its detailed forecast
                - Temperature units can be switched here at any time
                - Data refreshes every 10 minutes, with an offline demo fallback
                - Air quality comes from the Open-Meteo Air Quality API
                """
            )

    return unit, query, regions


# ---------------------------------------------------------------------------
# Overview page
# ---------------------------------------------------------------------------


def render_overview(overview: dict[str, dict], error: str | None, unit: str) -> None:
    now = now_china()
    st.markdown(hero_html(now, error is None, len(CITIES)), unsafe_allow_html=True)
    source_alert(error)
    st.markdown(stats_html(overview, CITY_BY_SLUG, unit), unsafe_allow_html=True)

    section = f"""
    <div class="section-head">
      <div>
        <h2>Major cities · 主要城市</h2>
        <p>Click a city card to open its current conditions and forecast.</p>
      </div>
      <span class="section-note">{len(CITIES)} cities · {now.strftime('%H:%M')} CST</span>
    </div>"""
    st.markdown(section, unsafe_allow_html=True)

    st.markdown(city_card_css(overview, CITIES), unsafe_allow_html=True)
    st.markdown(
        """
        <style>
        .st-key-city_grid [data-testid="stHorizontalBlock"] { row-gap: 0.15rem; }
        </style>""",
        unsafe_allow_html=True,
    )

    with st.container(key="city_grid"):
        columns = st.columns(4, gap="small")
        for index, city in enumerate(CITIES):
            weather = overview.get(city.slug)
            if not weather:
                continue
            label, foot = city_labels(city, weather, unit)
            with columns[index % 4]:
                if st.button(
                    label,
                    key=f"city_{city.slug}",
                    width="stretch",
                    help=f"Open the {city.name_en} forecast",
                ):
                    open_city(city.slug)
                st.markdown(foot, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="section-head">
          <div>
            <h2>Weather map · 天气地图</h2>
            <p>Marker colour shows current temperature. Hover a city for today's range.</p>
          </div>
          <span class="section-note">Open-Meteo · Asia/Shanghai</span>
        </div>""",
        unsafe_allow_html=True,
    )
    render_map_section(CITIES, overview, unit)
    updated = next(iter(overview.values()), {}).get("time", "")[11:16]
    st.markdown(footer_html("demo" if error else "live", updated or now.strftime("%H:%M")), unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Detail page
# ---------------------------------------------------------------------------


def render_detail(city: City, overview: dict[str, dict], unit: str) -> None:
    detail, error = load_detail(city.slug)
    now = now_china()

    if st.button("← All cities", key="back_btn"):
        st.query_params.clear()
        st.rerun()

    st.markdown(detail_hero_html(city, detail, unit), unsafe_allow_html=True)
    source_alert(error)
    st.markdown(alerts_html(city, detail, unit), unsafe_allow_html=True)
    st.markdown(metrics_html(detail, unit), unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="section-head">
          <div>
            <h2>7-day forecast · 未来七天</h2>
            <p>Daily highs, lows and rain probability for {city.name_zh}.</p>
          </div>
          <span class="section-note">Updated {detail['time'][11:16]} CST</span>
        </div>""",
        unsafe_allow_html=True,
    )
    st.markdown(daily_html(detail, unit), unsafe_allow_html=True)

    tab_hourly, tab_map, tab_sun = st.tabs(
        ["📈 Next 24 hours", "🗺️ Weather map", "🌅 Sun & air"]
    )

    with tab_hourly:
        st.markdown(
            """
            <div class="section-head">
              <div>
                <h2>Rolling 24-hour forecast</h2>
                <p>Temperature and rain probability. Shaded bands mark night-time.</p>
              </div>
            </div>""",
            unsafe_allow_html=True,
        )
        st.plotly_chart(
            hourly_chart(detail, unit),
            width="stretch",
            theme=None,
            config=PLOT_CONFIG,
        )
        st.caption(
            "Hover the chart for feels-like temperature, humidity, wind and rainfall. "
            "The teal dot marks the current hour."
        )

    with tab_map:
        st.markdown(
            f"""
            <div class="section-head">
              <div>
                <h2>{city.name_en} on the map</h2>
                <p>The gold star marks {city.name_zh}; every city is coloured by current temperature.</p>
              </div>
            </div>""",
            unsafe_allow_html=True,
        )
        render_map_section(CITIES, overview, unit, city.slug)

    with tab_sun:
        st.markdown(
            """
            <div class="section-head">
              <div>
                <h2>Sunlight and air</h2>
                <p>Today's daylight window plus the latest air-quality reading.</p>
              </div>
            </div>""",
            unsafe_allow_html=True,
        )
        st.markdown(sun_air_html(detail, unit), unsafe_allow_html=True)
        st.caption("Air quality is fetched separately and may lag the weather forecast by up to an hour.")

    st.markdown(
        footer_html("demo" if error else "live", detail["time"][11:16] or now.strftime("%H:%M")),
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    st.set_page_config(
        page_title="China Weather Atlas · 中国城市天气",
        page_icon="🌤️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(CSS, unsafe_allow_html=True)

    # The overview powers both the sidebar status and the city map.
    overview, overview_error = load_overview(tuple(city.slug for city in CITIES))
    unit, query, regions = render_sidebar(overview, overview_error, "°C")

    selected = selected_city_from_query()
    if selected:
        render_detail(selected, overview, unit)
    else:
        visible = filtered_cities(query, regions)
        if not query and (not regions or set(regions) == set(REGIONS)):
            render_overview(overview, overview_error, unit)
        else:
            # Reuse the overview layout with the current filter applied.
            render_filtered_overview(overview, overview_error, unit, visible, query, regions)


def render_filtered_overview(
    overview: dict[str, dict],
    error: str | None,
    unit: str,
    visible: list[City],
    query: str,
    regions: list[str],
) -> None:
    now = now_china()
    st.markdown(hero_html(now, error is None, len(CITIES)), unsafe_allow_html=True)
    source_alert(error)
    st.markdown(stats_html(overview, CITY_BY_SLUG, unit), unsafe_allow_html=True)

    filter_note = []
    if query:
        filter_note.append(f"search “{query}”")
    if regions and set(regions) != set(REGIONS):
        filter_note.append(f"{len(regions)} region(s)")
    note = " · ".join(filter_note) if filter_note else "all cities"

    st.markdown(
        f"""
        <div class="section-head">
          <div>
            <h2>Cities · 城市</h2>
            <p>Showing {len(visible)} of {len(CITIES)} cities · {note}. Click a card for details.</p>
          </div>
          <span class="section-note">{now.strftime('%H:%M')} CST</span>
        </div>""",
        unsafe_allow_html=True,
    )

    if not visible:
        st.info("No cities match that search. Try another name or clear the region filter.")
        st.markdown(footer_html("demo" if error else "live", now.strftime("%H:%M")), unsafe_allow_html=True)
        return

    st.markdown(city_card_css(overview, visible), unsafe_allow_html=True)
    with st.container(key="city_grid"):
        columns = st.columns(4, gap="small")
        for index, city in enumerate(visible):
            weather = overview.get(city.slug)
            if not weather:
                continue
            label, foot = city_labels(city, weather, unit)
            with columns[index % 4]:
                if st.button(
                    label,
                    key=f"city_{city.slug}",
                    width="stretch",
                    help=f"Open the {city.name_en} forecast",
                ):
                    open_city(city.slug)
                st.markdown(foot, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="section-head">
          <div>
            <h2>Weather map · 天气地图</h2>
            <p>Marker colour shows current temperature across the country.</p>
          </div>
        </div>""",
        unsafe_allow_html=True,
    )
    render_map_section(visible, overview, unit)
    updated = next(iter(overview.values()), {}).get("time", "")[11:16]
    st.markdown(footer_html("demo" if error else "live", updated or now.strftime("%H:%M")), unsafe_allow_html=True)


if __name__ == "__main__":
    main()
