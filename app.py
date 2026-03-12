import streamlit as st
import pandas as pd
import math

# ─── Page Config ───
st.set_page_config(
    page_title="DAZI Paid Search Simulator",
    page_icon="🎯",
    layout="wide",
)

# ─── Constants ───
BUDGET = 5000
MARGIN_PER_CONVERSION = 20

# ─── Keyword Data ───
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
    """Run the paid search simulation using the exact Excel formulas."""
    raw_rows = []
    for kw, bid in zip(keywords, bids):
        F = bid
        G = kw["quality"]
        D = kw["top_bid"]
        C = kw["comp_score"]
        E = kw["avg_monthly"]
        S = kw["conv_rate"]

        # Impressions: =ROUND(IF(G*F > D*C, (G*F/(D*11))*0.5*E, 0), 0)
        if G * F > D * C:
            impressions0 = round((G * F / (D * 11)) * 0.5 * E)
        else:
            impressions0 = 0

        # Top Impression Rate: =MIN(IF(F*G > D*C, F*G/(D*C/3.5*10), 0), 0.98)
        if F * G > D * C:
            top_rate = min(F * G / (D * C / 3.5 * 10), 0.98)
        else:
            top_rate = 0.0

        # CTR: =top_rate * 0.14 / C * IF(G>9, 5, IF(G>7, 2, 1))
        q_mult = 5 if G > 9 else (2 if G > 7 else 1)
        ctr = top_rate * 0.14 / C * q_mult

        # Clicks: =ROUND(impressions0 * ctr, 0)
        clicks0 = round(impressions0 * ctr)

        raw_rows.append({
            "impressions0": impressions0,
            "top_rate": top_rate,
            "ctr": ctr,
            "clicks0": clicks0,
            "bid": F,
            "conv_rate": S,
        })

    # Budget scaling: if total raw spend > $5000, scale down proportionally
    total_raw_spend = sum(r["bid"] * r["clicks0"] for r in raw_rows)
    scale = BUDGET / total_raw_spend if total_raw_spend > BUDGET else 1.0

    results = []
    for r in raw_rows:
        if total_raw_spend > BUDGET:
            impressions = round(r["impressions0"] * scale)
            clicks = round(r["clicks0"] * scale)
        else:
            impressions = r["impressions0"]
            clicks = r["clicks0"]

        avg_cpc = r["bid"]
        total_cost = avg_cpc * clicks
        conversions = round(clicks * r["conv_rate"])
        cpa = total_cost / conversions if conversions > 0 else None
        roas = (MARGIN_PER_CONVERSION - cpa) / cpa if cpa is not None and cpa > 0 else None

        results.append({
            "Impressions": impressions,
            "Top Imp. Rate": r["top_rate"],
            "CTR": r["ctr"],
            "Clicks": clicks,
            "Avg CPC": avg_cpc,
            "Total Cost": total_cost,
            "Conversions": conversions,
            "Conv. Rate": r["conv_rate"],
            "CPA": cpa,
            "ROAS": roas,
        })

    return results


# ─── Custom CSS ───
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

    .stApp {
        font-family: 'DM Sans', sans-serif;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid rgba(148,163,184,0.12);
        border-radius: 14px;
        padding: 18px 20px;
    }

    div[data-testid="stMetric"] label {
        color: #64748b !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #f1f5f9 !important;
        font-size: 28px !important;
        font-weight: 700 !important;
    }

    .feedback-good {
        background: rgba(5,150,105,0.12);
        border: 1px solid rgba(5,150,105,0.25);
        border-radius: 10px;
        padding: 12px 16px;
        color: #34d399;
        font-weight: 600;
    }
    .feedback-ok {
        background: rgba(245,158,11,0.12);
        border: 1px solid rgba(245,158,11,0.25);
        border-radius: 10px;
        padding: 12px 16px;
        color: #fbbf24;
        font-weight: 600;
    }
    .feedback-bad {
        background: rgba(220,38,38,0.12);
        border: 1px solid rgba(220,38,38,0.25);
        border-radius: 10px;
        padding: 12px 16px;
        color: #f87171;
        font-weight: 600;
    }

    .comp-high { color: #ef4444; font-weight: 600; }
    .comp-medium { color: #f59e0b; font-weight: 600; }
    .comp-low { color: #22c55e; font-weight: 600; }

    section[data-testid="stSidebar"] {
        background: #0f172a;
    }

    .big-header {
        font-size: 28px;
        font-weight: 700;
        color: #f1f5f9;
        letter-spacing: -0.02em;
        margin-bottom: 4px;
    }

    .sub-header {
        font-size: 14px;
        color: #64748b;
        margin-bottom: 24px;
    }
</style>
""", unsafe_allow_html=True)


# ─── Header ───
st.markdown('<div class="sub-header" style="text-align: center;"><strong>Floral Tie Campaign</strong></div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header" style="text-align: center;"><strong>Floral Tie Campaign — Adjust your keyword bids in the sidebar and watch results update in real time.</strong></div>', unsafe_allow_html=True)

# ─── Tabs ───
tab_sim, tab_ref, tab_glossary = st.tabs(["📊 Bid Simulator", "🔍 Keyword Reference", "📖 Glossary"])


# ─── Sidebar: Bid Inputs ───
with st.sidebar:
    st.markdown("## 💰 Set Your Bids")
    st.markdown(f"**Budget:** ${BUDGET:,}")
    st.divider()

    bids = []
    for i, kw in enumerate(KEYWORDS):
        comp_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}[kw["competition"]]
        label = f"{comp_color} **{kw['keyword']}**"
        st.markdown(label)
        st.caption(f"Top bid: ${kw['top_bid']:.2f} · Quality: {kw['quality']}/10 · Vol: {kw['avg_monthly']:,}")

        bid = st.slider(
            label=f"CPC Bid for {kw['keyword']}",
            min_value=0.0,
            max_value=round(max(kw["top_bid"] * 2.5, 3.0), 2),
            value=0.0,
            step=0.01,
            format="$%.2f",
            key=f"bid_{i}",
            label_visibility="collapsed",
        )
        bids.append(bid)
        st.markdown("---")

    col_reset, col_sample = st.columns(2)
    # Note: Streamlit sliders can't be reset programmatically without session state tricks,
    # so we provide instructions instead
    st.caption("💡 Tip: Try setting bids on the high-quality floral keywords first!")


# ─── Run Simulation ───
results = simulate(KEYWORDS, bids)

# ─── Totals ───
total_imp = sum(r["Impressions"] for r in results)
total_clicks = sum(r["Clicks"] for r in results)
total_cost = sum(r["Total Cost"] for r in results)
total_conv = sum(r["Conversions"] for r in results)
total_cpa = total_cost / total_conv if total_conv > 0 else None
total_roas = (MARGIN_PER_CONVERSION - total_cpa) / total_cpa if total_cpa and total_cpa > 0 else None


# ─── TAB 1: Simulator ───
with tab_sim:
    # Summary metrics
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Impressions", f"{total_imp:,}")
    m2.metric("Clicks", f"{total_clicks:,}")
    m3.metric("Conversions", f"{total_conv:,}")
    m4.metric("Total Cost", f"${total_cost:,.2f}")
    m5.metric("ROAS", f"{total_roas:.1%}" if total_roas is not None else "—")

    # Budget bar
    budget_pct = min(total_cost / BUDGET * 100, 100)
    st.progress(budget_pct / 100, text=f"Budget used: ${total_cost:,.0f} / ${BUDGET:,} ({budget_pct:.0f}%)")

    st.markdown("---")

    # Results table
    st.markdown("### 📋 Keyword Performance Results")

    table_data = []
    for kw, r in zip(KEYWORDS, results):
        active = r["Clicks"] > 0
        table_data.append({
            "Keyword": kw["keyword"],
            "Competition": kw["competition"],
            "Your Bid": f"${bids[KEYWORDS.index(kw)]:.2f}",
            "Impressions": f"{r['Impressions']:,}",
            "Top Imp. %": f"{r['Top Imp. Rate']:.1%}" if active else "—",
            "CTR": f"{r['CTR']:.2%}" if active else "—",
            "Clicks": f"{r['Clicks']:,}",
            "Avg CPC": f"${r['Avg CPC']:.2f}" if active else "—",
            "Total Cost": f"${r['Total Cost']:,.2f}",
            "Conversions": r["Conversions"],
            "CPA": f"${r['CPA']:.2f}" if r["CPA"] else "—",
            "ROAS": f"{r['ROAS']:.1%}" if r["ROAS"] is not None else "—",
        })

    df_display = pd.DataFrame(table_data)
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        height=440,
    )

    # Totals row
    tc1, tc2, tc3, tc4, tc5 = st.columns(5)
    tc1.markdown(f"**Total Impressions:** {total_imp:,}")
    tc2.markdown(f"**Total Clicks:** {total_clicks:,}")
    tc3.markdown(f"**Total Cost:** ${total_cost:,.2f}")
    tc4.markdown(f"**Total Conversions:** {total_conv:,}")
    tc5.markdown(f"**Avg CPA:** {'${:.2f}'.format(total_cpa) if total_cpa else '—'}")

    st.markdown("---")

    # Performance Feedback
    st.markdown("### 🎯 Performance Feedback")

    fb1, fb2 = st.columns(2)

    with fb1:
        # Clicks feedback
        if total_clicks >= 7200:
            st.markdown('<div class="feedback-good">✅ <b>Clicks:</b> Great click volume!</div>', unsafe_allow_html=True)
        elif total_clicks >= 6000:
            st.markdown('<div class="feedback-ok">➡️ <b>Clicks:</b> Good volume, but push for more clicks.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="feedback-bad">❌ <b>Clicks:</b> Drive more clicks! Increase bids on high-quality keywords.</div>', unsafe_allow_html=True)

        st.markdown("")

        # Budget feedback
        if total_cost >= 4500:
            st.markdown('<div class="feedback-good">✅ <b>Budget:</b> You\'ve deployed almost all your budget!</div>', unsafe_allow_html=True)
        elif total_cost >= 3000:
            st.markdown('<div class="feedback-ok">➡️ <b>Budget:</b> Using budget — try to deploy the full $5,000.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="feedback-bad">❌ <b>Budget:</b> You haven\'t used much of your budget.</div>', unsafe_allow_html=True)

    with fb2:
        # Conversions feedback
        if total_conv >= 310:
            st.markdown('<div class="feedback-good">✅ <b>Conversions:</b> Excellent conversions!</div>', unsafe_allow_html=True)
        elif total_conv >= 290:
            st.markdown('<div class="feedback-ok">➡️ <b>Conversions:</b> Close to target — optimize further.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="feedback-bad">❌ <b>Conversions:</b> Drive more conversions! Focus on high-conversion keywords.</div>', unsafe_allow_html=True)

        st.markdown("")

        # ROAS feedback
        if total_roas is not None and total_roas >= 0.18:
            st.markdown('<div class="feedback-good">✅ <b>ROAS:</b> Strong return on ad spend!</div>', unsafe_allow_html=True)
        elif total_roas is not None and total_roas >= 0:
            st.markdown('<div class="feedback-ok">➡️ <b>ROAS:</b> Profitable, but can be improved.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="feedback-bad">❌ <b>ROAS:</b> Not profitable — you\'re losing money on ads.</div>', unsafe_allow_html=True)


# ─── TAB 2: Keyword Reference ───
with tab_ref:
    st.markdown("### 🔍 Keyword Research Data")
    st.markdown("Use this reference data to inform your bidding strategy.")
    st.markdown("")

    ref_data = []
    for kw in KEYWORDS:
        ref_data.append({
            "Keyword": kw["keyword"],
            "Competition": kw["competition"],
            "Top-of-Page Bid": f"${kw['top_bid']:.2f}",
            "Avg Monthly Searches": f"{kw['avg_monthly']:,}",
            "Quality Score": f"{kw['quality']}/10",
            "Conv. Rate": f"{kw['conv_rate']:.1%}",
        })

    st.dataframe(
        pd.DataFrame(ref_data),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")
    st.markdown("#### 💡 Strategy Tips")

    st.info("""
    **High Quality Score (9-10)** keywords like *floral tie*, *pink floral tie*, and *floral wedding tie* 
    give you the best bang for your buck — they earn more impressions and higher CTR per dollar bid.

    **High Conversion Rate** keywords like *floral tie for sale* (25%) and *pink floral tie* (16%) 
    convert visitors into customers at much higher rates.

    **Low Competition** keywords like *how to tie a tie* have massive volume but very low conversion rates (1.6%) — 
    they're cheap but may not drive purchases.
    """)


# ─── TAB 3: Glossary ───
with tab_glossary:
    st.markdown("### 📖 Glossary of Terms")
    st.markdown("")

    glossary = {
        "CPC Bid": "The maximum amount you're willing to pay per click on an ad.",
        "Quality Score": "Google's rating (1–10) based on ad relevance, expected CTR, and landing page experience. Higher scores mean better ad placement at lower costs.",
        "Impressions": "The total number of times your ad appears in search results.",
        "Search Top Impression Rate": "The percentage of times your ad appears in the top positions of search results.",
        "CTR (Click-Through Rate)": "The percentage of impressions that result in a click. Calculated as Clicks ÷ Impressions.",
        "Avg. CPC (Cost per Click)": "The average amount you actually pay per click — equals your bid in this simulation.",
        "Total Cost": "Your total advertising expenditure (CPC × Clicks). Automatically capped at the $5,000 budget.",
        "Conversions": "The number of desired actions completed (e.g., purchases). Driven by the keyword's conversion rate.",
        "Conversion Rate": "The percentage of clicks that result in a conversion. Calculated as Conversions ÷ Clicks.",
        "CPA (Cost per Acquisition)": "The cost of acquiring one customer. Calculated as Total Cost ÷ Conversions.",
        "ROAS (Return on Ad Spend)": "Measures profitability: (Margin per Conversion − CPA) ÷ CPA. Positive means profitable, negative means losing money.",
        "Budget": "The $5,000 spending cap. If your total spend would exceed this, impressions and clicks are scaled down proportionally across all keywords.",
    }

    for term, definition in glossary.items():
        with st.expander(f"**{term}**"):
            st.markdown(definition)
