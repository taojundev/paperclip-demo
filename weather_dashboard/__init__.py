"""China City Weather — data, API and UI helpers for the Streamlit dashboard."""

from .cities import CITIES, CITY_BY_SLUG, REGIONS, City, weather_code_info
from .api import (
    WeatherError,
    demo_detail,
    demo_overview,
    fetch_detail,
    fetch_overview,
)

__all__ = [
    "CITIES",
    "CITY_BY_SLUG",
    "REGIONS",
    "City",
    "weather_code_info",
    "WeatherError",
    "demo_detail",
    "demo_overview",
    "fetch_detail",
    "fetch_overview",
]
