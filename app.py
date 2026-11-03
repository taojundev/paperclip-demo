"""China City Weather — a Streamlit dashboard for major Chinese cities."""

from __future__ import annotations

import html
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
from weather_dashboard.i18n import DEFAULT_LANGUAGE, region_label, t
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


def current_language() -> str:
    """Return the active UI language, initialising English on first load."""

    if "language" not in st.session_state:
        st.session_state["language"] = DEFAULT_LANGUAGE
    return st.session_state["language"]


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
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    """Show the weather map beside the warmest/coldest ladder."""

    map_column, side_column = st.columns([2.15, 1], gap="medium")
    with map_column:
        st.plotly_chart(
            map_chart(cities, overview, selected_slug, unit, lang),
            width="stretch",
            theme=None,
            config=PLOT_CONFIG,
        )
    with side_column:
        st.markdown(
            extremes_html(cities, overview, unit, lang),
            unsafe_allow_html=True,
        )


def source_alert(error: str | None, lang: str = DEFAULT_LANGUAGE) -> None:
    if not error:
        return
    st.markdown(
        f"""
        <div class="alert info">
          <span class="a-icon">🛰️</span>
          <div><b>{t('demo_title', lang)}</b> {t('demo_body', lang)}</div>
        </div>""",
        unsafe_allow_html=True,
    )
    with st.expander(t("technical_details", lang)):
        st.code(error)


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------


def render_sidebar(
    overview: dict[str, dict],
    error: str | None,
    unit: str,
    lang: str,
) -> tuple[str, str, list[str]]:
    with st.sidebar:
        st.markdown(
            f'<div class="side-label" style="margin-top:0">{t("language_label", lang)}</div>',
            unsafe_allow_html=True,
        )
        if st.button(
            t("language_button", lang),
            key="lang_toggle",
            width="stretch",
            help="切换中文 / Switch to English",
        ):
            st.session_state["language"] = "zh" if lang == "en" else "en"
            st.rerun()

        st.markdown(
            f"""
            <div class="side-brand">
              <div class="side-logo">🌤️</div>
              <div class="side-title">{t('brand_title', lang)}<span>{t('brand_subtitle', lang)}</span></div>
            </div>
            <div class="side-copy">{t('side_copy', lang)}</div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="side-label">{t("temperature_unit", lang)}</div>',
            unsafe_allow_html=True,
        )
        picked_unit = st.segmented_control(
            t("temperature_unit", lang),
            options=["°C", "°F"],
            default=unit,
            required=True,
            key="unit",
            label_visibility="collapsed",
        )
        unit = picked_unit or "°C"

        st.markdown(
            f'<div class="side-label">{t("search_cities", lang)}</div>',
            unsafe_allow_html=True,
        )
        query = st.text_input(
            t("search_cities", lang),
            placeholder=t("search_placeholder", lang),
            label_visibility="collapsed",
        )

        st.markdown(
            f'<div class="side-label">{t("regions", lang)}</div>',
            unsafe_allow_html=True,
        )
        regions = st.multiselect(
            t("regions", lang),
            options=list(REGIONS),
            default=[],
            placeholder=t("all_regions", lang),
            label_visibility="collapsed",
            format_func=lambda region: region_label(region, lang),
        )

        status_class = "live" if not error else "demo"
        status_text = t("status_live" if not error else "status_demo", lang)
        updated = next(iter(overview.values()), {}).get("time", "")[11:16] if overview else "—"
        st.markdown(
            f"""
            <div class="side-status">
              <div class="row"><span>{t('source', lang)}</span><b class="{status_class}">{status_text}</b></div>
              <div class="row"><span>{t('cities', lang)}</span><b>{len(overview)}</b></div>
              <div class="row"><span>{t('updated', lang)}</span><b>{updated or '—'} {t('cst', lang)}</b></div>
              <div class="row"><span>{t('cache', lang)}</span><b>{t('cache_value', lang)}</b></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(t("refresh", lang), width="stretch"):
            st.cache_data.clear()
            st.rerun()

        if st.button(t("surprise", lang), width="stretch"):
            open_city(random.choice(CITIES).slug)

        st.markdown(
            f'<div class="side-foot">{t("side_footer", lang)}</div>',
            unsafe_allow_html=True,
        )

        with st.expander(t("about_title", lang)):
            st.markdown(t("about_body", lang))

    return unit, query, regions


# ---------------------------------------------------------------------------
# Overview page
# ---------------------------------------------------------------------------


def render_overview(
    overview: dict[str, dict],
    error: str | None,
    unit: str,
    lang: str,
) -> None:
    now = now_china()
    st.markdown(hero_html(now, error is None, len(CITIES), lang), unsafe_allow_html=True)
    source_alert(error, lang)
    st.markdown(stats_html(overview, CITY_BY_SLUG, unit, lang), unsafe_allow_html=True)

    section = f"""
    <div class="section-head">
      <div>
        <h2>{t('major_title', lang)}</h2>
        <p>{t('major_sub', lang)}</p>
      </div>
      <span class="section-note">{t('major_note', lang, count=len(CITIES), time=now.strftime('%H:%M'))}</span>
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
            label, foot = city_labels(city, weather, unit, lang)
            city_name = city.name_zh if lang == "zh" else city.name_en
            with columns[index % 4]:
                if st.button(
                    label,
                    key=f"city_{city.slug}",
                    width="stretch",
                    help=t("help_open_city", lang, city=city_name),
                ):
                    open_city(city.slug)
                st.markdown(foot, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="section-head">
          <div>
            <h2>{t('map_title', lang)}</h2>
            <p>{t('map_sub', lang)}</p>
          </div>
          <span class="section-note">{t('map_note', lang)}</span>
        </div>""",
        unsafe_allow_html=True,
    )
    render_map_section(CITIES, overview, unit, lang=lang)
    updated = next(iter(overview.values()), {}).get("time", "")[11:16]
    st.markdown(
        footer_html("demo" if error else "live", updated or now.strftime("%H:%M"), lang),
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Detail page
# ---------------------------------------------------------------------------


def render_detail(city: City, overview: dict[str, dict], unit: str, lang: str) -> None:
    detail, error = load_detail(city.slug)
    now = now_china()
    city_name = city.name_zh if lang == "zh" else city.name_en

    if st.button(t("back", lang), key="back_btn"):
        st.query_params.clear()
        st.rerun()

    st.markdown(detail_hero_html(city, detail, unit, lang), unsafe_allow_html=True)
    source_alert(error, lang)
    st.markdown(alerts_html(city, detail, unit, lang), unsafe_allow_html=True)
    st.markdown(metrics_html(detail, unit, lang), unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="section-head">
          <div>
            <h2>{t('daily_title', lang)}</h2>
            <p>{t('daily_sub', lang, city=city_name)}</p>
          </div>
          <span class="section-note">{t('daily_note', lang, time=detail['time'][11:16])}</span>
        </div>""",
        unsafe_allow_html=True,
    )
    st.markdown(daily_html(detail, unit, lang), unsafe_allow_html=True)

    tab_hourly, tab_map, tab_sun = st.tabs(
        [t("tab_hourly", lang), t("tab_map", lang), t("tab_sun", lang)]
    )

    with tab_hourly:
        st.markdown(
            f"""
            <div class="section-head">
              <div>
                <h2>{t('hourly_title', lang)}</h2>
                <p>{t('hourly_sub', lang)}</p>
              </div>
            </div>""",
            unsafe_allow_html=True,
        )
        st.plotly_chart(
            hourly_chart(detail, unit, lang),
            width="stretch",
            theme=None,
            config=PLOT_CONFIG,
        )
        st.caption(t("hourly_caption", lang))

    with tab_map:
        st.markdown(
            f"""
            <div class="section-head">
              <div>
                <h2>{t('map_tab_title', lang, city=city_name)}</h2>
                <p>{t('map_tab_sub', lang, city=city_name)}</p>
              </div>
            </div>""",
            unsafe_allow_html=True,
        )
        render_map_section(CITIES, overview, unit, city.slug, lang)

    with tab_sun:
        st.markdown(
            f"""
            <div class="section-head">
              <div>
                <h2>{t('sun_tab_title', lang)}</h2>
                <p>{t('sun_tab_sub', lang)}</p>
              </div>
            </div>""",
            unsafe_allow_html=True,
        )
        st.markdown(sun_air_html(detail, unit, lang), unsafe_allow_html=True)
        st.caption(t("sun_tab_caption", lang))

    st.markdown(
        footer_html(
            "demo" if error else "live",
            detail["time"][11:16] or now.strftime("%H:%M"),
            lang,
        ),
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
    lang = current_language()

    # The overview powers both the sidebar status and the city map.
    overview, overview_error = load_overview(tuple(city.slug for city in CITIES))
    unit, query, regions = render_sidebar(overview, overview_error, "°C", lang)

    selected = selected_city_from_query()
    if selected:
        render_detail(selected, overview, unit, lang)
    else:
        visible = filtered_cities(query, regions)
        if not query and (not regions or set(regions) == set(REGIONS)):
            render_overview(overview, overview_error, unit, lang)
        else:
            # Reuse the overview layout with the current filter applied.
            render_filtered_overview(
                overview, overview_error, unit, visible, query, regions, lang
            )


def render_filtered_overview(
    overview: dict[str, dict],
    error: str | None,
    unit: str,
    visible: list[City],
    query: str,
    regions: list[str],
    lang: str,
) -> None:
    now = now_china()
    st.markdown(hero_html(now, error is None, len(CITIES), lang), unsafe_allow_html=True)
    source_alert(error, lang)
    st.markdown(stats_html(overview, CITY_BY_SLUG, unit, lang), unsafe_allow_html=True)

    filter_note = []
    if query:
        filter_note.append(t("filter_search_note", lang, query=html.escape(query)))
    if regions and set(regions) != set(REGIONS):
        filter_note.append(t("filter_regions_note", lang, count=len(regions)))
    note = " · ".join(filter_note) if filter_note else t("filter_all_note", lang)

    st.markdown(
        f"""
        <div class="section-head">
          <div>
            <h2>{t('cities_title', lang)}</h2>
            <p>{t('cities_sub', lang, visible=len(visible), total=len(CITIES), note=note)}</p>
          </div>
          <span class="section-note">{now.strftime('%H:%M')} {t('cst', lang)}</span>
        </div>""",
        unsafe_allow_html=True,
    )

    if not visible:
        st.info(t("no_match", lang))
        st.markdown(
            footer_html("demo" if error else "live", now.strftime("%H:%M"), lang),
            unsafe_allow_html=True,
        )
        return

    st.markdown(city_card_css(overview, visible), unsafe_allow_html=True)
    with st.container(key="city_grid"):
        columns = st.columns(4, gap="small")
        for index, city in enumerate(visible):
            weather = overview.get(city.slug)
            if not weather:
                continue
            label, foot = city_labels(city, weather, unit, lang)
            city_name = city.name_zh if lang == "zh" else city.name_en
            with columns[index % 4]:
                if st.button(
                    label,
                    key=f"city_{city.slug}",
                    width="stretch",
                    help=t("help_open_city", lang, city=city_name),
                ):
                    open_city(city.slug)
                st.markdown(foot, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="section-head">
          <div>
            <h2>{t('map_title', lang)}</h2>
            <p>{t('map_sub_filtered', lang)}</p>
          </div>
        </div>""",
        unsafe_allow_html=True,
    )
    render_map_section(visible, overview, unit, lang=lang)
    updated = next(iter(overview.values()), {}).get("time", "")[11:16]
    st.markdown(
        footer_html("demo" if error else "live", updated or now.strftime("%H:%M"), lang),
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
