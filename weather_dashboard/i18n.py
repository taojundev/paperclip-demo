"""English/Chinese copy and formatting helpers for the dashboard UI."""

from __future__ import annotations

from datetime import datetime

DEFAULT_LANGUAGE = "en"
LANGUAGES: dict[str, str] = {"en": "English", "zh": "中文"}

# Display labels for the region keys used by the city catalogue.
REGION_LABELS: dict[str, str] = {
    "North": "华北",
    "Northeast": "东北",
    "East": "华东",
    "Southeast": "东南",
    "South": "华南",
    "Central": "华中",
    "Southwest": "西南",
    "Northwest": "西北",
}

# Province / SAR names that appear in the detail-page breadcrumb.
PROVINCE_LABELS: dict[str, str] = {
    "Beijing": "北京",
    "Tianjin": "天津",
    "Hebei": "河北",
    "Heilongjiang": "黑龙江",
    "Liaoning": "辽宁",
    "Shanghai": "上海",
    "Jiangsu": "江苏",
    "Zhejiang": "浙江",
    "Anhui": "安徽",
    "Shandong": "山东",
    "Fujian": "福建",
    "Guangdong": "广东",
    "Hong Kong SAR": "香港特别行政区",
    "Macau SAR": "澳门特别行政区",
    "Hainan": "海南",
    "Hubei": "湖北",
    "Hunan": "湖南",
    "Henan": "河南",
    "Jiangxi": "江西",
    "Sichuan": "四川",
    "Chongqing": "重庆",
    "Yunnan": "云南",
    "Guizhou": "贵州",
    "Guangxi": "广西",
    "Shaanxi": "陕西",
    "Gansu": "甘肃",
    "Xinjiang": "新疆",
    "Tibet": "西藏",
    "Qinghai": "青海",
    "Inner Mongolia": "内蒙古",
}

_WEEKDAYS_ZH = ("星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日")
_WEEKDAYS_ZH_SHORT = ("周一", "周二", "周三", "周四", "周五", "周六", "周日")
_WEEKDAYS_EN_SHORT = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")

_WIND_EN = (
    "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
    "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW",
)
_WIND_ZH = (
    "北", "东北偏北", "东北", "东北偏东", "东", "东南偏东", "东南", "东南偏南",
    "南", "西南偏南", "西南", "西南偏西", "西", "西北偏西", "西北", "西北偏北",
)

STRINGS: dict[str, dict[str, str]] = {
    "en": {
        # Page / sidebar
        "page_title": "China Weather Atlas · 中国城市天气",
        "brand_title": "China Weather",
        "brand_subtitle": "Atlas · 中国城市天气",
        "side_copy": (
            "Current conditions and forecasts for major cities, from the northeast "
            "frontier to the tropical south."
        ),
        "language_label": "Language",
        "language_button": "🌐 中文",
        "temperature_unit": "Temperature unit",
        "search_cities": "Search cities",
        "search_placeholder": "Beijing, 上海, Chengdu…",
        "regions": "Regions",
        "all_regions": "All regions",
        "source": "Source",
        "cities": "Cities",
        "updated": "Updated",
        "cst": "CST",
        "cache": "Cache",
        "cache_value": "10 minutes",
        "status_live": "Live · Open-Meteo",
        "status_demo": "Demo fallback",
        "refresh": "↻ Refresh live data",
        "surprise": "🎲 Surprise me",
        "side_footer": (
            'Powered by <a href="https://open-meteo.com/" target="_blank">Open-Meteo</a>. '
            "Forecasts cover the next 24 hours and 7 days."
        ),
        "about_title": "About this dashboard",
        "about_body": (
            "**35 major cities**, one dashboard.\n\n"
            "- Click any city card to open its detailed forecast\n"
            "- Temperature units and language can be switched here at any time\n"
            "- Data refreshes every 10 minutes, with an offline demo fallback\n"
            "- Air quality comes from the Open-Meteo Air Quality API"
        ),
        # Alerts
        "demo_title": "Showing demo weather.",
        "demo_body": (
            "Live Open-Meteo data could not be reached, so this page is using a "
            "realistic offline fallback. Try refreshing in a moment."
        ),
        "technical_details": "Technical details",
        # Hero
        "hero_kicker": "China Weather Atlas · 中国城市天气",
        "hero_title": 'Weather across <span class="grad">China</span>,<br/>city by city.',
        "hero_sub": (
            "A living forecast for {city_count} major cities — from Harbin's frost to "
            "Sanya's tropical breeze. Click any city card to open its current conditions, "
            "next 24 hours, 7-day outlook, air quality and map."
        ),
        "hero_live": "Live data",
        "hero_demo": "Demo data",
        "hero_timezone": "China Standard Time",
        "hero_cities": "cities tracked",
        # Stats
        "stat_hottest": "Hottest right now",
        "stat_coldest": "Coldest right now",
        "stat_wettest": "Highest rain chance",
        "stat_coverage": "Live coverage",
        "stat_feels": "Feels like {temp}",
        "stat_low_tonight": "Low tonight {temp}",
        "stat_max_prob": "Today's maximum probability",
        "stat_coverage_sub": "Open-Meteo · refreshed every 10 min",
        # Overview
        "major_title": "Major cities",
        "major_sub": "Click a city card to open its current conditions and forecast.",
        "major_note": "{count} cities · {time} CST",
        "help_open_city": "Open the {city} forecast",
        "map_title": "Weather map",
        "map_sub": (
            "Marker colour shows current temperature. Hover a city for today's range."
        ),
        "map_sub_filtered": "Marker colour shows current temperature across the country.",
        "map_note": "Open-Meteo · Asia/Shanghai",
        "cities_title": "Cities",
        "cities_sub": (
            "Showing {visible} of {total} cities · {note}. Click a card for details."
        ),
        "filter_search_note": "search “{query}”",
        "filter_regions_note": "{count} region(s)",
        "filter_all_note": "all cities",
        "no_match": (
            "No cities match that search. Try another name or clear the region filter."
        ),
        # Detail
        "back": "← All cities",
        "crumb": "{region} China · {province}",
        "chip_feels": "Feels like <b>{temp}</b>",
        "chip_high_low": "H <b>{high}</b> / L <b>{low}</b>",
        "chip_humidity": "💧 <b>{value}%</b> humidity",
        "chip_wind": "💨 <b>{value} km/h</b> {direction}",
        "chip_rain": "🌧️ <b>{value}%</b> rain",
        "now_updated": "Updated {time} CST · {condition}",
        # Alerts
        "alert_storm_title": "Thunderstorms in the area",
        "alert_storm_body": (
            "Lightning and heavy showers are possible. Keep an eye on local alerts "
            "before heading out."
        ),
        "alert_heat_title": "Heat advisory",
        "alert_heat_body": (
            "Today's high reaches {temp}. Hydrate often and avoid the midday sun."
        ),
        "alert_hot_title": "A hot one",
        "alert_hot_body": (
            "Today's high is {temp}. Plan outdoor time for the morning or evening."
        ),
        "alert_cold_title": "Bundle up",
        "alert_cold_body": (
            "Tonight drops to {temp}. Wind chill will make it feel colder."
        ),
        "alert_rain_title": "Rain likely",
        "alert_rain_body": (
            "{rain}% chance of precipitation today — an umbrella is a good idea."
        ),
        "alert_wind_title": "Windy conditions",
        "alert_wind_body": (
            "Gusts up to {wind} km/h are forecast. Secure loose items outdoors."
        ),
        "alert_aqi_title": "Air quality: {label}",
        "alert_aqi_body": (
            "European AQI is {aqi}. Consider reducing strenuous outdoor activity."
        ),
        # Metrics
        "metric_feels": "Feels like",
        "metric_actual": "Actual {temp}",
        "metric_humidity": "Humidity",
        "metric_relative_humidity": "Relative humidity",
        "metric_wind": "Wind",
        "metric_from": "From {direction} · {degrees}°",
        "metric_pressure": "Pressure",
        "metric_surface_pressure": "Surface pressure",
        "metric_visibility": "Visibility",
        "metric_horizontal_visibility": "Horizontal visibility",
        "metric_uv": "UV index",
        "metric_uv_sub": "{label} exposure",
        "metric_rain": "Rain chance",
        "metric_rain_sub": "Maximum today",
        "metric_air": "Air quality",
        # Forecast / tabs
        "daily_title": "7-day forecast",
        "daily_sub": "Daily highs, lows and rain probability for {city}.",
        "daily_note": "Updated {time} CST",
        "day_today": "Today",
        "no_daily": "No daily forecast available.",
        "tab_hourly": "📈 Next 24 hours",
        "tab_map": "🗺️ Weather map",
        "tab_sun": "🌅 Sun & air",
        "hourly_title": "Rolling 24-hour forecast",
        "hourly_sub": (
            "Temperature and rain probability. Shaded bands mark night-time."
        ),
        "hourly_caption": (
            "Hover the chart for feels-like temperature, humidity, wind and rainfall. "
            "The teal dot marks the current hour."
        ),
        "map_tab_title": "{city} on the map",
        "map_tab_sub": (
            "The gold star marks {city}; every city is coloured by current temperature."
        ),
        "sun_tab_title": "Sunlight and air",
        "sun_tab_sub": (
            "Today's daylight window plus the latest air-quality reading."
        ),
        "sun_tab_caption": (
            "Air quality is fetched separately and may lag the weather forecast by up "
            "to an hour."
        ),
        # Ladder
        "ladder_title": "Temperature ladder",
        "ladder_sub": "Warmest and coldest of the {count} cities shown.",
        "ladder_warm": "🔥 Warmest",
        "ladder_cold": "🧊 Coldest",
        "ladder_foot": "Click any city card above for its full forecast.",
        # Sun & air
        "sun_title": "🌅 Sun & daylight",
        "sun_sub": "Today's solar window in {condition} skies",
        "sunrise": "Sunrise",
        "sunset": "Sunset",
        "daylight": "Daylight",
        "daylight_value": "{hours:.1f} hours",
        "uv_peak": "UV peak",
        "air_title": "🍃 Air quality",
        "air_sub": "European AQI · updated hourly",
        "air_us": "US AQI {aqi} · {time} CST",
        "air_unavailable": "Air quality data is unavailable right now.",
        "air_still_live": "The forecast above is still live.",
        # Chart copy
        "chart_rain_chance": "Rain chance",
        "chart_temperature": "Temperature",
        "chart_feels": "Feels like",
        "chart_humidity": "Humidity",
        "chart_wind": "Wind",
        "chart_rain": "Rain",
        "chart_temp_axis": "Temperature ({unit})",
        "chart_now": "Now",
        "chart_high": "H",
        "chart_low": "L",
        # Footer
        "footer_demo": "Demo data",
        "footer_live": "Live Open-Meteo data",
        "footer_line": (
            "Data: <b>{mode}</b> · Updated {updated} CST · Cached for 10 minutes"
        ),
        "footer_built": "Built with <b>Streamlit</b> + <b>Plotly</b> · 中国城市天气",
        # Condition / index labels
        "aqi_good": "Good",
        "aqi_fair": "Fair",
        "aqi_moderate": "Moderate",
        "aqi_poor": "Poor",
        "aqi_very_poor": "Very poor",
        "aqi_extremely_poor": "Extremely poor",
        "uv_low": "Low",
        "uv_moderate": "Moderate",
        "uv_high": "High",
        "uv_very_high": "Very high",
        "uv_extreme": "Extreme",
    },
    "zh": {
        # Page / sidebar
        "page_title": "中国城市天气 · China Weather Atlas",
        "brand_title": "中国城市天气",
        "brand_subtitle": "图鉴 · CHINA WEATHER ATLAS",
        "side_copy": "覆盖全国主要城市的实时天气与预报，从东北边陲到热带南国。",
        "language_label": "语言",
        "language_button": "🌐 English",
        "temperature_unit": "温度单位",
        "search_cities": "搜索城市",
        "search_placeholder": "北京、上海、成都…",
        "regions": "地区",
        "all_regions": "全部地区",
        "source": "数据源",
        "cities": "城市数",
        "updated": "更新时间",
        "cst": "北京时间",
        "cache": "缓存",
        "cache_value": "10 分钟",
        "status_live": "实时 · Open-Meteo",
        "status_demo": "演示数据",
        "refresh": "↻ 刷新实时数据",
        "surprise": "🎲 随机看看",
        "side_footer": (
            '数据来自 <a href="https://open-meteo.com/" target="_blank">Open-Meteo</a>。'
            "预报覆盖未来 24 小时与 7 天。"
        ),
        "about_title": "关于本看板",
        "about_body": (
            "**35 座主要城市**，一个看板。\n\n"
            "- 点击任意城市卡片查看详细预报\n"
            "- 可随时切换温度单位与界面语言\n"
            "- 数据每 10 分钟刷新，离线时提供演示数据\n"
            "- 空气质量来自 Open-Meteo 空气质量 API"
        ),
        # Alerts
        "demo_title": "当前显示演示天气。",
        "demo_body": (
            "暂时无法连接 Open-Meteo 实时数据，本页使用逼真的离线演示数据。"
            "请稍后刷新。"
        ),
        "technical_details": "技术详情",
        # Hero
        "hero_kicker": "中国城市天气 · China Weather Atlas",
        "hero_title": '看遍<span class="grad">中国</span>，<br/>一城一天气。',
        "hero_sub": (
            "覆盖 {city_count} 座主要城市的实时预报——从哈尔滨的冰霜到三亚的热带海风。"
            "点击城市卡片，查看当前天气、未来 24 小时、7 天趋势、空气质量与地图。"
        ),
        "hero_live": "实时数据",
        "hero_demo": "演示数据",
        "hero_timezone": "中国标准时间",
        "hero_cities": "座城市",
        # Stats
        "stat_hottest": "当前最热",
        "stat_coldest": "当前最冷",
        "stat_wettest": "降雨概率最高",
        "stat_coverage": "实时覆盖",
        "stat_feels": "体感 {temp}",
        "stat_low_tonight": "今夜最低 {temp}",
        "stat_max_prob": "今日最高概率",
        "stat_coverage_sub": "Open-Meteo · 每 10 分钟刷新",
        # Overview
        "major_title": "主要城市",
        "major_sub": "点击城市卡片，查看当前天气与预报。",
        "major_note": "{count} 座城市 · {time} 北京时间",
        "help_open_city": "查看{city}的天气预报",
        "map_title": "天气地图",
        "map_sub": "圆点颜色代表当前气温，悬停可查看今日温度范围。",
        "map_sub_filtered": "圆点颜色展示全国当前气温。",
        "map_note": "Open-Meteo · 亚洲/上海",
        "cities_title": "城市",
        "cities_sub": "显示 {visible}/{total} 座城市 · {note}。点击卡片查看详情。",
        "filter_search_note": "搜索“{query}”",
        "filter_regions_note": "{count} 个地区",
        "filter_all_note": "全部城市",
        "no_match": "没有匹配的城市，请尝试其他名称或清除地区筛选。",
        # Detail
        "back": "← 所有城市",
        "crumb": "中国{region} · {province}",
        "chip_feels": "体感 <b>{temp}</b>",
        "chip_high_low": "最高 <b>{high}</b> / 最低 <b>{low}</b>",
        "chip_humidity": "💧 湿度 <b>{value}%</b>",
        "chip_wind": "💨 <b>{value} km/h</b> {direction}",
        "chip_rain": "🌧️ 降雨概率 <b>{value}%</b>",
        "now_updated": "更新于 {time} 北京时间 · {condition}",
        # Alerts
        "alert_storm_title": "附近有雷暴",
        "alert_storm_body": "可能出现雷电和强阵雨，外出前请关注当地预警。",
        "alert_heat_title": "高温预警",
        "alert_heat_body": "今日最高气温将达 {temp}，请及时补水并避免正午暴晒。",
        "alert_hot_title": "天气炎热",
        "alert_hot_body": "今日最高气温 {temp}，建议将户外活动安排在早晚。",
        "alert_cold_title": "注意保暖",
        "alert_cold_body": "今夜最低气温降至 {temp}，风寒效应会更冷。",
        "alert_rain_title": "可能有雨",
        "alert_rain_body": "今日降水概率 {rain}%，建议随身带伞。",
        "alert_wind_title": "大风天气",
        "alert_wind_body": "预计阵风可达 {wind} km/h，请固定好户外物品。",
        "alert_aqi_title": "空气质量：{label}",
        "alert_aqi_body": "欧洲 AQI 为 {aqi}，建议减少剧烈户外活动。",
        # Metrics
        "metric_feels": "体感温度",
        "metric_actual": "实际 {temp}",
        "metric_humidity": "湿度",
        "metric_relative_humidity": "相对湿度",
        "metric_wind": "风速",
        "metric_from": "来自 {direction} · {degrees}°",
        "metric_pressure": "气压",
        "metric_surface_pressure": "地面气压",
        "metric_visibility": "能见度",
        "metric_horizontal_visibility": "水平能见度",
        "metric_uv": "紫外线指数",
        "metric_uv_sub": "{label}强度",
        "metric_rain": "降雨概率",
        "metric_rain_sub": "今日最高",
        "metric_air": "空气质量",
        # Forecast / tabs
        "daily_title": "未来七天",
        "daily_sub": "{city}每日最高/最低气温与降雨概率。",
        "daily_note": "更新于 {time} 北京时间",
        "day_today": "今天",
        "no_daily": "暂无每日预报数据。",
        "tab_hourly": "📈 未来 24 小时",
        "tab_map": "🗺️ 天气地图",
        "tab_sun": "🌅 日出与空气",
        "hourly_title": "未来 24 小时预报",
        "hourly_sub": "气温与降雨概率，阴影部分表示夜间。",
        "hourly_caption": (
            "悬停图表可查看体感温度、湿度、风速和降水量，青色圆点表示当前时刻。"
        ),
        "map_tab_title": "{city}的位置",
        "map_tab_sub": "金色星标代表{city}，所有城市按当前气温着色。",
        "sun_tab_title": "日照与空气",
        "sun_tab_sub": "今日日照时段与最新空气质量。",
        "sun_tab_caption": "空气质量为独立获取，可能比天气预报延迟最多一小时。",
        # Ladder
        "ladder_title": "气温阶梯",
        "ladder_sub": "展示城市中最热与最冷的 {count} 座。",
        "ladder_warm": "🔥 最热",
        "ladder_cold": "🧊 最冷",
        "ladder_foot": "点击上方城市卡片查看完整预报。",
        # Sun & air
        "sun_title": "🌅 日出与日照",
        "sun_sub": "今日{condition}天气下的日照时段",
        "sunrise": "日出",
        "sunset": "日落",
        "daylight": "日照时长",
        "daylight_value": "{hours:.1f} 小时",
        "uv_peak": "紫外线峰值",
        "air_title": "🍃 空气质量",
        "air_sub": "欧洲 AQI · 每小时更新",
        "air_us": "美国 AQI {aqi} · {time} 北京时间",
        "air_unavailable": "暂时无法获取空气质量数据。",
        "air_still_live": "上方天气预报仍然可用。",
        # Chart copy
        "chart_rain_chance": "降雨概率",
        "chart_temperature": "气温",
        "chart_feels": "体感",
        "chart_humidity": "湿度",
        "chart_wind": "风速",
        "chart_rain": "降水",
        "chart_temp_axis": "气温（{unit}）",
        "chart_now": "当前",
        "chart_high": "最高",
        "chart_low": "最低",
        # Footer
        "footer_demo": "演示数据",
        "footer_live": "Open-Meteo 实时数据",
        "footer_line": "数据：<b>{mode}</b> · 更新于 {updated} 北京时间 · 缓存 10 分钟",
        "footer_built": "基于 <b>Streamlit</b> + <b>Plotly</b> · 中国城市天气",
        # Condition / index labels
        "aqi_good": "优",
        "aqi_fair": "良",
        "aqi_moderate": "中度",
        "aqi_poor": "较差",
        "aqi_very_poor": "很差",
        "aqi_extremely_poor": "极差",
        "uv_low": "低",
        "uv_moderate": "中等",
        "uv_high": "高",
        "uv_very_high": "很高",
        "uv_extreme": "极高",
    },
}


def normalize_language(lang: str | None) -> str:
    return lang if lang in STRINGS else DEFAULT_LANGUAGE


def t(key: str, lang: str = DEFAULT_LANGUAGE, **values: object) -> str:
    """Return localized copy for ``key``, formatting optional placeholders."""

    lang = normalize_language(lang)
    template = STRINGS[lang].get(key) or STRINGS[DEFAULT_LANGUAGE].get(key) or key
    if not values:
        return template
    try:
        return template.format(**values)
    except (KeyError, IndexError, ValueError):
        return template


def region_label(region: str, lang: str = DEFAULT_LANGUAGE) -> str:
    if normalize_language(lang) == "zh":
        return REGION_LABELS.get(region, region)
    return region


def province_label(province: str, lang: str = DEFAULT_LANGUAGE) -> str:
    if normalize_language(lang) == "zh":
        return PROVINCE_LABELS.get(province, province)
    return province


def condition_label(info: dict, lang: str = DEFAULT_LANGUAGE) -> str:
    """Pick the Chinese or English label from a weather-code info dict."""

    key = "label_zh" if normalize_language(lang) == "zh" else "label_en"
    return info.get(key) or info.get("label_en") or ""


def format_date(moment: datetime, lang: str = DEFAULT_LANGUAGE) -> str:
    if normalize_language(lang) == "zh":
        return (
            f"{moment.year}年{moment.month}月{moment.day}日 "
            f"{_WEEKDAYS_ZH[moment.weekday()]}"
        )
    return moment.strftime("%A, %B %d, %Y")


def weekday_short(moment: datetime, lang: str = DEFAULT_LANGUAGE) -> str:
    if normalize_language(lang) == "zh":
        return _WEEKDAYS_ZH_SHORT[moment.weekday()]
    return _WEEKDAYS_EN_SHORT[moment.weekday()]


def month_day(moment: datetime, lang: str = DEFAULT_LANGUAGE) -> str:
    if normalize_language(lang) == "zh":
        return f"{moment.month}月{moment.day}日"
    return moment.strftime("%b %d")


def wind_direction_name(degrees: float | int, lang: str = DEFAULT_LANGUAGE) -> str:
    index = int((float(degrees) % 360) / 22.5 + 0.5) % 16
    return (_WIND_ZH if normalize_language(lang) == "zh" else _WIND_EN)[index]
