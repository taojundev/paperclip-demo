"""Global CSS for the glassy weather dashboard (dark and light themes)."""

from __future__ import annotations

THEMES = ("dark", "light")
DEFAULT_THEME = "dark"

CSS = r"""
<style>
/* Tiny subset (84 kB) of Noto Color Emoji so condition icons render
even on machines without a system emoji font. */
@font-face {
    font-family: "App Emoji";
    src: url("app/static/emoji.woff2") format("woff2");
    font-weight: 400;
    font-style: normal;
    font-display: swap;
}

:root {
    --bg: #060912;
    --bg-2: #0a1024;
    --panel: rgba(17, 24, 48, 0.72);
    --panel-strong: rgba(21, 29, 58, 0.9);
    --stroke: rgba(148, 163, 255, 0.14);
    --stroke-strong: rgba(148, 163, 255, 0.28);
    --text: #eef2ff;
    --muted: #96a2c8;
    --faint: #6c789e;
    --accent: #7c9bff;
    --accent-2: #6ee7d8;
    --warm: #ffb86b;
    --danger: #ff7a8a;
    --shadow: 0 24px 70px rgba(0, 0, 0, 0.42);
}

html, body, [class*="css"], .stApp,
button, input, textarea, select,
h1, h2, h3, h4, h5, h6,
[data-testid="stMarkdownContainer"], [data-testid="stWidgetLabel"],
[data-testid="stCaptionContainer"] {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI",
        "PingFang SC", "Hiragino Sans GB", "Noto Sans SC", "Microsoft YaHei",
        "App Emoji", "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji",
        sans-serif;
}

.stApp {
    background:
        radial-gradient(1100px 680px at 8% -8%, rgba(96, 76, 255, 0.20), transparent 62%),
        radial-gradient(900px 620px at 100% 0%, rgba(31, 190, 190, 0.14), transparent 60%),
        radial-gradient(900px 700px at 50% 110%, rgba(68, 90, 220, 0.14), transparent 62%),
        linear-gradient(180deg, #060912 0%, #070b18 46%, #050811 100%);
    color: var(--text);
}

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background-image:
        linear-gradient(rgba(148, 163, 255, 0.028) 1px, transparent 1px),
        linear-gradient(90deg, rgba(148, 163, 255, 0.028) 1px, transparent 1px);
    background-size: 64px 64px;
    mask-image: radial-gradient(circle at 50% 20%, black, transparent 78%);
    -webkit-mask-image: radial-gradient(circle at 50% 20%, black, transparent 78%);
    z-index: 0;
}

[data-testid="stHeader"] {
    background: transparent;
    height: 0;
}
[data-testid="stToolbar"], [data-testid="stDecoration"], #MainMenu, footer {
    visibility: hidden;
    height: 0;
}
[data-testid="stStatusWidget"] { display: none; }

.block-container {
    position: relative;
    z-index: 1;
    max-width: 1520px;
    padding: 1.35rem 2.6rem 4.5rem;
}

/* ------------------------------------------------------------------ hero */
.hero {
    position: relative;
    overflow: hidden;
    border: 1px solid var(--stroke);
    border-radius: 30px;
    padding: 38px 42px 34px;
    background:
        radial-gradient(620px 300px at 92% -10%, rgba(110, 231, 216, 0.16), transparent 60%),
        radial-gradient(700px 360px at 0% 120%, rgba(124, 155, 255, 0.18), transparent 62%),
        linear-gradient(122deg, rgba(23, 31, 64, 0.94), rgba(12, 17, 38, 0.82));
    box-shadow: var(--shadow), inset 0 1px 0 rgba(255, 255, 255, 0.05);
    animation: rise 0.55s cubic-bezier(0.22, 1, 0.36, 1) both;
}
.hero::after {
    content: "";
    position: absolute;
    width: 260px;
    height: 260px;
    right: -60px;
    top: -90px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(110, 231, 216, 0.24), transparent 68%);
    filter: blur(6px);
    animation: float 9s ease-in-out infinite;
    pointer-events: none;
}
.hero-kicker {
    display: inline-flex;
    align-items: center;
    gap: 9px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    font-size: 0.68rem;
    font-weight: 700;
    color: #9fb1ff;
}
.hero-kicker .dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #6ee7b7;
    box-shadow: 0 0 0 4px rgba(110, 231, 183, 0.14), 0 0 16px rgba(110, 231, 183, 0.8);
}
.hero h1 {
    margin: 0.55rem 0 0.55rem;
    font-size: clamp(2.15rem, 4.1vw, 3.7rem);
    line-height: 1.03;
    letter-spacing: -0.035em;
    font-weight: 800;
}
.hero h1 .grad {
    background: linear-gradient(94deg, #ffffff 4%, #b7c6ff 42%, #6ee7d8 92%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
.hero-sub {
    max-width: 760px;
    margin: 0;
    color: #aab5d8;
    font-size: 0.98rem;
    line-height: 1.65;
}
.hero-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 9px;
    margin-top: 22px;
}
.pill {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 7px 13px;
    border-radius: 999px;
    border: 1px solid rgba(148, 163, 255, 0.17);
    background: rgba(255, 255, 255, 0.045);
    color: #c8d2f2;
    font-size: 0.77rem;
    font-weight: 500;
    backdrop-filter: blur(8px);
}
.pill strong { color: #fff; font-weight: 650; }
.pill .live-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #4ade80;
    box-shadow: 0 0 8px rgba(74, 222, 128, 0.9);
}
.pill .demo-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #fbbf24;
    box-shadow: 0 0 8px rgba(251, 191, 36, 0.8);
}

/* ----------------------------------------------------------------- stats */
.stats {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 13px;
    margin: 16px 0 4px;
}
.stat {
    display: flex;
    align-items: center;
    gap: 13px;
    padding: 14px 16px;
    border-radius: 18px;
    border: 1px solid var(--stroke);
    background: linear-gradient(150deg, rgba(24, 32, 62, 0.76), rgba(12, 17, 37, 0.72));
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04);
    animation: rise 0.55s cubic-bezier(0.22, 1, 0.36, 1) both;
}
.stat-icon {
    width: 40px;
    height: 40px;
    flex: 0 0 40px;
    display: grid;
    place-items: center;
    border-radius: 13px;
    background: rgba(124, 155, 255, 0.12);
    border: 1px solid rgba(124, 155, 255, 0.2);
    font-size: 1.15rem;
}
.stat-label {
    font-size: 0.62rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--faint);
    font-weight: 700;
}
.stat-value {
    margin-top: 2px;
    font-size: 1.06rem;
    font-weight: 700;
    line-height: 1.25;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.stat-sub { font-size: 0.72rem; color: var(--muted); margin-top: 1px; }

/* --------------------------------------------------------------- section */
.section-head {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 18px;
    margin: 30px 0 12px;
}
.section-head h2 {
    margin: 0;
    font-size: 1.12rem;
    letter-spacing: -0.01em;
    font-weight: 700;
}
.section-head p { margin: 4px 0 0; color: var(--muted); font-size: 0.82rem; }
.section-note { color: var(--faint); font-size: 0.75rem; white-space: nowrap; }

/* ------------------------------------------------------------ city cards */
.stButton > button {
    min-height: 74px;
    padding: 13px 15px;
    border-radius: 17px;
    border: 1px solid rgba(148, 163, 255, 0.16);
    background: linear-gradient(152deg, rgba(26, 34, 66, 0.92), rgba(12, 17, 37, 0.86));
    color: #eef2ff;
    font-weight: 600;
    text-align: left;
    justify-content: flex-start;
    transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease,
        background 0.18s ease;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.045);
}
.stButton > button p {
    margin: 0;
    font-size: 0.94rem;
    line-height: 1.42;
    font-weight: 600;
    white-space: pre-line;
    text-align: left;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-3px);
    border-color: rgba(148, 163, 255, 0.42);
    box-shadow: 0 16px 38px rgba(5, 9, 24, 0.55), inset 0 1px 0 rgba(255, 255, 255, 0.08);
    color: #fff;
}
.stButton > button:active { transform: translateY(-1px); }
.stButton > button:focus:not(:active) {
    border-color: rgba(110, 231, 216, 0.65);
    box-shadow: 0 0 0 3px rgba(110, 231, 216, 0.14);
    color: #fff;
}
.city-foot {
    margin: 7px 4px 15px;
    color: var(--faint);
    font-size: 0.7rem;
    letter-spacing: 0.01em;
    display: flex;
    justify-content: space-between;
    gap: 8px;
    white-space: nowrap;
}
.city-foot span:last-child { color: #aab5d8; }

/* -------------------------------------------------------------- detail */
.back-btn button,
.st-key-back_btn button {
    min-height: 0 !important;
    padding: 8px 14px !important;
    border-radius: 11px !important;
    background: rgba(255, 255, 255, 0.04) !important;
}
.back-btn button p,
.st-key-back_btn button p { font-size: 0.8rem !important; }
.st-key-back_btn { margin-bottom: 12px; }

.detail-hero {
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: stretch;
    justify-content: space-between;
    gap: 28px;
    padding: 34px 40px;
    border-radius: 30px;
    border: 1px solid var(--stroke);
    background:
        radial-gradient(560px 300px at 88% -20%, var(--glow, rgba(124, 155, 255, 0.25)), transparent 64%),
        radial-gradient(620px 320px at 0% 130%, rgba(110, 231, 216, 0.12), transparent 66%),
        linear-gradient(124deg, rgba(24, 32, 66, 0.95), rgba(11, 16, 36, 0.86));
    box-shadow: var(--shadow), inset 0 1px 0 rgba(255, 255, 255, 0.05);
    animation: rise 0.5s cubic-bezier(0.22, 1, 0.36, 1) both;
}
.detail-hero::after {
    content: "";
    position: absolute;
    width: 340px;
    height: 340px;
    right: -100px;
    bottom: -190px;
    border-radius: 50%;
    background: radial-gradient(circle, var(--glow, rgba(124, 155, 255, 0.3)), transparent 68%);
    filter: blur(4px);
    pointer-events: none;
}
.crumb {
    color: #93a2cf;
    font-size: 0.68rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    font-weight: 700;
}
.detail-hero h1 {
    margin: 9px 0 4px;
    font-size: clamp(2rem, 3.3vw, 3rem);
    letter-spacing: -0.035em;
    line-height: 1.05;
    font-weight: 800;
}
.detail-hero h1 span {
    font-size: 0.46em;
    color: #9fadd6;
    font-weight: 600;
    letter-spacing: 0;
    margin-left: 6px;
}
.detail-cond {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: #d5defb;
    font-size: 1rem;
    margin-top: 7px;
}
.detail-cond .zh { color: #fff; font-weight: 650; }
.detail-cond .en { color: var(--muted); }
.detail-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 18px; }
.chip {
    padding: 7px 12px;
    border-radius: 10px;
    border: 1px solid rgba(148, 163, 255, 0.16);
    background: rgba(255, 255, 255, 0.045);
    color: #c6d1f4;
    font-size: 0.76rem;
}
.chip b { color: #fff; font-weight: 650; }
.now-panel {
    position: relative;
    z-index: 1;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    justify-content: center;
    min-width: 210px;
    text-align: right;
}
.now-emoji {
    font-size: clamp(2.7rem, 5vw, 4.1rem);
    line-height: 1;
    filter: drop-shadow(0 10px 26px rgba(0, 0, 0, 0.45));
    animation: float 7s ease-in-out infinite;
}
.temp-now {
    font-size: clamp(3.8rem, 8vw, 6.3rem);
    line-height: 0.92;
    font-weight: 800;
    letter-spacing: -0.055em;
    margin-top: 4px;
    background: linear-gradient(180deg, #ffffff 20%, #b9c8ff 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
.temp-now sup {
    font-size: 0.32em;
    letter-spacing: 0;
    vertical-align: super;
    color: #9fb1ff;
    -webkit-text-fill-color: #9fb1ff;
}
.updated { color: var(--faint); font-size: 0.72rem; margin-top: 6px; }

/* ----------------------------------------------------------- alerts */
.alert {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin-top: 12px;
    padding: 13px 17px;
    border-radius: 15px;
    border: 1px solid var(--alert-border, rgba(251, 191, 36, 0.3));
    background: var(--alert-bg, rgba(251, 191, 36, 0.08));
    color: #f3e7c8;
    font-size: 0.84rem;
    line-height: 1.5;
}
.alert .a-icon { font-size: 1.05rem; line-height: 1.4; }
.alert b { color: #fff; }
.alert.danger { --alert-border: rgba(255, 122, 138, 0.34); --alert-bg: rgba(255, 122, 138, 0.09); color: #ffd6dc; }
.alert.info { --alert-border: rgba(124, 155, 255, 0.32); --alert-bg: rgba(124, 155, 255, 0.09); color: #dbe3ff; }

/* ---------------------------------------------------------- metrics */
.metrics {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 11px;
    margin: 14px 0 4px;
}
.metric {
    padding: 14px 15px;
    border-radius: 16px;
    border: 1px solid var(--stroke);
    background: linear-gradient(152deg, rgba(22, 30, 58, 0.78), rgba(11, 16, 35, 0.74));
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04);
    animation: rise 0.5s cubic-bezier(0.22, 1, 0.36, 1) both;
}
.m-top { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
.m-label {
    color: var(--faint);
    font-size: 0.63rem;
    letter-spacing: 0.11em;
    text-transform: uppercase;
    font-weight: 700;
}
.m-icon { font-size: 0.92rem; opacity: 0.8; }
.m-value {
    margin-top: 5px;
    font-size: 1.32rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    line-height: 1.2;
}
.m-value small { font-size: 0.48em; color: var(--muted); font-weight: 600; margin-left: 2px; }
.m-sub { margin-top: 3px; color: var(--muted); font-size: 0.7rem; }
.m-bar { height: 4px; border-radius: 99px; background: rgba(148, 163, 255, 0.13); margin-top: 9px; overflow: hidden; }
.m-bar span { display: block; height: 100%; border-radius: 99px; background: linear-gradient(90deg, var(--accent), var(--accent-2)); }

/* ------------------------------------------------------------ daily */
.forecast-strip {
    display: grid;
    grid-template-columns: repeat(7, minmax(0, 1fr));
    gap: 9px;
    margin-top: 4px;
}
.day-card {
    position: relative;
    padding: 14px 9px 12px;
    border-radius: 17px;
    border: 1px solid var(--stroke);
    background: linear-gradient(170deg, rgba(23, 31, 60, 0.78), rgba(10, 15, 33, 0.8));
    text-align: center;
    transition: transform 0.18s ease, border-color 0.18s ease;
}
.day-card:hover { transform: translateY(-3px); border-color: var(--stroke-strong); }
.day-card.today {
    border-color: rgba(110, 231, 216, 0.36);
    background:
        radial-gradient(160px 90px at 50% 0%, rgba(110, 231, 216, 0.14), transparent 70%),
        linear-gradient(170deg, rgba(27, 42, 72, 0.88), rgba(11, 17, 36, 0.85));
}
.day-name { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.04em; }
.day-date { color: var(--faint); font-size: 0.62rem; margin-top: 1px; }
.day-icon { font-size: 1.65rem; line-height: 1.35; margin-top: 6px; filter: drop-shadow(0 4px 10px rgba(0,0,0,.35)); }
.day-cond { color: var(--muted); font-size: 0.6rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.day-temps { margin-top: 5px; font-size: 0.82rem; font-weight: 650; }
.day-temps .lo { color: var(--faint); font-weight: 500; }
.day-range { position: relative; height: 4px; border-radius: 99px; background: rgba(148, 163, 255, 0.13); margin: 7px 3px 0; }
.day-range span {
    position: absolute;
    top: 0;
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, #6ee7ff, #ffd06b 68%, #ff8e72);
}
.day-rain { color: #8fc8ff; font-size: 0.62rem; margin-top: 5px; }

/* ------------------------------------------------------------- tabs */
.stTabs [data-baseweb="tab-list"],
.stTabs [role="tablist"] {
    gap: 5px;
    padding: 5px;
    border-radius: 14px;
    border: 1px solid var(--stroke);
    background: rgba(12, 17, 37, 0.7);
    width: fit-content;
}
.stTabs [data-baseweb="tab"],
.stTabs [role="tab"] {
    height: auto;
    padding: 8px 16px;
    border-radius: 10px;
    color: var(--muted);
    font-size: 0.8rem;
    font-weight: 600;
}
.stTabs [data-baseweb="tab"]:hover,
.stTabs [role="tab"]:hover { color: #fff; background: rgba(255, 255, 255, 0.04); }
.stTabs [aria-selected="true"] {
    color: #fff !important;
    background: linear-gradient(135deg, rgba(124, 155, 255, 0.22), rgba(110, 231, 216, 0.12));
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"],
.stTabs .react-aria-SelectionIndicator { display: none; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 14px; }
/* Streamlit's tab labels need the emoji font explicitly. */
.stTabs [role="tab"] p,
.stTabs [data-testid="stTab"] p {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI",
        "PingFang SC", "Hiragino Sans GB", "Noto Sans SC", "Microsoft YaHei",
        "App Emoji", "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji",
        sans-serif;
    font-size: 0.8rem;
    margin: 0;
}

/* ------------------------------------------------------ sun + air */
.duo { display: grid; grid-template-columns: 1fr 1fr; gap: 13px; }
.info-card {
    padding: 19px 20px;
    border-radius: 20px;
    border: 1px solid var(--stroke);
    background: linear-gradient(152deg, rgba(23, 31, 60, 0.8), rgba(10, 15, 33, 0.8));
}
.info-card h3 { margin: 0; font-size: 0.92rem; font-weight: 700; }
.info-card .sub { color: var(--muted); font-size: 0.72rem; margin-top: 2px; }
.sun-row { display: flex; justify-content: space-between; margin-top: 18px; }
.sun-item { display: flex; flex-direction: column; gap: 3px; }
.sun-item .k { color: var(--faint); font-size: 0.62rem; letter-spacing: 0.1em; text-transform: uppercase; }
.sun-item .v { font-size: 1rem; font-weight: 650; }
.sun-track {
    position: relative;
    height: 8px;
    margin: 20px 4px 4px;
    border-radius: 99px;
    background: linear-gradient(90deg, rgba(124, 155, 255, 0.3), rgba(255, 184, 107, 0.55), rgba(255, 122, 138, 0.35));
}
.sun-track .sun-dot {
    position: absolute;
    top: 50%;
    width: 15px;
    height: 15px;
    border-radius: 50%;
    transform: translate(-50%, -50%);
    background: radial-gradient(circle at 35% 30%, #fff6cf, #ffb86b 60%, #ff8e72);
    box-shadow: 0 0 18px rgba(255, 184, 107, 0.9), 0 0 0 4px rgba(255, 184, 107, 0.14);
}
.aqi-head { display: flex; align-items: flex-end; justify-content: space-between; gap: 12px; margin-top: 12px; }
.aqi-value { font-size: 2.4rem; font-weight: 800; letter-spacing: -0.04em; line-height: 1; }
.aqi-tag {
    padding: 5px 10px;
    border-radius: 999px;
    font-size: 0.68rem;
    font-weight: 700;
    border: 1px solid currentColor;
    background: rgba(255, 255, 255, 0.04);
}
.pollutant { margin-top: 10px; }
.p-row { display: flex; justify-content: space-between; color: var(--muted); font-size: 0.7rem; margin-bottom: 3px; }
.p-row b { color: #dfe6ff; font-weight: 600; }
.p-bar { height: 4px; border-radius: 99px; background: rgba(148, 163, 255, 0.13); overflow: hidden; }
.p-bar span { display: block; height: 100%; border-radius: 99px; }

/* --------------------------------------------------- map + ladder */
.map-side {
    box-sizing: border-box;
    height: 100%;
    min-height: 470px;
    padding: 20px 20px 14px;
    border-radius: 20px;
    border: 1px solid var(--stroke);
    background: linear-gradient(152deg, rgba(23, 31, 60, 0.82), rgba(10, 15, 33, 0.85));
    display: flex;
    flex-direction: column;
}
.map-side-head h3 { margin: 0; font-size: 0.92rem; font-weight: 700; }
.map-side-head p { margin: 3px 0 0; color: var(--muted); font-size: 0.72rem; }
.ladder-label {
    display: flex;
    justify-content: space-between;
    margin: 14px 0 3px;
    color: var(--faint);
    font-size: 0.6rem;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    font-weight: 700;
}
.ladder-label.cold {
    margin-top: 13px;
    padding-top: 12px;
    border-top: 1px solid rgba(148, 163, 255, 0.1);
}
.ladder-row {
    display: grid;
    grid-template-columns: 22px 1fr auto;
    align-items: center;
    column-gap: 8px;
    padding: 4px 0;
}
.ladder-rank { color: var(--faint); font-size: 0.6rem; font-variant-numeric: tabular-nums; }
.ladder-name {
    min-width: 0;
    font-size: 0.78rem;
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.ladder-name small {
    display: block;
    color: var(--faint);
    font-size: 0.62rem;
    font-weight: 500;
    line-height: 1.35;
}
.ladder-val { font-size: 0.86rem; font-weight: 700; font-variant-numeric: tabular-nums; }
.ladder-bar {
    grid-column: 2 / -1;
    height: 3px;
    margin-top: 1px;
    border-radius: 99px;
    background: rgba(148, 163, 255, 0.1);
    overflow: hidden;
}
.ladder-bar i { display: block; height: 100%; border-radius: 99px; opacity: 0.8; }
.map-side-foot { margin-top: auto; padding-top: 10px; color: var(--faint); font-size: 0.64rem; }

/* ------------------------------------------------------------- footer */
.app-footer {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    gap: 10px;
    margin-top: 34px;
    padding-top: 16px;
    border-top: 1px solid rgba(148, 163, 255, 0.1);
    color: var(--faint);
    font-size: 0.72rem;
}
.app-footer b { color: #aebbe2; font-weight: 600; }

/* ----------------------------------------------------------- sidebar */
[data-testid="stSidebar"] {
    background:
        radial-gradient(420px 300px at 50% -8%, rgba(96, 76, 255, 0.18), transparent 62%),
        linear-gradient(180deg, #0a0f22 0%, #070b17 100%);
    border-right: 1px solid rgba(148, 163, 255, 0.1);
}
[data-testid="stSidebarUserContent"] { padding: 1.6rem 1.1rem 2.5rem; }
.side-brand { display: flex; align-items: center; gap: 11px; margin-bottom: 6px; }
.side-logo {
    width: 42px;
    height: 42px;
    flex: 0 0 42px;
    display: grid;
    place-items: center;
    border-radius: 13px;
    font-size: 1.3rem;
    background: linear-gradient(145deg, rgba(124, 155, 255, 0.28), rgba(110, 231, 216, 0.16));
    border: 1px solid rgba(148, 163, 255, 0.3);
    box-shadow: 0 8px 24px rgba(60, 80, 220, 0.25);
}
.side-title { font-size: 0.98rem; font-weight: 750; line-height: 1.2; letter-spacing: -0.01em; }
.side-title span { display: block; color: var(--faint); font-size: 0.63rem; letter-spacing: 0.13em; text-transform: uppercase; font-weight: 600; margin-top: 2px; }
.side-copy { color: var(--muted); font-size: 0.78rem; line-height: 1.55; margin: 12px 0 18px; }
.side-label {
    color: var(--faint);
    font-size: 0.61rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    font-weight: 700;
    margin: 15px 0 5px;
}
.side-status {
    margin-top: 16px;
    padding: 13px 14px;
    border-radius: 15px;
    border: 1px solid var(--stroke);
    background: rgba(255, 255, 255, 0.035);
    font-size: 0.73rem;
    color: var(--muted);
}
.side-status .row { display: flex; justify-content: space-between; gap: 8px; padding: 3px 0; }
.side-status .row b { color: #e5ebff; font-weight: 600; }
.side-status .live { color: #6ee7b7; }
.side-status .demo { color: #fbbf24; }
.side-foot { margin-top: 20px; color: var(--faint); font-size: 0.66rem; line-height: 1.5; }
.side-foot a { color: #9fb1ff; text-decoration: none; }

[data-testid="stSidebar"] .stButton > button {
    min-height: 0;
    width: 100%;
    justify-content: center;
    text-align: center;
    padding: 9px 12px;
    border-radius: 11px;
    font-size: 0.78rem;
}
[data-testid="stSidebar"] .stButton > button p {
    font-size: 0.78rem;
    text-align: center;
    white-space: normal;
}

/* Theme + language toggles sit above the brand, always one click away. */
.st-key-theme_toggle { margin-bottom: 7px; }
.st-key-lang_toggle { margin-bottom: 12px; }
.st-key-theme_toggle button,
.st-key-lang_toggle button {
    background: linear-gradient(120deg, rgba(124, 155, 255, 0.26), rgba(110, 231, 216, 0.16)) !important;
    border: 1px solid rgba(148, 163, 255, 0.36) !important;
    color: #eef2ff !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em;
}
.st-key-theme_toggle button:hover,
.st-key-lang_toggle button:hover {
    border-color: rgba(110, 231, 216, 0.62) !important;
    box-shadow: 0 8px 22px rgba(60, 80, 220, 0.28);
}
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] > div {
    background: rgba(255, 255, 255, 0.045);
    border-color: rgba(148, 163, 255, 0.16);
    color: var(--text);
    border-radius: 11px;
}
[data-testid="stSidebar"] .stTextInput input::placeholder { color: #6c789e; }
[data-testid="stSidebar"] label p { font-size: 0.73rem; color: #b9c4e6; }
[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: rgba(124, 155, 255, 0.18) !important;
    border-radius: 7px !important;
}
[data-testid="stSidebar"] [data-baseweb="tag"] span { color: #dfe6ff !important; font-size: 0.68rem; }

[data-testid="stExpander"] {
    border: 1px solid var(--stroke);
    border-radius: 13px;
    background: rgba(255, 255, 255, 0.025);
    overflow: hidden;
}
[data-testid="stExpander"] summary { font-size: 0.76rem; color: #b9c4e6; }
[data-testid="stExpander"] p { font-size: 0.74rem; color: var(--muted); }

[data-testid="stAlert"] { border-radius: 13px; }
[data-testid="stPlotlyChart"] {
    border-radius: 20px;
    border: 1px solid var(--stroke);
    background: linear-gradient(152deg, rgba(19, 26, 52, 0.74), rgba(9, 13, 29, 0.72));
    padding: 8px 6px 2px;
    overflow: hidden;
}
[data-testid="stCaptionContainer"] p { color: var(--faint); font-size: 0.72rem; }

/* --------------------------------------------------------- animation */
@keyframes rise {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-9px); }
}

/* -------------------------------------------------------- responsive */
@media (max-width: 1180px) {
    .block-container { padding: 1rem 1.4rem 3.5rem; }
    .stats { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .metrics { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .forecast-strip { grid-template-columns: repeat(4, minmax(0, 1fr)); }
    .duo { grid-template-columns: 1fr; }
}
@media (max-width: 760px) {
    .hero { padding: 26px 22px; border-radius: 22px; }
    .detail-hero { flex-direction: column; padding: 24px 22px; border-radius: 22px; }
    .now-panel { align-items: flex-start; text-align: left; min-width: 0; }
    .temp-now { font-size: 4.2rem; }
    .stats, .metrics { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .forecast-strip { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .section-head { flex-direction: column; align-items: flex-start; gap: 4px; }
    .map-side { min-height: 0; height: auto; }
}
</style>
"""


# The light theme is layered on top of the dark stylesheet: it retunes the
# design tokens and repaints the few surfaces that use literal dark colours.
LIGHT_CSS = r"""<style>
:root {
    --bg: #f6f8ff;
    --bg-2: #eef3fd;
    --panel: rgba(255, 255, 255, 0.86);
    --panel-strong: rgba(255, 255, 255, 0.96);
    --stroke: rgba(59, 78, 140, 0.14);
    --stroke-strong: rgba(59, 78, 140, 0.28);
    --text: #17203a;
    --muted: #5c6a91;
    --faint: #7885a8;
    --accent: #4f6bed;
    --accent-2: #0f9c8f;
    --warm: #c2740b;
    --danger: #d23b53;
    --shadow: 0 22px 60px rgba(40, 58, 120, 0.13);

    /* Streamlit's own widgets inherit these. */
    --background-color: #f6f8ff;
    --secondary-background-color: #ffffff;
    --text-color: #17203a;
    --primary-color: #4f6bed;
}

.stApp {
    background:
        radial-gradient(1100px 680px at 8% -8%, rgba(79, 107, 237, 0.13), transparent 62%),
        radial-gradient(900px 620px at 100% 0%, rgba(15, 156, 143, 0.11), transparent 60%),
        radial-gradient(900px 700px at 50% 110%, rgba(79, 107, 237, 0.09), transparent 62%),
        linear-gradient(180deg, #fbfcff 0%, #f2f6fe 46%, #edf2fb 100%);
    color: var(--text);
}
.stApp::before {
    background-image:
        linear-gradient(rgba(59, 78, 140, 0.045) 1px, transparent 1px),
        linear-gradient(90deg, rgba(59, 78, 140, 0.045) 1px, transparent 1px);
}

/* ------------------------------------------------------------- typography */
.hero-kicker { color: #3f5bd6; }
.hero h1 .grad {
    background: linear-gradient(94deg, #101a35 4%, #2f4ed0 52%, #0f8f84 94%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
.hero-sub { color: #52618a; }
.pill {
    border-color: rgba(59, 78, 140, 0.16);
    background: rgba(255, 255, 255, 0.72);
    color: #44527a;
}
.pill strong { color: #17203a; }
.section-note { color: var(--faint); }
.city-foot { color: var(--faint); }
.city-foot span:last-child { color: #5a6890; }

/* ------------------------------------------------------------------ hero */
.hero {
    background:
        radial-gradient(620px 300px at 92% -10%, rgba(15, 156, 143, 0.13), transparent 60%),
        radial-gradient(700px 360px at 0% 120%, rgba(79, 107, 237, 0.12), transparent 62%),
        linear-gradient(122deg, rgba(255, 255, 255, 0.96), rgba(240, 245, 255, 0.9));
    box-shadow: var(--shadow), inset 0 1px 0 rgba(255, 255, 255, 0.8);
}
.hero::after { background: radial-gradient(circle, rgba(15, 156, 143, 0.18), transparent 68%); }

/* ----------------------------------------------------------- cards / stats */
.stat {
    background: linear-gradient(150deg, rgba(255, 255, 255, 0.96), rgba(242, 246, 255, 0.9));
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.9), 0 10px 28px rgba(40, 58, 120, 0.06);
}
.stat-icon {
    background: rgba(79, 107, 237, 0.10);
    border-color: rgba(79, 107, 237, 0.18);
}
.stButton > button {
    background: linear-gradient(152deg, rgba(255, 255, 255, 0.98), rgba(243, 247, 255, 0.95));
    border-color: rgba(59, 78, 140, 0.16);
    color: #17203a;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.9), 0 8px 20px rgba(40, 58, 120, 0.05);
}
.stButton > button:hover {
    border-color: rgba(79, 107, 237, 0.45);
    box-shadow: 0 16px 34px rgba(40, 58, 120, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.9);
    color: #101a35;
}
.stButton > button:focus:not(:active) {
    border-color: rgba(15, 156, 143, 0.6);
    box-shadow: 0 0 0 3px rgba(15, 156, 143, 0.14);
    color: #101a35;
}

/* ---------------------------------------------------------------- detail */
.detail-hero {
    background:
        radial-gradient(560px 300px at 88% -20%, var(--glow, rgba(79, 107, 237, 0.18)), transparent 64%),
        radial-gradient(620px 320px at 0% 130%, rgba(15, 156, 143, 0.10), transparent 66%),
        linear-gradient(124deg, rgba(255, 255, 255, 0.97), rgba(240, 245, 255, 0.92));
    box-shadow: var(--shadow), inset 0 1px 0 rgba(255, 255, 255, 0.85);
}
.crumb { color: #6070a0; }
.detail-hero h1 span { color: #5a6890; }
.detail-cond { color: #44527a; }
.detail-cond .zh { color: #17203a; }
.chip {
    border-color: rgba(59, 78, 140, 0.16);
    background: rgba(255, 255, 255, 0.8);
    color: #44527a;
}
.chip b { color: #17203a; }
.now-emoji { filter: drop-shadow(0 10px 20px rgba(40, 58, 120, 0.18)); }
.temp-now {
    background: linear-gradient(180deg, #17203a 20%, #4257a8 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
.temp-now sup { color: #3f5bd6; -webkit-text-fill-color: #3f5bd6; }

/* ---------------------------------------------------------------- alerts */
.alert {
    color: #7a5a12;
    --alert-border: rgba(194, 116, 11, 0.26);
    --alert-bg: rgba(251, 191, 36, 0.12);
}
.alert b { color: #17203a; }
.alert.danger {
    --alert-border: rgba(210, 59, 83, 0.28);
    --alert-bg: rgba(210, 59, 83, 0.08);
    color: #a1263b;
}
.alert.info {
    --alert-border: rgba(79, 107, 237, 0.26);
    --alert-bg: rgba(79, 107, 237, 0.08);
    color: #2e45a0;
}

/* --------------------------------------------------------------- metrics */
.metric {
    background: linear-gradient(152deg, rgba(255, 255, 255, 0.96), rgba(242, 246, 255, 0.92));
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.9), 0 8px 22px rgba(40, 58, 120, 0.05);
}
.m-bar, .day-range, .p-bar, .ladder-bar { background: rgba(59, 78, 140, 0.12); }

/* ---------------------------------------------------------------- daily */
.day-card {
    background: linear-gradient(170deg, rgba(255, 255, 255, 0.97), rgba(242, 246, 255, 0.94));
}
.day-card:hover { border-color: var(--stroke-strong); }
.day-card.today {
    border-color: rgba(15, 156, 143, 0.35);
    background:
        radial-gradient(160px 90px at 50% 0%, rgba(15, 156, 143, 0.12), transparent 70%),
        linear-gradient(170deg, rgba(255, 255, 255, 0.98), rgba(238, 247, 249, 0.95));
}
.day-icon { filter: drop-shadow(0 4px 8px rgba(40, 58, 120, 0.16)); }
.day-rain { color: #2f7fd1; }

/* ----------------------------------------------------------------- tabs */
.stTabs [data-baseweb="tab-list"],
.stTabs [role="tablist"] {
    border-color: var(--stroke);
    background: rgba(255, 255, 255, 0.82);
}
.stTabs [data-baseweb="tab"],
.stTabs [role="tab"] { color: #5c6a91; }
.stTabs [data-baseweb="tab"]:hover,
.stTabs [role="tab"]:hover { color: #17203a; background: rgba(79, 107, 237, 0.06); }
.stTabs [aria-selected="true"] {
    color: #17203a !important;
    background: linear-gradient(135deg, rgba(79, 107, 237, 0.16), rgba(15, 156, 143, 0.10));
}

/* ------------------------------------------------------------ sun / air */
.info-card, .map-side {
    background: linear-gradient(152deg, rgba(255, 255, 255, 0.96), rgba(241, 246, 255, 0.92));
}
.pollutant .p-row b { color: #2b3552; }
.ladder-label.cold { border-top-color: rgba(59, 78, 140, 0.10); }

/* --------------------------------------------------------------- footer */
.app-footer { border-top-color: rgba(59, 78, 140, 0.12); }
.app-footer b { color: #44527a; }

/* -------------------------------------------------------------- sidebar */
[data-testid="stSidebar"] {
    background:
        radial-gradient(420px 300px at 50% -8%, rgba(79, 107, 237, 0.12), transparent 62%),
        linear-gradient(180deg, #fbfcff 0%, #f1f5fd 100%);
    border-right: 1px solid rgba(59, 78, 140, 0.12);
}
.side-logo {
    background: linear-gradient(145deg, rgba(79, 107, 237, 0.18), rgba(15, 156, 143, 0.12));
    border-color: rgba(79, 107, 237, 0.24);
    box-shadow: 0 8px 22px rgba(79, 107, 237, 0.16);
}
.side-status {
    background: rgba(255, 255, 255, 0.72);
    border-color: var(--stroke);
}
.side-status .row b { color: #2b3552; }
.side-status .live { color: #0f8f74; }
.side-status .demo { color: #b57500; }
.side-foot a { color: #3f5bd6; }
.st-key-theme_toggle button,
.st-key-lang_toggle button {
    background: linear-gradient(120deg, rgba(79, 107, 237, 0.16), rgba(15, 156, 143, 0.12)) !important;
    border: 1px solid rgba(79, 107, 237, 0.30) !important;
    color: #26345c !important;
}
.st-key-theme_toggle button:hover,
.st-key-lang_toggle button:hover {
    border-color: rgba(15, 156, 143, 0.55) !important;
    box-shadow: 0 8px 20px rgba(79, 107, 237, 0.16);
}
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] > div {
    background: rgba(255, 255, 255, 0.88);
    border-color: rgba(59, 78, 140, 0.18);
    color: var(--text);
}
[data-testid="stSidebar"] [data-testid="stTextInputRootElement"] {
    background: rgba(255, 255, 255, 0.88) !important;
    border-color: rgba(59, 78, 140, 0.18) !important;
}
[data-testid="stSidebar"] [data-testid="stTextInputRootElement"]:focus-within {
    border-color: rgba(79, 107, 237, 0.55) !important;
    box-shadow: 0 0 0 2px rgba(79, 107, 237, 0.12) !important;
}
[data-testid="stSidebar"] .stTextInput input::placeholder { color: #8792b0; }
[data-testid="stSidebar"] .stTextInput input:focus {
    border-color: rgba(79, 107, 237, 0.55) !important;
    box-shadow: 0 0 0 2px rgba(79, 107, 237, 0.12) !important;
    outline: none !important;
}
.detail-hero h1 { color: var(--text); }
[data-testid="stSidebar"] label p { color: #44527a; }
[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: rgba(79, 107, 237, 0.12) !important;
}
[data-testid="stSidebar"] [data-baseweb="tag"] span { color: #26345c !important; }

/* ------------------------------------------------------ Streamlit widgets */
[data-testid="stMarkdownContainer"],
[data-testid="stWidgetLabel"],
[data-testid="stCaptionContainer"],
[data-testid="stSidebar"] { color: var(--text); }
.side-title { color: #17203a; }
[data-testid="stMultiSelect"] [role="group"] {
    background: rgba(255, 255, 255, 0.88);
    border: 1px solid rgba(59, 78, 140, 0.18);
    border-radius: 11px;
}
[data-testid="stMultiSelect"] input { color: var(--text); }
[data-testid="stMultiSelect"] input::placeholder { color: #8792b0; opacity: 1; }
[data-testid="stMultiSelect"] button { color: #44527a; }
[data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.78);
    border-color: var(--stroke);
}
[data-testid="stExpander"] summary { color: #44527a; }
[data-testid="stPlotlyChart"] {
    background: linear-gradient(152deg, rgba(255, 255, 255, 0.94), rgba(241, 246, 255, 0.9));
    border-color: var(--stroke);
}
[data-testid="stAlert"] { border-radius: 13px; }
[data-testid="stAlert"] p,
[data-testid="stAlert"] li { color: #26345c; }
button[data-variant="segmented_control"],
[data-testid="stSegmentedControl"] button,
[data-baseweb="button-group"] button {
    color: #44527a !important;
    background: rgba(255, 255, 255, 0.78) !important;
    border-color: rgba(59, 78, 140, 0.16) !important;
}
button[data-variant="segmented_control"]:hover,
[data-testid="stSegmentedControl"] button:hover,
[data-baseweb="button-group"] button:hover { background: rgba(79, 107, 237, 0.08) !important; }
button[data-variant="segmented_control"][aria-checked="true"],
[data-testid="stSegmentedControl"] button[aria-checked="true"],
[data-testid="stSegmentedControl"] button[aria-selected="true"] {
    color: #ffffff !important;
    background: #4f6bed !important;
    border-color: #4f6bed !important;
}
[data-baseweb="popover"], [data-baseweb="menu"], [role="listbox"] {
    background: #ffffff !important;
    color: #17203a !important;
    border-color: rgba(59, 78, 140, 0.16) !important;
}
[data-baseweb="popover"] li:hover, [role="option"]:hover { background: rgba(79, 107, 237, 0.08) !important; }
[data-testid="stCaptionContainer"] p { color: var(--faint); }
</style>
"""


def theme_css(theme: str = DEFAULT_THEME) -> str:
    """Return the stylesheet for ``theme`` (dark is the base, light extends it)."""

    return CSS + (LIGHT_CSS if theme == "light" else "")
