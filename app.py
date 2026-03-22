import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="DAZI Paid Search Simulator", page_icon="🎯", layout="wide")

BUDGET = 5000
MARGIN_PER_CONVERSION = 20

KEYWORDS = [
    {"keyword": "necktie", "competition": "High", "comp_score": 5, "top_bid": 2.10, "avg_monthly": 100_000, "quality": 7, "conv_rate": 0.045},
    {"keyword": "tie for suit", "competition": "High", "comp_score": 5, "top_bid": 2.40, "avg_monthly": 10_000, "quality": 6, "conv_rate": 0.047},
    {"keyword": "floral tie", "competition": "High", "comp_score": 5, "top_bid": 1.71, "avg_monthly": 9_500, "quality": 10, "conv_rate": 0.12},
    {"keyword": "floral wedding tie", "competition": "High", "comp_score": 5, "top_bid": 2.50, "avg_monthly": 9_000, "quality": 10, "conv_rate": 0.15},
    {"keyword": "pink floral tie", "competition": "High", "comp_score": 5, "top_bid": 1.30, "avg_monthly": 8_500, "quality": 10, "conv_rate": 0.16},
    {"keyword": "floral tie for sale", "competition": "High", "comp_score": 5, "top_bid": 2.40, "avg_monthly": 880, "quality": 9, "conv_rate": 0.25},
    {"keyword": "unique floral tie", "competition": "Medium", "comp_score": 4, "top_bid": 0.95, "avg_monthly": 700, "quality": 9, "conv_rate": 0.06},
    {"keyword": "red tie with black suit", "competition": "Medium", "comp_score": 4, "top_bid": 0.65, "avg_monthly": 550, "quality": 6, "conv_rate": 0.034},
    {"keyword": "tie and handkerchief set", "competition": "Medium", "comp_score": 4, "top_bid": 0.50, "avg_monthly": 550, "quality": 5, "conv_rate": 0.035},
    {"keyword": "how to tie a tie", "competition": "Low", "comp_score": 3, "top_bid": 0.25, "avg_monthly": 500_000, "quality": 6, "conv_rate": 0.016},
    {"keyword": "best tie knot", "competition": "Low", "comp_score": 3, "top_bid": 0.10, "avg_monthly": 9_000, "quality": 4, "conv_rate": 0.025},
]


def simulate(keywords, bids):
    raw_rows = []
    for kw, bid in zip(keywords, bids):
        F, G, D, C, E, S = bid, kw["quality"], kw["top_bid"], kw["comp_score"], kw["avg_monthly"], kw["conv_rate"]
        impressions0 = round((G * F / (D * 11)) * 0.5 * E) if G * F > D * C else 0
        top_rate = min(F * G / (D * C / 3.5 * 10), 0.98) if F * G > D * C else 0.0
        q_mult = 5 if G > 9 else (2 if G > 7 else 1)
        ctr = top_rate * 0.14 / C * q_mult
        clicks0 = round(impressions0 * ctr)
        raw_rows.append({"impressions0": impressions0, "top_rate": top_rate, "ctr": ctr, "clicks0": clicks0, "bid": F, "conv_rate": S})

    total_raw_spend = sum(r["bid"] * r["clicks0"] for r in raw_rows)
    scale = BUDGET / total_raw_spend if total_raw_spend > BUDGET else 1.0

    results = []
    for r in raw_rows:
        impressions = round(r["impressions0"] * scale) if total_raw_spend > BUDGET else r["impressions0"]
        clicks = round(r["clicks0"] * scale) if total_raw_spend > BUDGET else r["clicks0"]
        total_cost = r["bid"] * clicks
        conversions = round(clicks * r["conv_rate"])
        cpa = total_cost / conversions if conversions > 0 else None
        poas = (MARGIN_PER_CONVERSION - cpa) / cpa if cpa is not None and cpa > 0 else None
        results.append({"Impressions": impressions, "Top Imp. Rate": r["top_rate"], "CTR": r["ctr"],
            "Clicks": clicks, "Avg CPC": r["bid"], "Total Cost": total_cost,
            "Conversions": conversions, "Conv. Rate": r["conv_rate"], "CPA": cpa, "POAS": poas})
    return results


# ─── Google Ads Style CSS ───
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Roboto:wght@400;500;700&display=swap');

    .stApp {
        background-color: #f8f9fa !important;
        font-family: 'Roboto', 'Google Sans', sans-serif;
        color: #202124;
    }

    .google-ads-header {
        background: #1a73e8;
        padding: 16px 24px;
        border-radius: 0;
        margin: -1rem -1rem 24px -1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        gap: 4px;
    }
    .google-ads-logo {
        font-family: 'Google Sans', sans-serif;
        font-size: 20px;
        font-weight: 500;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .google-ads-subtitle {
        font-size: 13px;
        color: rgba(255,255,255,0.8);
        margin-left: 0;
    }

    .section-title {
        font-family: 'Google Sans', 'Roboto', sans-serif;
        font-size: 16px;
        font-weight: 500;
        color: #202124;
        margin: 20px 0 12px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid #1a73e8;
        display: inline-block;
    }

    div[data-testid="stMetric"] {
        background: #ffffff !important;
        border: 1px solid #dadce0;
        border-radius: 8px;
        padding: 16px 20px;
        box-shadow: none;
    }
    div[data-testid="stMetric"] label {
        color: #5f6368 !important;
        font-size: 11px !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-family: 'Roboto', sans-serif !important;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #202124 !important;
        font-size: 24px !important;
        font-weight: 500 !important;
        font-family: 'Google Sans', 'Roboto', sans-serif !important;
    }

    .stTabs [data-baseweb="tab-list"] { gap: 0px; border-bottom: 1px solid #dadce0; }
    .stTabs [data-baseweb="tab"] {
        color: #5f6368; font-family: 'Google Sans', 'Roboto', sans-serif;
        font-size: 14px; font-weight: 500; padding: 12px 24px;
        border-bottom: 3px solid transparent;
    }
    .stTabs [aria-selected="true"] { color: #1a73e8 !important; border-bottom: 3px solid #1a73e8 !important; }

    .stDataFrame { border: 1px solid #dadce0; border-radius: 8px; overflow: hidden; }

    .feedback-good {
        background: #e6f4ea; border: 1px solid #34a853;
        border-radius: 8px; padding: 12px 16px; color: #137333; font-weight: 500;
    }
    .feedback-ok {
        background: #fef7e0; border: 1px solid #f9ab00;
        border-radius: 8px; padding: 12px 16px; color: #b06000; font-weight: 500;
    }
    .feedback-bad {
        background: #fce8e6; border: 1px solid #ea4335;
        border-radius: 8px; padding: 12px 16px; color: #c5221f; font-weight: 500;
    }

    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #dadce0;
    }
    section[data-testid="stSidebar"] .stMarkdown h2 {
        font-size: 18px !important;
        color: #202124 !important;
        font-family: 'Google Sans', sans-serif !important;
    }
    .keyword-label {
        font-size: 15px;
        font-weight: 600;
        color: #202124;
        margin-bottom: 2px;
        line-height: 1.4;
    }
    .keyword-info {
        font-size: 12px;
        color: #5f6368;
        margin-bottom: 8px;
    }

    .stMarkdown, .stMarkdown p, .stCaption { color: #202124 !important; }
    a { color: #1a73e8 !important; }
    .stProgress > div > div { background-color: #1a73e8 !important; }

    .ad-copy-box { background: #fff; border-radius: 8px; padding: 16px 20px; margin-bottom: 16px; border: 1px solid #dadce0; }
    .ad-label { font-size: 11px; color: #202124; font-weight: 700; display: inline-block; background: #f1f3f4; padding: 2px 6px; border-radius: 3px; margin-right: 6px; border: 1px solid #dadce0; }
    .ad-url { font-size: 13px; color: #202124; }
    .ad-headline { font-size: 18px; color: #1a0dab; font-weight: 400; margin: 4px 0; line-height: 1.3; }
    .ad-description { font-size: 13px; color: #4d5156; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)


# ─── Header ───
st.markdown("""
<div class="google-ads-header">
    <div class="google-ads-logo">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="white"><circle cx="12" cy="12" r="10" fill="none" stroke="white" stroke-width="2"/><text x="12" y="16" text-anchor="middle" font-size="12" fill="white" font-weight="bold">G</text></svg>
        DAZI Paid Search Simulator
    </div>
    <div class="google-ads-subtitle">Floral Tie Campaign — Adjust your keyword bids in the sidebar and watch results update in real time.</div>
</div>
""", unsafe_allow_html=True)

# ─── Tabs ───
tab_sim, tab_ref, tab_ads, tab_glossary = st.tabs(["📊 Bid Simulator", "🔍 Keyword Research", "📢 Ad Group: Floral Ties", "📖 Glossary"])

# ─── Sidebar ───
with st.sidebar:
    st.markdown("## 💰 Set Your Bids")
    st.markdown(f"**Budget:** ${BUDGET:,}")
    st.divider()
    bids = []
    for i, kw in enumerate(KEYWORDS):
        st.markdown(f'<div class="keyword-label">{kw["keyword"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="keyword-info">Competition: {kw["competition"]} &nbsp;·&nbsp; Top bid: ${kw["top_bid"]:.2f} &nbsp;·&nbsp; Vol: {kw["avg_monthly"]:,}</div>', unsafe_allow_html=True)
        bid = st.slider(f"CPC Bid for {kw['keyword']}", 0.0, round(max(kw["top_bid"] * 2.5, 3.0), 2), 0.0, 0.01, format="$%.2f", key=f"bid_{i}", label_visibility="collapsed")
        bids.append(bid)
        st.markdown("---")
    st.caption("💡 Tip: Focus bids on high-quality floral keywords first for the best POAS!")

# ─── Run Simulation ───
results = simulate(KEYWORDS, bids)
total_imp = sum(r["Impressions"] for r in results)
total_clicks = sum(r["Clicks"] for r in results)
total_cost = sum(r["Total Cost"] for r in results)
total_conv = sum(r["Conversions"] for r in results)
total_ctr = total_clicks / total_imp * 100 if total_imp > 0 else 0
total_conv_rate = total_conv / total_clicks * 100 if total_clicks > 0 else 0
total_cpa = total_cost / total_conv if total_conv > 0 else None
total_poas = (MARGIN_PER_CONVERSION - total_cpa) / total_cpa * 100 if total_cpa and total_cpa > 0 else None


# ═══════════════════════════════════════════════════════
# TAB 1: BID SIMULATOR
# ═══════════════════════════════════════════════════════

with tab_sim:
    st.markdown('<div class="section-title">Summary of Simulation Results</div>', unsafe_allow_html=True)

    m1, m2, m3, m4, m5, m6, m7 = st.columns(7)
    m1.metric("Impressions", f"{total_imp:,}")
    m2.metric("Clicks", f"{total_clicks:,}")
    m3.metric("CTR", f"{total_ctr:.2f}%")
    m4.metric("Conversions", f"{total_conv:,}")
    m5.metric("Conv. Rate", f"{total_conv_rate:.2f}%")
    m6.metric("Total Cost", f"${total_cost:,.2f}")
    m7.metric("POAS", f"{total_poas:.1f}%" if total_poas is not None else "—")

    budget_pct = min(total_cost / BUDGET * 100, 100)
    st.markdown(f'**Budget used:** ${total_cost:,.0f} / ${BUDGET:,} ({budget_pct:.0f}%)')
    st.progress(budget_pct / 100)

    # Performance Feedback
    st.markdown("")
    st.markdown('<div class="section-title">Performance Feedback</div>', unsafe_allow_html=True)
    fb1, fb2 = st.columns(2)
    with fb1:
        if total_clicks >= 7200:
            st.markdown('<div class="feedback-good">✅ <b>Clicks:</b> Great click volume!</div>', unsafe_allow_html=True)
        elif total_clicks >= 6000:
            st.markdown('<div class="feedback-ok">➡️ <b>Clicks:</b> Good volume, but push for more clicks.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="feedback-bad">❌ <b>Clicks:</b> Drive more clicks! Increase bids on high-quality keywords.</div>', unsafe_allow_html=True)
        st.markdown("")
        if total_cost >= 4500:
            st.markdown('<div class="feedback-good">✅ <b>Budget:</b> You\'ve deployed almost all your budget!</div>', unsafe_allow_html=True)
        elif total_cost >= 3000:
            st.markdown('<div class="feedback-ok">➡️ <b>Budget:</b> Using budget — try to deploy the full $5,000.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="feedback-bad">❌ <b>Budget:</b> You haven\'t used much of your budget.</div>', unsafe_allow_html=True)
    with fb2:
        if total_conv >= 310:
            st.markdown('<div class="feedback-good">✅ <b>Conversions:</b> Excellent conversions!</div>', unsafe_allow_html=True)
        elif total_conv >= 290:
            st.markdown('<div class="feedback-ok">➡️ <b>Conversions:</b> Close to target — optimize further.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="feedback-bad">❌ <b>Conversions:</b> Drive more conversions! Focus on high-conversion keywords.</div>', unsafe_allow_html=True)
        st.markdown("")
        if total_poas is not None and total_poas >= 18:
            st.markdown('<div class="feedback-good">✅ <b>POAS:</b> Strong profit on ad spend!</div>', unsafe_allow_html=True)
        elif total_poas is not None and total_poas >= 0:
            st.markdown('<div class="feedback-ok">➡️ <b>POAS:</b> Profitable, but can be improved.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="feedback-bad">❌ <b>POAS:</b> Not profitable — you\'re losing money on ads.</div>', unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<div class="section-title">Keyword Performance Results</div>', unsafe_allow_html=True)

    # Build table: text columns for "-" display, numeric columns for sorting
    table_rows = []
    for kw, r in zip(KEYWORDS, results):
        clicks = r["Clicks"]
        conv = r["Conversions"]
        table_rows.append({
            "Keyword": kw["keyword"],
            "Quality": kw["quality"],
            "Your Bid": bids[KEYWORDS.index(kw)],
            "Impressions": r["Impressions"],
            "Top Imp. %": f"{r['Top Imp. Rate'] * 100:.1f}%" if clicks > 0 else "-",
            "CTR": f"{r['CTR'] * 100:.2f}%" if clicks > 0 else "-",
            "Clicks": clicks,
            "Avg CPC": f"${r['Avg CPC']:.2f}" if clicks > 0 else "-",
            "Total Cost": r["Total Cost"],
            "Conversions": conv,
            # Conv. Rate as text (sorting not critical)
            "Conv. Rate": f"{conv / clicks * 100:.1f}%" if clicks > 0 else "-",
            # CPA and POAS as NUMBERS for proper sorting (None shows blank)
            "CPA": r["CPA"],
            "POAS": r["POAS"] * 100 if r["POAS"] is not None else None,
        })

    df_results = pd.DataFrame(table_rows)

    st.dataframe(
        df_results,
        use_container_width=True,
        hide_index=True,
        height=440,
        column_config={
            "Quality": st.column_config.NumberColumn(format="%d"),
            "Your Bid": st.column_config.NumberColumn(format="$%.2f"),
            "Impressions": st.column_config.NumberColumn(format="%d"),
            "Top Imp. %": st.column_config.TextColumn(),
            "CTR": st.column_config.TextColumn(),
            "Clicks": st.column_config.NumberColumn(format="%d"),
            "Avg CPC": st.column_config.TextColumn(),
            "Total Cost": st.column_config.NumberColumn(format="$%,.2f"),
            "Conversions": st.column_config.NumberColumn(format="%d"),
            "Conv. Rate": st.column_config.TextColumn(),
            # CPA and POAS stay as NumberColumn for sorting
            "CPA": st.column_config.NumberColumn(format="$%.2f"),
            "POAS": st.column_config.NumberColumn("POAS", format="%.1f%%"),
        },
    )

    tc1, tc2, tc3, tc4, tc5 = st.columns(5)
    tc1.markdown(f"**Total Impressions:** {total_imp:,}")
    tc2.markdown(f"**Total Clicks:** {total_clicks:,}")
    tc3.markdown(f"**Total Cost:** ${total_cost:,.2f}")
    tc4.markdown(f"**Total Conversions:** {total_conv:,}")
    tc5.markdown(f"**Avg CPA:** {'${:.2f}'.format(total_cpa) if total_cpa else '—'}")


# ═══════════════════════════════════════════════════════
# TAB 2: KEYWORD RESEARCH
# ═══════════════════════════════════════════════════════

with tab_ref:
    st.markdown('<div class="section-title">Keyword Research Data</div>', unsafe_allow_html=True)
    st.markdown("Use this reference data to inform your bidding strategy.")
    st.markdown("")

    ref_df = pd.DataFrame({
        "Keyword": [kw["keyword"] for kw in KEYWORDS],
        "Competition": [kw["competition"] for kw in KEYWORDS],
        "Top-of-Page Bid": [kw["top_bid"] for kw in KEYWORDS],
        "Avg Monthly Searches": [kw["avg_monthly"] for kw in KEYWORDS],
    })

    st.dataframe(ref_df, use_container_width=True, hide_index=True, height=422,
        column_config={
            "Top-of-Page Bid": st.column_config.NumberColumn(format="$%.2f"),
            "Avg Monthly Searches": st.column_config.NumberColumn(format="%d"),
        })


# ═══════════════════════════════════════════════════════
# TAB 3: ADS & LANDING PAGE
# ═══════════════════════════════════════════════════════

with tab_ads:
    st.markdown('<div class="section-title">Ad Group: Floral Ties</div>', unsafe_allow_html=True)
    st.markdown(f"**Landing page:** [www.daziusa.com/collections/floral](https://www.daziusa.com/collections/floral)")
    st.markdown("")
    st.markdown('<div class="section-title">Ad Copy Examples</div>', unsafe_allow_html=True)
    col_ad1, col_ad2 = st.columns(2)
    with col_ad1:
        st.markdown("""<div class="ad-copy-box"><div><span class="ad-label">Ad</span> <span class="ad-url">https://www.daziusa.com/neckties/floral</span></div><div class="ad-headline">Shop Floral Ties For Weddings - Free Shipping On Orders $40+</div><div class="ad-description">Browse Our Original <b>Floral Ties</b>, <b>Floral</b> Bow <b>Ties</b>, And Other Essentials. Shop DAZI® Today! Free Shipping Over $40. Best Quality. Great For <b>Weddings</b>. Styles: White <b>Floral</b>, Blue Bloom.</div></div>""", unsafe_allow_html=True)
    with col_ad2:
        st.markdown("""<div class="ad-copy-box"><div><span class="ad-label">Ad</span> <span class="ad-url">https://www.daziusa.com/neckties/floral</span></div><div class="ad-headline">Shop Floral Ties - DAZI® Original Floral Ties - daziusa.com</div><div class="ad-description">Browse Our Original <b>Floral Ties</b>, <b>Floral</b> Bow <b>Ties</b>, And More. Shop & Save Today! Best Quality.</div></div>""", unsafe_allow_html=True)
    st.markdown("")
    st.markdown('<div class="section-title">Landing Page Preview</div>', unsafe_allow_html=True)
    st.markdown("The ads direct users to the DAZI floral ties collection page:")
    st.markdown("")

    st.image("Floral1.png", use_container_width=True)

    st.markdown("")
    st.caption("Landing page: www.daziusa.com/collections/floral — Products priced at $32.00 each")


# ═══════════════════════════════════════════════════════
# TAB 4: GLOSSARY
# ═══════════════════════════════════════════════════════

with tab_glossary:
    st.markdown('<div class="section-title">Glossary of Terms</div>', unsafe_allow_html=True)
    st.markdown("")
    for term, defn in {
        "CPC Bid": "The maximum amount you're willing to pay per click on an ad.",
        "Quality Score": "Google's rating (1–10) based on ad relevance, expected CTR, and landing page experience.",
        "Impressions": "The total number of times your ad appears in search results.",
        "Search Top Impression Rate": "The percentage of times your ad appears in the top positions.",
        "CTR (Click-Through Rate)": "The percentage of impressions that result in a click (Clicks ÷ Impressions).",
        "Avg. CPC": "The average amount you actually pay per click — equals your bid in this simulation.",
        "Total Cost": "Your total ad expenditure (CPC × Clicks). Capped at $5,000 budget.",
        "Conversions": "The number of desired actions completed (e.g., purchases).",
        "Conversion Rate": "The percentage of clicks that result in a conversion (Conversions ÷ Clicks).",
        "CPA (Cost per Acquisition)": "The cost of acquiring one customer (Total Cost ÷ Conversions).",
        "POAS (Profit on Ad Spend)": "Profitability measure: (Margin − CPA) ÷ CPA. Positive = profitable.",
        "Budget": "The $5,000 cap. If spend exceeds this, everything scales down proportionally.",
    }.items():
        with st.expander(f"**{term}**"):
            st.markdown(defn)