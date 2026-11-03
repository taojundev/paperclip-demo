"""Live Open-Meteo data access plus an offline demo fallback."""

from __future__ import annotations

import math
import random
from datetime import datetime, timedelta
from typing import Iterable, Sequence
from zoneinfo import ZoneInfo

import requests

from .cities import City, weather_code_info

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
TIMEZONE = "Asia/Shanghai"
REQUEST_TIMEOUT = 15
CN_TZ = ZoneInfo(TIMEZONE)


class WeatherError(RuntimeError):
    """Raised when live weather data cannot be fetched."""


# ---------------------------------------------------------------------------
# Small parsing helpers
# ---------------------------------------------------------------------------


def _f(value: object, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _i(value: object, default: int = 0) -> int:
    try:
        if value is None:
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def _now() -> datetime:
    return datetime.now(CN_TZ)


def _chunks(items: Sequence[City], size: int) -> Iterable[Sequence[City]]:
    for start in range(0, len(items), size):
        yield items[start : start + size]


def _get_json(url: str, params: dict[str, object]) -> dict | list:
    try:
        response = requests.get(
            url,
            params=params,
            timeout=REQUEST_TIMEOUT,
            headers={"User-Agent": "china-weather-dashboard/1.0"},
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise WeatherError(f"Weather service unavailable: {exc}") from exc
    except ValueError as exc:
        raise WeatherError("Weather service returned an invalid response.") from exc


# ---------------------------------------------------------------------------
# Normalisation
# ---------------------------------------------------------------------------


def _normalise_overview(item: dict) -> dict:
    current = item.get("current") or {}
    daily = item.get("daily") or {}
    code = _i(current.get("weather_code"))
    is_day = bool(_i(current.get("is_day"), 1))

    def daily_value(key: str, default: float = 0.0) -> float:
        values = daily.get(key) or []
        return _f(values[0], default) if values else default

    return {
        "temp": _f(current.get("temperature_2m")),
        "feels": _f(current.get("apparent_temperature")),
        "humidity": _i(current.get("relative_humidity_2m")),
        "precip": _f(current.get("precipitation")),
        "code": code,
        "is_day": is_day,
        "wind": _f(current.get("wind_speed_10m")),
        "wind_dir": _i(current.get("wind_direction_10m")),
        "pressure": _f(current.get("surface_pressure"), 1013),
        "cloud": _i(current.get("cloud_cover")),
        "high": daily_value("temperature_2m_max"),
        "low": daily_value("temperature_2m_min"),
        "rain_chance": _i(daily_value("precipitation_probability_max")),
        "sunrise": (daily.get("sunrise") or [""])[0],
        "sunset": (daily.get("sunset") or [""])[0],
        "time": current.get("time", ""),
        "condition": weather_code_info(code, is_day),
    }


def _normalise_detail(payload: dict) -> dict:
    current = payload.get("current") or {}
    hourly = payload.get("hourly") or {}
    daily = payload.get("daily") or {}
    current_time = current.get("time", "")
    current_hour = current_time[:13]

    times: list[str] = list(hourly.get("time") or [])
    start = 0
    for index, stamp in enumerate(times):
        if stamp[:13] == current_hour:
            start = index
            break
    window = slice(start, start + 24)

    def series(key: str, cast=_f) -> list:
        values = list(hourly.get(key) or [])
        sliced = values[window]
        return [cast(value) for value in sliced]

    def maybe_at(key: str, cast=_f, default=0):
        values = list(hourly.get(key) or [])
        if not values:
            return default
        index = min(start, len(values) - 1)
        return cast(values[index])

    overview = _normalise_overview(payload)
    overview["visibility"] = maybe_at("visibility", _f, 10000) / 1000
    overview["uv"] = maybe_at("uv_index", _f, 0)

    normalised_daily = {
        "time": list(daily.get("time") or []),
        "code": [_i(v) for v in (daily.get("weather_code") or [])],
        "high": [_f(v) for v in (daily.get("temperature_2m_max") or [])],
        "low": [_f(v) for v in (daily.get("temperature_2m_min") or [])],
        "rain_chance": [
            _i(v) for v in (daily.get("precipitation_probability_max") or [])
        ],
        "precip_sum": [_f(v) for v in (daily.get("precipitation_sum") or [])],
        "uv": [_f(v) for v in (daily.get("uv_index_max") or [])],
        "sunrise": list(daily.get("sunrise") or []),
        "sunset": list(daily.get("sunset") or []),
        "wind_max": [_f(v) for v in (daily.get("wind_speed_10m_max") or [])],
        "wind_dir": [_i(v) for v in (daily.get("wind_direction_10m_dominant") or [])],
    }

    return {
        "current": overview,
        "hourly": {
            "time": times[window],
            "temp": series("temperature_2m"),
            "feels": series("apparent_temperature"),
            "rain_chance": series("precipitation_probability", _i),
            "precip": series("precipitation"),
            "code": series("weather_code", _i),
            "wind": series("wind_speed_10m"),
            "humidity": series("relative_humidity_2m", _i),
            "visibility": series("visibility"),
            "uv": series("uv_index"),
            "is_day": series("is_day", lambda v: bool(_i(v, 1))),
        },
        "daily": normalised_daily,
        "air": None,
        "time": current_time,
        "source": "live",
    }


def _normalise_air(payload: dict) -> dict | None:
    current = payload.get("current") or {}
    if not current:
        return None
    return {
        "time": current.get("time", ""),
        "pm2_5": _f(current.get("pm2_5")),
        "pm10": _f(current.get("pm10")),
        "european_aqi": _i(current.get("european_aqi")),
        "us_aqi": _i(current.get("us_aqi")),
        "ozone": _f(current.get("ozone")),
        "no2": _f(current.get("nitrogen_dioxide")),
        "so2": _f(current.get("sulphur_dioxide")),
        "co": _f(current.get("carbon_monoxide")),
    }


# ---------------------------------------------------------------------------
# Live API
# ---------------------------------------------------------------------------


def _overview_params(cities: Sequence[City]) -> dict[str, object]:
    return {
        "latitude": ",".join(f"{city.lat:.4f}" for city in cities),
        "longitude": ",".join(f"{city.lon:.4f}" for city in cities),
        "current": (
            "temperature_2m,apparent_temperature,relative_humidity_2m,"
            "precipitation,weather_code,cloud_cover,wind_speed_10m,"
            "wind_direction_10m,surface_pressure,is_day"
        ),
        "daily": (
            "weather_code,temperature_2m_max,temperature_2m_min,"
            "precipitation_probability_max,sunrise,sunset"
        ),
        "timezone": TIMEZONE,
        "forecast_days": 1,
    }


def fetch_overview(cities: Sequence[City]) -> dict[str, dict]:
    """Fetch current conditions and today's range for several cities."""

    result: dict[str, dict] = {}
    for group in _chunks(cities, 25):
        payload = _get_json(FORECAST_URL, _overview_params(group))
        if isinstance(payload, dict):
            payload = [payload]
        if not isinstance(payload, list) or not payload:
            raise WeatherError("Weather service returned no data.")
        for city, item in zip(group, payload):
            result[city.slug] = _normalise_overview(item)
    if not result:
        raise WeatherError("No city weather data was returned.")
    return result


def fetch_detail(city: City) -> dict:
    """Fetch current, 24-hour and 7-day forecast detail for one city."""

    params = {
        "latitude": city.lat,
        "longitude": city.lon,
        "current": (
            "temperature_2m,relative_humidity_2m,apparent_temperature,is_day,"
            "precipitation,weather_code,cloud_cover,pressure_msl,"
            "surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m"
        ),
        "hourly": (
            "temperature_2m,apparent_temperature,precipitation_probability,"
            "precipitation,weather_code,wind_speed_10m,relative_humidity_2m,"
            "visibility,uv_index,is_day"
        ),
        "daily": (
            "weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,"
            "uv_index_max,precipitation_sum,precipitation_probability_max,"
            "wind_speed_10m_max,wind_direction_10m_dominant"
        ),
        "timezone": TIMEZONE,
        "forecast_days": 7,
    }
    payload = _get_json(FORECAST_URL, params)
    if not isinstance(payload, dict):
        raise WeatherError("Weather service returned an unexpected response.")

    detail = _normalise_detail(payload)

    try:
        air_payload = _get_json(
            AIR_QUALITY_URL,
            {
                "latitude": city.lat,
                "longitude": city.lon,
                "current": (
                    "pm2_5,pm10,european_aqi,us_aqi,ozone,nitrogen_dioxide,"
                    "sulphur_dioxide,carbon_monoxide"
                ),
                "timezone": TIMEZONE,
            },
        )
        if isinstance(air_payload, dict):
            detail["air"] = _normalise_air(air_payload)
    except WeatherError:
        # Air quality is a bonus; the forecast is still useful without it.
        detail["air"] = None

    return detail


# ---------------------------------------------------------------------------
# Offline demo fallback
# ---------------------------------------------------------------------------

_ALTITUDE_ADJUSTMENT = {"Tibet": -7.0, "Qinghai": -6.0, "Yunnan": -3.0}


def _base_temperature(city: City, day: datetime) -> float:
    day_of_year = day.timetuple().tm_yday
    annual = 26.0 - max(0.0, city.lat - 20.0) * 0.55
    amplitude = 8.5 + max(0.0, city.lat - 24.0) * 0.35
    if city.region in {"North", "Northeast", "Northwest"}:
        amplitude += 2.0
    if city.region in {"South", "Southeast"}:
        amplitude -= 1.0
    seasonal = amplitude * math.cos(2 * math.pi * (day_of_year - 200) / 365)
    return annual + seasonal + _ALTITUDE_ADJUSTMENT.get(city.province, 0.0)


def _demo_day(city: City, day: datetime, rng: random.Random) -> dict:
    base = _base_temperature(city, day)
    swing = 4.0 + rng.uniform(0.0, 2.5)
    high = base + swing + rng.uniform(-1.0, 1.5)
    low = base - swing + rng.uniform(-1.5, 1.0)
    humidity = min(96, max(24, 55 + rng.uniform(-18, 28)))
    rain_chance = min(92, max(2, (humidity - 48) * 1.6 + rng.uniform(-12, 22)))

    if rng.random() * 100 < rain_chance:
        if high < 1:
            code = rng.choice([71, 73, 75, 85])
        elif high < 4:
            code = rng.choice([66, 71, 80])
        else:
            code = rng.choice([51, 61, 63, 80, 81])
    else:
        code = rng.choice([0, 0, 1, 1, 2, 2, 3, 3, 45])

    sunrise = day.replace(hour=6, minute=rng.randint(5, 50), second=0, microsecond=0)
    sunset = day.replace(hour=18, minute=rng.randint(0, 45), second=0, microsecond=0)
    return {
        "date": day,
        "high": round(high, 1),
        "low": round(low, 1),
        "humidity": round(humidity),
        "rain_chance": round(rain_chance),
        "precip_sum": round(rng.uniform(0, 12) * rain_chance / 100, 1),
        "uv": round(max(0.5, 7.5 - abs(city.lat - 25) * 0.08) * rng.uniform(0.55, 1.0), 1),
        "wind_max": round(rng.uniform(6, 34), 1),
        "wind_dir": rng.choice([0, 45, 90, 135, 180, 225, 270, 315]),
        "code": code,
        "sunrise": sunrise,
        "sunset": sunset,
    }


def _demo_current(city: City, now: datetime, rng: random.Random) -> dict:
    today = _demo_day(city, now.replace(hour=0, minute=0, second=0, microsecond=0), rng)
    hour = now.hour + now.minute / 60
    fraction = 0.5 + 0.5 * math.sin(2 * math.pi * (hour - 9) / 24)
    temp = today["low"] + (today["high"] - today["low"]) * fraction
    is_day = 6 <= hour < 18
    return {
        "temp": round(temp, 1),
        "feels": round(temp + rng.uniform(-2.2, 2.2), 1),
        "humidity": today["humidity"],
        "precip": round(rng.uniform(0, 2.5) * today["rain_chance"] / 100, 1),
        "code": today["code"],
        "is_day": is_day,
        "wind": round(rng.uniform(2, 24), 1),
        "wind_dir": today["wind_dir"],
        "pressure": round(1013 + rng.uniform(-9, 9), 1),
        "cloud": round(min(100, max(0, rng.uniform(5, 95)))),
        "high": today["high"],
        "low": today["low"],
        "rain_chance": today["rain_chance"],
        "sunrise": today["sunrise"].isoformat(),
        "sunset": today["sunset"].isoformat(),
        "time": now.strftime("%Y-%m-%dT%H:%M"),
        "condition": weather_code_info(today["code"], is_day),
    }


def demo_overview(cities: Sequence[City], now: datetime | None = None) -> dict[str, dict]:
    """Deterministic, plausible fallback data so the UI always renders."""

    now = now or _now()
    result = {}
    for city in cities:
        rng = random.Random(f"{city.slug}:{now.date().isoformat()}")
        result[city.slug] = _demo_current(city, now, rng)
    return result


def demo_detail(city: City, now: datetime | None = None) -> dict:
    """Build a full demo forecast, used when Open-Meteo is unreachable."""

    now = now or _now()
    rng = random.Random(f"{city.slug}:{now.date().isoformat()}:detail")
    start_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    days = [_demo_day(city, start_day + timedelta(days=offset), rng) for offset in range(7)]

    current = _demo_current(city, now, rng)
    current["visibility"] = round(rng.uniform(6, 24), 1)
    current["uv"] = days[0]["uv"] if current["is_day"] else 0.0

    hourly = {
        "time": [],
        "temp": [],
        "feels": [],
        "rain_chance": [],
        "precip": [],
        "code": [],
        "wind": [],
        "humidity": [],
        "visibility": [],
        "uv": [],
        "is_day": [],
    }
    for offset in range(24):
        moment = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=offset)
        day = days[0]
        if moment.date() > start_day.date() and len(days) > 1:
            day = days[1]
        fraction = 0.5 + 0.5 * math.sin(2 * math.pi * ((moment.hour + moment.minute / 60) - 9) / 24)
        temp = day["low"] + (day["high"] - day["low"]) * fraction
        daylight = 6 <= moment.hour < 18
        chance = int(min(98, max(0, day["rain_chance"] + (10 if not daylight else 0))))
        hourly["time"].append(moment.strftime("%Y-%m-%dT%H:%M"))
        hourly["temp"].append(round(temp, 1))
        hourly["feels"].append(round(temp + rng.uniform(-2, 2), 1))
        hourly["rain_chance"].append(chance)
        hourly["precip"].append(round(rng.uniform(0, 3) * chance / 100, 1))
        hourly["code"].append(day["code"])
        hourly["wind"].append(round(rng.uniform(2, 26), 1))
        hourly["humidity"].append(day["humidity"])
        hourly["visibility"].append(round(rng.uniform(8, 25) * 1000))
        hourly["uv"].append(round(max(0.0, 6.5 * math.sin(math.pi * (moment.hour - 6) / 12)), 1))
        hourly["is_day"].append(daylight)

    pm2_5 = round(rng.uniform(14, 95), 1)
    aqi = int(min(180, max(8, pm2_5 * 1.25 + rng.uniform(-12, 16))))

    return {
        "current": current,
        "hourly": hourly,
        "daily": {
            "time": [day["date"].date().isoformat() for day in days],
            "code": [day["code"] for day in days],
            "high": [day["high"] for day in days],
            "low": [day["low"] for day in days],
            "rain_chance": [day["rain_chance"] for day in days],
            "precip_sum": [day["precip_sum"] for day in days],
            "uv": [day["uv"] for day in days],
            "sunrise": [day["sunrise"].isoformat() for day in days],
            "sunset": [day["sunset"].isoformat() for day in days],
            "wind_max": [day["wind_max"] for day in days],
            "wind_dir": [day["wind_dir"] for day in days],
        },
        "air": {
            "time": now.strftime("%Y-%m-%dT%H:%M"),
            "pm2_5": pm2_5,
            "pm10": round(pm2_5 * rng.uniform(1.2, 1.8), 1),
            "european_aqi": aqi,
            "us_aqi": int(aqi * 1.3),
            "ozone": round(rng.uniform(30, 110), 1),
            "no2": round(rng.uniform(8, 65), 1),
            "so2": round(rng.uniform(2, 24), 1),
            "co": round(rng.uniform(200, 900), 1),
        },
        "time": current["time"],
        "source": "demo",
    }
