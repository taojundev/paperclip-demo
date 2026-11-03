"""Major Chinese cities and WMO weather-code presentation metadata."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class City:
    """A city shown on the dashboard."""

    slug: str
    name_zh: str
    name_en: str
    province: str
    region: str
    lat: float
    lon: float

    @property
    def label(self) -> str:
        return f"{self.name_zh} · {self.name_en}"


CITIES: tuple[City, ...] = (
    City("beijing", "北京", "Beijing", "Beijing", "North", 39.9042, 116.4074),
    City("tianjin", "天津", "Tianjin", "Tianjin", "North", 39.3434, 117.3616),
    City("shijiazhuang", "石家庄", "Shijiazhuang", "Hebei", "North", 38.0428, 114.5149),
    City("harbin", "哈尔滨", "Harbin", "Heilongjiang", "Northeast", 45.8038, 126.5349),
    City("shenyang", "沈阳", "Shenyang", "Liaoning", "Northeast", 41.8057, 123.4315),
    City("dalian", "大连", "Dalian", "Liaoning", "Northeast", 38.9140, 121.6147),
    City("shanghai", "上海", "Shanghai", "Shanghai", "East", 31.2304, 121.4737),
    City("nanjing", "南京", "Nanjing", "Jiangsu", "East", 32.0603, 118.7969),
    City("suzhou", "苏州", "Suzhou", "Jiangsu", "East", 31.2989, 120.5853),
    City("hangzhou", "杭州", "Hangzhou", "Zhejiang", "East", 30.2741, 120.1551),
    City("hefei", "合肥", "Hefei", "Anhui", "East", 31.8206, 117.2272),
    City("qingdao", "青岛", "Qingdao", "Shandong", "East", 36.0671, 120.3826),
    City("xiamen", "厦门", "Xiamen", "Fujian", "Southeast", 24.4798, 118.0894),
    City("fuzhou", "福州", "Fuzhou", "Fujian", "Southeast", 26.0745, 119.2965),
    City("guangzhou", "广州", "Guangzhou", "Guangdong", "South", 23.1291, 113.2644),
    City("shenzhen", "深圳", "Shenzhen", "Guangdong", "South", 22.5431, 114.0579),
    City("zhuhai", "珠海", "Zhuhai", "Guangdong", "South", 22.2710, 113.5767),
    City("hongkong", "香港", "Hong Kong", "Hong Kong SAR", "South", 22.3193, 114.1694),
    City("macau", "澳门", "Macau", "Macau SAR", "South", 22.1987, 113.5439),
    City("sanya", "三亚", "Sanya", "Hainan", "South", 18.2528, 109.5119),
    City("wuhan", "武汉", "Wuhan", "Hubei", "Central", 30.5928, 114.3055),
    City("changsha", "长沙", "Changsha", "Hunan", "Central", 28.2282, 112.9388),
    City("zhengzhou", "郑州", "Zhengzhou", "Henan", "Central", 34.7466, 113.6254),
    City("nanchang", "南昌", "Nanchang", "Jiangxi", "Central", 28.6820, 115.8579),
    City("chengdu", "成都", "Chengdu", "Sichuan", "Southwest", 30.5728, 104.0668),
    City("chongqing", "重庆", "Chongqing", "Chongqing", "Southwest", 29.5630, 106.5516),
    City("kunming", "昆明", "Kunming", "Yunnan", "Southwest", 25.0389, 102.7183),
    City("guiyang", "贵阳", "Guiyang", "Guizhou", "Southwest", 26.6470, 106.6302),
    City("guilin", "桂林", "Guilin", "Guangxi", "Southwest", 25.2736, 110.2900),
    City("xian", "西安", "Xi'an", "Shaanxi", "Northwest", 34.3416, 108.9398),
    City("lanzhou", "兰州", "Lanzhou", "Gansu", "Northwest", 36.0611, 103.8343),
    City("urumqi", "乌鲁木齐", "Urumqi", "Xinjiang", "Northwest", 43.8256, 87.6168),
    City("lhasa", "拉萨", "Lhasa", "Tibet", "Southwest", 29.6520, 91.1721),
    City("xining", "西宁", "Xining", "Qinghai", "Northwest", 36.6171, 101.7782),
    City("hohhot", "呼和浩特", "Hohhot", "Inner Mongolia", "North", 40.8426, 111.7492),
)

CITY_BY_SLUG: dict[str, City] = {city.slug: city for city in CITIES}

REGIONS: tuple[str, ...] = (
    "North",
    "Northeast",
    "East",
    "Southeast",
    "South",
    "Central",
    "Southwest",
    "Northwest",
)


# WMO weather interpretation codes used by Open-Meteo.
# code: (English label, Chinese label, day emoji, night emoji, kind)
_WEATHER_CODES: dict[int, tuple[str, str, str, str, str]] = {
    0: ("Clear sky", "晴", "☀️", "🌙", "clear"),
    1: ("Mainly clear", "晴间多云", "🌤️", "🌙", "clear"),
    2: ("Partly cloudy", "多云", "⛅", "☁️", "cloudy"),
    3: ("Overcast", "阴", "☁️", "☁️", "cloudy"),
    45: ("Fog", "雾", "🌫️", "🌫️", "fog"),
    48: ("Rime fog", "雾凇", "🌫️", "🌫️", "fog"),
    51: ("Light drizzle", "小毛毛雨", "🌦️", "🌧️", "rain"),
    53: ("Drizzle", "毛毛雨", "🌦️", "🌧️", "rain"),
    55: ("Heavy drizzle", "强毛毛雨", "🌧️", "🌧️", "rain"),
    56: ("Freezing drizzle", "冻毛毛雨", "🌨️", "🌨️", "snow"),
    57: ("Heavy freezing drizzle", "强冻毛毛雨", "🌨️", "🌨️", "snow"),
    61: ("Light rain", "小雨", "🌦️", "🌧️", "rain"),
    63: ("Rain", "中雨", "🌧️", "🌧️", "rain"),
    65: ("Heavy rain", "大雨", "🌧️", "🌧️", "rain"),
    66: ("Freezing rain", "冻雨", "🌨️", "🌨️", "snow"),
    67: ("Heavy freezing rain", "强冻雨", "🌨️", "🌨️", "snow"),
    71: ("Light snow", "小雪", "🌨️", "🌨️", "snow"),
    73: ("Snow", "中雪", "❄️", "❄️", "snow"),
    75: ("Heavy snow", "大雪", "❄️", "❄️", "snow"),
    77: ("Snow grains", "雪粒", "🌨️", "🌨️", "snow"),
    80: ("Light showers", "小阵雨", "🌦️", "🌧️", "rain"),
    81: ("Showers", "阵雨", "🌧️", "🌧️", "rain"),
    82: ("Heavy showers", "强阵雨", "⛈️", "⛈️", "rain"),
    85: ("Snow showers", "阵雪", "🌨️", "🌨️", "snow"),
    86: ("Heavy snow showers", "强阵雪", "❄️", "❄️", "snow"),
    95: ("Thunderstorm", "雷阵雨", "⛈️", "⛈️", "storm"),
    96: ("Thunderstorm with hail", "雷暴伴冰雹", "⛈️", "⛈️", "storm"),
    99: ("Severe thunderstorm", "强雷暴伴冰雹", "⛈️", "⛈️", "storm"),
}

_UNKNOWN_CODE = ("Unknown", "未知", "🌡️", "🌡️", "cloudy")


def weather_code_info(code: int | float | None, is_day: bool = True) -> dict[str, str]:
    """Return presentation metadata for a WMO weather code."""

    try:
        meta = _WEATHER_CODES.get(int(code or 0), _UNKNOWN_CODE)
    except (TypeError, ValueError):
        meta = _UNKNOWN_CODE
    label_en, label_zh, day_emoji, night_emoji, kind = meta
    return {
        "label_en": label_en,
        "label_zh": label_zh,
        "emoji": day_emoji if is_day else night_emoji,
        "day_emoji": day_emoji,
        "kind": kind,
    }
