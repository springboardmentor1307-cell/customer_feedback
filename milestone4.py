# ============================
# ReviewSense – Milestone 4 (Enhanced & Fixed Final)
# Interactive Customer Feedback Dashboard
# ============================
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from wordcloud import WordCloud
import numpy as np
import hashlib

# ── Demo Credentials (SHA-256 hashed) ────────────────────────────────────────
# Default: username="admin", password="admin123"
# To add users: hashlib.sha256("yourpassword".encode()).hexdigest()
USERS = {
    "admin": hashlib.sha256("admin123".encode()).hexdigest(),

}

# ── Session State ────────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""


def verify_login(username: str, password: str) -> bool:
    hashed = hashlib.sha256(password.encode()).hexdigest()
    return USERS.get(username.strip().lower()) == hashed


# ── Authentication Check ─────────────────────────────────────────
if not st.session_state.authenticated:
    # Page configuration for login
    st.set_page_config(
        page_title="ReviewSense – Login",
        page_icon="🔐",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    # Custom CSS for login
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & Root ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #0a0e1a !important;
    font-family: 'DM Sans', sans-serif;
    min-height: 100vh;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 60% at 50% -10%, rgba(29,99,220,0.35) 0%, transparent 70%),
        radial-gradient(ellipse 50% 40% at 85% 80%, rgba(100,220,180,0.12) 0%, transparent 60%),
        #0a0e1a !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

/* ── Card wrapper ── */
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"],
section.main > div { padding-top: 0 !important; }

/* ── Logo / Brand ── */
.brand-wrap {
    text-align: center;
    padding: 3.5rem 0 2rem;
}
.brand-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 72px; height: 72px;
    border-radius: 20px;
    background: linear-gradient(135deg, #1d63dc 0%, #38c9a4 100%);
    font-size: 2.2rem;
    box-shadow: 0 8px 32px rgba(29,99,220,0.45);
    margin-bottom: 1.1rem;
}
.brand-name {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    background: linear-gradient(90deg, #ffffff 30%, #38c9a4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.brand-tagline {
    color: rgba(255,255,255,0.45);
    font-size: 0.9rem;
    font-weight: 300;
    letter-spacing: 0.04em;
    margin-top: 0.3rem;
}

/* ── Login card ── */
.login-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 20px;
    padding: 2.2rem 2.4rem 2.4rem;
    max-width: 420px;
    margin: 0 auto 2rem;
    backdrop-filter: blur(16px);
    box-shadow: 0 24px 64px rgba(0,0,0,0.4), 0 1px 0 rgba(255,255,255,0.07) inset;
}
.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.3rem;
}
.card-sub {
    color: rgba(255,255,255,0.4);
    font-size: 0.85rem;
    margin-bottom: 1.8rem;
}

/* ── Input labels ── */
.stTextInput label, .stTextInput [data-testid="InputInstructions"] {
    color: rgba(255,255,255,0.65) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
}

/* ── Input fields ── */
.stTextInput input {
    background: #ffffff !important;
    border: 1px solid #cccccc !important;
    border-radius: 10px !important;
    color: #000000 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput input:focus {
    border-color: #1d63dc !important;
    box-shadow: 0 0 0 3px rgba(29,99,220,0.22) !important;
    outline: none !important;
}
.stTextInput input::placeholder { color: #666666 !important; }

/* ── Button ── */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #1d63dc 0%, #1a52b8 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    padding: 0.7rem 1.5rem !important;
    margin-top: 0.5rem !important;
    cursor: pointer !important;
    transition: transform 0.15s, box-shadow 0.2s !important;
    box-shadow: 0 4px 18px rgba(29,99,220,0.4) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 28px rgba(29,99,220,0.55) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Alerts ── */
.stAlert {
    border-radius: 10px !important;
    font-size: 0.88rem !important;
}

/* ── Demo hint ── */
.demo-hint {
    text-align: center;
    color: rgba(255,255,255,0.25);
    font-size: 0.78rem;
    margin-top: 1.5rem;
    letter-spacing: 0.02em;
}
.demo-hint span { color: rgba(56,201,164,0.7); font-weight: 500; }

/* ── Divider ── */
.divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.07);
    margin: 1.4rem 0 1.2rem;
}
</style>
""", unsafe_allow_html=True)

    # ── Login UI ────────
    st.markdown("""
<div class="brand-wrap">
    <div class="brand-icon">📊</div>
    <div class="brand-name">ReviewSense</div>
    <div class="brand-tagline">Customer Feedback Intelligence Platform</div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Welcome back</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="card-sub">Sign in to access your dashboard</div>',
                unsafe_allow_html=True)

    username = st.text_input(
        "Username", placeholder="Enter your username", key="username_input")
    password = st.text_input(
        "Password", placeholder="Enter your password", type="password", key="password_input")

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    if st.button("Sign In →", use_container_width=True):
        if not username or not password:
            st.error("⚠️ Please enter both username and password.")
        elif verify_login(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username.strip().lower()
            st.success("✅ Login successful! Loading your dashboard…")
            st.rerun()
        else:
            st.error("❌ Invalid username or password. Please try again.")

    st.markdown("""
<div class="demo-hint">
    Demo credentials — username: <span>admin</span> · password: <span>admin123</span>
</div>
""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()  # Stop execution if not authenticated

# If authenticated, proceed to dashboard
# Page configuration
st.set_page_config(
    page_title="ReviewSense Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better look
st.markdown(
    """
        <style>
        .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        }
        .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        </style>
""",
    unsafe_allow_html=True,
)

# ── Load Data


@st.cache_data
def load_data():
    df = pd.read_csv("Milestone2_Sentiment_Results.csv")

    # ←←← ADD THESE TWO LINES ←←←
    df["sentiment"] = df["sentiment"].str.lower().str.strip()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    return df


@st.cache_data
def load_keywords():
    """Load keywords CSV, supporting both plain and marked formats."""
    # first try reading as a normal CSV file
    try:
        keywords_df = pd.read_csv("Milestone3_Keyword_Insights.csv")
        if "keyword" in keywords_df.columns and "frequency" in keywords_df.columns:
            return keywords_df
    except Exception:
        pass

    # fallback: parse sections if the file contains markers
    try:
        with open("Milestone3_Keyword_Insights.csv", "r", encoding="utf-8") as f:
            content = f.read()
        if "=== KEYWORD FREQUENCY ===" in content:
            keyword_part = content.split("=== KEYWORD FREQUENCY===")[1].split(
                "=== PRODUCT SENTIMENT SUMMARY ==="
            )[0]
            keyword_part = keyword_part.strip().splitlines()
            if len(keyword_part) > 1:
                keywords_df = pd.read_csv(pd.StringIO("\n".join(keyword_part)))
                return keywords_df
    except Exception:
        pass

    return pd.DataFrame()


df = load_data()
keywords_df = load_keywords()

# ── Sidebar Filters
st.sidebar.header("🔍 Filters")
# Logout
st.sidebar.subheader("👤 User")
st.sidebar.write(f"Logged in as: **{st.session_state.username}**")
if st.sidebar.button("Logout", use_container_width=True):
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.rerun()
# Sentiment
sentiment_options = ["positive", "negative", "neutral"]
sentiment_display = {"positive": "Positive",
                     "negative": "Negative", "neutral": "Neutral"}
sentiment_filter_display = st.sidebar.multiselect(
    "Select Sentiment",
    options=[sentiment_display[s] for s in sentiment_options],
    default=[sentiment_display[s] for s in sentiment_options],
)
sentiment_filter = [k for k, v in sentiment_display.items()
                    if v in sentiment_filter_display]
# Product
product_filter = st.sidebar.multiselect(
    "Select Product",
    options=sorted(df["product"].unique()),
    default=sorted(df["product"].unique()),
)
# Date range
st.sidebar.subheader("📅 Date Range")
# Safe defaults
if pd.notna(df["date"].min()):
    default_start = df["date"].min().date()
else:
    default_start = datetime(2025, 1, 1).date()
if pd.notna(df["date"].max()):
    default_end = df["date"].max().date()
else:
    default_end = datetime(2025, 12, 31).date()
col1, col2 = st.sidebar.columns(2)
start_date = col1.date_input("Start Date", value=default_start)
end_date = col2.date_input("End Date", value=default_end)

# ── Apply Filters
filtered_df = df[
    (df["sentiment"].isin(sentiment_filter))
    & (df["product"].isin(product_filter))
    & (df["date"] >= pd.to_datetime(start_date))
    & (df["date"] <= pd.to_datetime(end_date))
].copy()  # .copy() avoids SettingWithCopyWarning later

# ── Main Dashboard
st.markdown(
    '<h1 class="main-header">📊 ReviewSense – Customer Feedback Dashboard</h1>',
    unsafe_allow_html=True,
)

# Key Metrics
col1, col2, col3, col4 = st.columns(4)
total_reviews = len(filtered_df)
pos_count = len(filtered_df[filtered_df["sentiment"] == "positive"])
neg_count = len(filtered_df[filtered_df["sentiment"] == "negative"])
neu_count = len(filtered_df[filtered_df["sentiment"] == "neutral"])
pos_pct = (pos_count / total_reviews * 100) if total_reviews > 0 else 0
neg_pct = (neg_count / total_reviews * 100) if total_reviews > 0 else 0
neu_pct = (neu_count / total_reviews * 100) if total_reviews > 0 else 0
with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Total Reviews", total_reviews)
    st.markdown("</div>", unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Positive", f"{pos_pct:.1f}%", delta=f"{pos_count} reviews")
    st.markdown("</div>", unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Negative", f"{neg_pct:.1f}%", delta=f"{neg_count} reviews")
    st.markdown("</div>", unsafe_allow_html=True)
with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Neutral", f"{neu_pct:.1f}%", delta=f"{neu_count} reviews")
    st.markdown("</div>", unsafe_allow_html=True)

# ── Sentiment Distribution ──────────────────────────────────────────────────
st.subheader("😊 Sentiment Distribution")
if not filtered_df.empty:
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    counts = filtered_df["sentiment"].value_counts()
    colors = {"positive": "#4CAF50",
              "negative": "#F44336", "neutral": "#9E9E9E"}
    bars = ax1.bar(
        [sentiment_display.get(s, s.title()) for s in counts.index],
        counts.values,
        color=[colors.get(s, "gray") for s in counts.index]
    )
    ax1.set_xlabel("Sentiment")
    ax1.set_ylabel("Number of Reviews")
    ax1.set_title("Overall Sentiment Breakdown")
    for bar in bars:
        yval = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            yval + 10,
            int(yval),
            ha="center",
            va="bottom",
        )
    st.pyplot(fig1)
else:
    st.info("No data matches the selected filters.")

# ── Product Sentiment ───────────────────────────────────────────────────────
st.subheader("📱 Product-wise Sentiment")
if not filtered_df.empty:
    product_sent = (
        filtered_df.groupby("product")[
            "sentiment"].value_counts().unstack(fill_value=0)
    )
    # Ensure all sentiment columns exist
    for col in sentiment_options:
        if col not in product_sent.columns:
            product_sent[col] = 0
    product_sent["Total"] = product_sent.sum(axis=1)
    product_sent["Positive %"] = (
        product_sent.get("positive", 0) / product_sent["Total"] * 100
    ).round(1)
    product_sent = product_sent.sort_values("Positive %", ascending=False)
    # Rename columns for display
    display_cols = [sentiment_display[s] for s in sentiment_options]
    product_sent_disp = product_sent.copy()
    product_sent_disp.rename(columns=sentiment_display, inplace=True)
    st.dataframe(product_sent_disp[display_cols + ["Total", "Positive %"]
                                   ].style.format(precision=1), use_container_width=True)
    # Heatmap
    fig_hm, ax_hm = plt.subplots(figsize=(10, 6))
    sns.heatmap(
        product_sent[sentiment_options],
        annot=True,
        fmt="d",
        cmap="RdYlGn",
        ax=ax_hm,
    )
    ax_hm.set_title("Product Sentiment Heatmap")
    st.pyplot(fig_hm)

    # ── Trend Over Time
    st.subheader("📈 Sentiment Trends Over Time")
if not filtered_df.empty:
    filtered_df["month"] = filtered_df["date"].dt.to_period("M")
    trend = filtered_df.groupby(
        ["month", "sentiment"]).size().unstack(fill_value=0)
    fig_trend, ax_trend = plt.subplots(figsize=(12, 6))
    for col in trend.columns:
        ax_trend.plot(
            trend.index.astype(str), trend[col], marker="o", linewidth=2, label=col
        )
    ax_trend.set_xlabel("Month")
    ax_trend.set_ylabel("Number of Reviews")
    ax_trend.set_title("Monthly Sentiment Trend")
    ax_trend.legend()
    ax_trend.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    st.pyplot(fig_trend)
else:
    st.info("No date-based data available after filtering.")

# ── Keywords ────────────────────────────────────────────────────────────────
st.subheader("🔑 Top Keywords & Word Cloud")
if not keywords_df.empty:
    top10 = keywords_df.head(15)
    colA, colB = st.columns([3, 2])
    with colA:
        fig_bar, ax_bar = plt.subplots(figsize=(10, 6))
        ax_bar.barh(top10["keyword"], top10["frequency"], color="skyblue")
        ax_bar.set_xlabel("Frequency")
        ax_bar.set_title("Top Keywords")
        ax_bar.invert_yaxis()
        st.pyplot(fig_bar)
    with colB:
        if len(top10) > 0:
            word_freq = dict(
                zip(keywords_df["keyword"], keywords_df["frequency"]))
            wc = WordCloud(
                width=400, height=400, background_color="white", min_font_size=10
            ).generate_from_frequencies(word_freq)
            fig_wc, ax_wc = plt.subplots(figsize=(6, 6))
            ax_wc.imshow(wc, interpolation="bilinear")
            ax_wc.axis("off")
            st.pyplot(fig_wc)

# ── Confidence Score ────────────────────────────────────────────────────────
st.subheader("📊 Confidence Score Distribution")
if not filtered_df.empty:
    fig_hist, ax_hist = plt.subplots(figsize=(10, 5))
    ax_hist.hist(
        filtered_df["confidence_score"],
        bins=25,
        color="cornflowerblue",
        edgecolor="black",
        alpha=0.7,
    )
    ax_hist.set_xlabel("Confidence Score (–1 to +1)")
    ax_hist.set_ylabel("Count")
    ax_hist.set_title("Sentiment Confidence Distribution")
    st.pyplot(fig_hist)

# ── Data & Download ─────────────────────────────────────────────────────────
with st.expander("📋 Preview Filtered Data (first 15 rows)"):
    st.dataframe(filtered_df.head(15), use_container_width=True)
    st.subheader("💾 Export Options")
    col_dl1, col_dl2 = st.columns(2)
with col_dl1:
    st.download_button(
        "⬇️ Download Filtered Reviews",
        filtered_df.to_csv(index=False).encode("utf-8"),
        "ReviewSense_Filtered_Reviews.csv",
        "text/csv",
        use_container_width=True,
    )
with col_dl2:
    if not keywords_df.empty:
        st.download_button(
            "⬇️ Download Keyword List",
            keywords_df.to_csv(index=False).encode("utf-8"),
            "ReviewSense_Keywords.csv",
            "text/csv",
            use_container_width=True,
        )
st.success("✅ Dashboard ready! Use the sidebar to explore different views.")
