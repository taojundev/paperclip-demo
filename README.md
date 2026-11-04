# China Weather Atlas · 中国城市天气图鉴

一个精致的 Streamlit 天气仪表盘，实时展示**中国 35 个主要城市**的天气——从哈尔滨的
冰霜到三亚的热带微风。点击任意城市卡片，即可打开完整预报。

![中国城市天气图鉴概览](docs/overview.webp)

## 功能亮点

- **35 座城市**，覆盖八大区域，每座城市都包含当前天气、今日最高/最低气温、湿度和
  降水概率。
- **点击进入城市详情页**：主天气信息、八项实时指标、未来 7 天预报条、24 小时
  气温/降水图表、标注所选城市的地图，以及日出/日落和空气质量。
- **可交互的中国地图**（Plotly），按当前气温着色，并配有最暖/最冷城市温度阶梯。
- **智能筛选**——支持中英文搜索、按区域筛选、在 °C 和 °F 之间切换、在**中文与
  English** 之间切换整个界面、在**浅色与深色主题**之间切换，还可以点“随机推荐”
  来抽取一座城市。
- **深链接**——每座城市都有形如 `/?city=shanghai` 的 URL；返回按钮可回到城市网格。
- **内置容错**——Open-Meteo 实时数据会缓存 10 分钟；网络不可用时，应用会回退到
  确定性的、贴近真实的演示预报。
- **精美的玻璃拟态 UI**——打磨过的深色与浅色主题、随气温变化的渐变、随天气变化的
  图标、响应式布局、双语标签，以及内置的 emoji 字体，即使机器没有系统 emoji 字体
  也能正常显示图标。

| 详情页 | 地图与温度阶梯 |
| --- | --- |
| ![上海详情页](docs/detail.webp) | ![天气地图](docs/map.webp) |

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

然后打开 <http://localhost:8501>。无需 API 密钥。

## 项目结构

```
app.py                       Streamlit 入口与页面路由
weather_dashboard/
  cities.py                  城市目录 + WMO 天气代码元数据
  api.py                     Open-Meteo 请求、数据归一化、演示数据回退
  components.py              HTML 片段与跟随主题的 Plotly 图表
  styles.py                  全局 CSS（深色基础 + 浅色主题、卡片、响应式规则）
  i18n.py                    中英文文案、日期与区域名称
static/emoji.woff2           UI 使用的 Noto Color Emoji 子集
.streamlit/config.toml       深色主题 + 静态文件服务
tests/                       离线单元测试 + 无头 AppTest 冒烟测试
```

## 数据来源

- 预报：[Open-Meteo](https://open-meteo.com/)——当前天气、逐小时和未来 7 天数据
  （`Asia/Shanghai` 时区）。
- 空气质量：Open-Meteo Air Quality API（欧洲 AQI、PM2.5、PM10、O₃、NO₂）。
- 响应会缓存 10 分钟（`st.cache_data`）；点击“刷新实时数据”可清除缓存。请求失败
  时，应用会显示一份明确标注的演示数据集，而不是错误页面。

## 测试

```bash
python -m pytest
```

测试覆盖数据归一化、离线回退、HTML 片段回归（空行会破坏 Streamlit 的 markdown
HTML 块）、主题配色，并通过 `streamlit.testing.v1.AppTest` 无头驱动应用：概览、
搜索/筛选、单位切换、语言与主题切换、城市导航以及返回。

## 说明

- 内置的 `static/emoji.woff2` 是
  [Noto Color Emoji](https://fonts.google.com/noto/specimen/Noto+Color+Emoji)
  的 33 字形子集，采用 SIL Open Font License 1.1 授权（见
  `static/OFL-NotoColorEmoji.txt`）。它通过 Streamlit 的静态文件服务提供
  （`server.enableStaticServing = true`）。
- 天气图标使用 Open-Meteo 返回的 WMO 解释代码。
