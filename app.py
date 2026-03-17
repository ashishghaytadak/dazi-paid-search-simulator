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
    raw_rows = []
    for kw, bid in zip(keywords, bids):
        F = bid
        G = kw["quality"]
        D = kw["top_bid"]
        C = kw["comp_score"]
        E = kw["avg_monthly"]
        S = kw["conv_rate"]

        if G * F > D * C:
            impressions0 = round((G * F / (D * 11)) * 0.5 * E)
        else:
            impressions0 = 0

        if F * G > D * C:
            top_rate = min(F * G / (D * C / 3.5 * 10), 0.98)
        else:
            top_rate = 0.0

        q_mult = 5 if G > 9 else (2 if G > 7 else 1)
        ctr = top_rate * 0.14 / C * q_mult
        clicks0 = round(impressions0 * ctr)

        raw_rows.append({
            "impressions0": impressions0, "top_rate": top_rate, "ctr": ctr,
            "clicks0": clicks0, "bid": F, "conv_rate": S,
        })

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
            "Impressions": impressions, "Top Imp. Rate": r["top_rate"], "CTR": r["ctr"],
            "Clicks": clicks, "Avg CPC": avg_cpc, "Total Cost": total_cost,
            "Conversions": conversions, "Conv. Rate": r["conv_rate"], "CPA": cpa, "ROAS": roas,
        })
    return results


# ─── Custom CSS ───
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
    .stApp { font-family: 'DM Sans', sans-serif; }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid rgba(148,163,184,0.12); border-radius: 14px; padding: 18px 20px;
    }
    div[data-testid="stMetric"] label {
        color: #64748b !important; font-size: 12px !important; font-weight: 600 !important;
        text-transform: uppercase; letter-spacing: 0.06em;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #f1f5f9 !important; font-size: 26px !important; font-weight: 700 !important;
    }
    .feedback-good {
        background: rgba(5,150,105,0.12); border: 1px solid rgba(5,150,105,0.25);
        border-radius: 10px; padding: 12px 16px; color: #34d399; font-weight: 600;
    }
    .feedback-ok {
        background: rgba(245,158,11,0.12); border: 1px solid rgba(245,158,11,0.25);
        border-radius: 10px; padding: 12px 16px; color: #fbbf24; font-weight: 600;
    }
    .feedback-bad {
        background: rgba(220,38,38,0.12); border: 1px solid rgba(220,38,38,0.25);
        border-radius: 10px; padding: 12px 16px; color: #f87171; font-weight: 600;
    }
    .big-header { font-size: 28px; font-weight: 700; color: #f1f5f9; letter-spacing: -0.02em; margin-bottom: 4px; }
    .sub-header { font-size: 14px; color: #64748b; margin-bottom: 24px; }
    .section-title { font-size: 18px; font-weight: 700; color: #f1f5f9; margin: 16px 0 10px 0; }
    section[data-testid="stSidebar"] { background: #0f172a; }
    .keyword-label { font-size: 15px; font-weight: 700; color: #f1f5f9; margin-bottom: 2px; }
    .keyword-info { font-size: 12px; color: #94a3b8; margin-bottom: 6px; }
    .ad-copy-box { background: #fff; border-radius: 12px; padding: 16px 20px; margin-bottom: 16px; border: 1px solid #e2e8f0; }
    .ad-label { font-size: 11px; color: #5f6368; font-weight: 600; display: inline-block; background: #f1f3f4; padding: 1px 6px; border-radius: 4px; margin-right: 6px; }
    .ad-headline { font-size: 18px; color: #1a0dab; font-weight: 400; margin-bottom: 4px; }
    .ad-description { font-size: 13px; color: #4d5156; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)

# ─── Header ───
st.markdown('<div class="big-header">🎯 DAZI Paid Search Simulator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Floral Tie Campaign — Adjust your keyword bids in the sidebar and watch results update in real time.</div>', unsafe_allow_html=True)

# ─── Tabs ───
tab_sim, tab_ref, tab_ads, tab_glossary = st.tabs(["📊 Bid Simulator", "🔍 Keyword Research", "📢 Ad Group: Floral Ties", "📖 Glossary"])

# ─── Sidebar ───
with st.sidebar:
    st.markdown("## 💰 Set Your Bids")
    st.markdown(f"**Budget:** ${BUDGET:,}")
    st.divider()
    bids = []
    for i, kw in enumerate(KEYWORDS):
        comp_icon = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}[kw["competition"]]
        st.markdown(f'<div class="keyword-label">{comp_icon} {kw["keyword"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="keyword-info">Top bid: ${kw["top_bid"]:.2f} &nbsp;·&nbsp; Quality: {kw["quality"]}/10 &nbsp;·&nbsp; Vol: {kw["avg_monthly"]:,}</div>', unsafe_allow_html=True)
        bid = st.slider(f"CPC Bid for {kw['keyword']}", 0.0, round(max(kw["top_bid"] * 2.5, 3.0), 2), 0.0, 0.01, format="$%.2f", key=f"bid_{i}", label_visibility="collapsed")
        bids.append(bid)
        st.markdown("---")
    st.caption("💡 Tip: Focus bids on high-quality floral keywords first for the best ROAS!")

# ─── Run Simulation ───
results = simulate(KEYWORDS, bids)
total_imp = sum(r["Impressions"] for r in results)
total_clicks = sum(r["Clicks"] for r in results)
total_cost = sum(r["Total Cost"] for r in results)
total_conv = sum(r["Conversions"] for r in results)
total_ctr = total_clicks / total_imp if total_imp > 0 else 0
total_conv_rate = total_conv / total_clicks if total_clicks > 0 else 0
total_cpa = total_cost / total_conv if total_conv > 0 else None
total_roas = (MARGIN_PER_CONVERSION - total_cpa) / total_cpa if total_cpa and total_cpa > 0 else None

# ─── TAB 1: Simulator ───
with tab_sim:
    st.markdown('<div class="section-title">Summary of Simulation Results</div>', unsafe_allow_html=True)
    m1, m2, m3, m4, m5, m6, m7 = st.columns(7)
    m1.metric("Impressions", f"{total_imp:,}")
    m2.metric("Clicks", f"{total_clicks:,}")
    m3.metric("CTR", f"{total_ctr:.2%}")
    m4.metric("Conversions", f"{total_conv:,}")
    m5.metric("Conv. Rate", f"{total_conv_rate:.2%}")
    m6.metric("Total Cost", f"${total_cost:,.2f}")
    m7.metric("ROAS", f"{total_roas:.1%}" if total_roas is not None else "—")

    budget_pct = min(total_cost / BUDGET * 100, 100)
    st.progress(budget_pct / 100, text=f"Budget used: ${total_cost:,.0f} / ${BUDGET:,} ({budget_pct:.0f}%)")

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
        if total_roas is not None and total_roas >= 0.18:
            st.markdown('<div class="feedback-good">✅ <b>ROAS:</b> Strong return on ad spend!</div>', unsafe_allow_html=True)
        elif total_roas is not None and total_roas >= 0:
            st.markdown('<div class="feedback-ok">➡️ <b>ROAS:</b> Profitable, but can be improved.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="feedback-bad">❌ <b>ROAS:</b> Not profitable — you\'re losing money on ads.</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-title">Keyword Performance Results</div>', unsafe_allow_html=True)

    table_data = []
    for kw, r in zip(KEYWORDS, results):
        active = r["Clicks"] > 0
        table_data.append({
            "Keyword": kw["keyword"],
            "Top Bid": f"${kw['top_bid']:.2f}",
            "Monthly Vol.": f"{kw['avg_monthly']:,}",
            "Quality": kw["quality"],
            "Your Bid": f"${bids[KEYWORDS.index(kw)]:.2f}",
            "Impressions": f"{r['Impressions']:,}",
            "Top Imp. %": f"{r['Top Imp. Rate']:.1%}" if active else "—",
            "CTR": f"{r['CTR']:.2%}" if active else "—",
            "Clicks": f"{r['Clicks']:,}",
            "Avg CPC": f"${r['Avg CPC']:.2f}" if active else "—",
            "Total Cost": f"${r['Total Cost']:,.2f}",
            "Conversions": r["Conversions"],
            "Conv. Rate": f"{r['Conversions']/r['Clicks']:.1%}" if r["Clicks"] > 0 else "—",
            "CPA": f"${r['CPA']:.2f}" if r["CPA"] else "—",
            "ROAS": f"{r['ROAS']:.1%}" if r["ROAS"] is not None else "—",
        })
    st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True, height=440)

    tc1, tc2, tc3, tc4, tc5 = st.columns(5)
    tc1.markdown(f"**Total Impressions:** {total_imp:,}")
    tc2.markdown(f"**Total Clicks:** {total_clicks:,}")
    tc3.markdown(f"**Total Cost:** ${total_cost:,.2f}")
    tc4.markdown(f"**Total Conversions:** {total_conv:,}")
    tc5.markdown(f"**Avg CPA:** {'${:.2f}'.format(total_cpa) if total_cpa else '—'}")

# ─── TAB 2: Keyword Research ───
with tab_ref:
    st.markdown('<div class="section-title">Keyword Research Data</div>', unsafe_allow_html=True)
    st.markdown("Use this reference data to inform your bidding strategy.")
    st.markdown("")
    ref_df = pd.DataFrame({
        "Keyword": [kw["keyword"] for kw in KEYWORDS],
        "Competition": [kw["competition"] for kw in KEYWORDS],
        "Top-of-Page Bid": [kw["top_bid"] for kw in KEYWORDS],
        "Avg Monthly Searches": [kw["avg_monthly"] for kw in KEYWORDS],
        "Quality Score": [kw["quality"] for kw in KEYWORDS],
    })
    st.dataframe(ref_df, use_container_width=True, hide_index=True,
        column_config={
            "Top-of-Page Bid": st.column_config.NumberColumn(format="$%.2f"),
            "Avg Monthly Searches": st.column_config.NumberColumn(format="%d"),
            "Quality Score": st.column_config.NumberColumn(format="%d/10"),
        })

# ─── TAB 3: Ads & Landing Page ───
with tab_ads:
    st.markdown('<div class="section-title">Ad Group: Floral Ties</div>', unsafe_allow_html=True)
    st.markdown(f"**Landing page:** [www.daziusa.com/collections/floral](https://www.daziusa.com/collections/floral)")
    st.markdown("")
    st.markdown('<div class="section-title">Ad Copy Examples</div>', unsafe_allow_html=True)
    col_ad1, col_ad2 = st.columns(2)
    with col_ad1:
        st.markdown("""
        <div class="ad-copy-box">
            <div><span class="ad-label">Ad</span> <span style="font-size:13px; color:#1a1a1a;">https://www.daziusa.com/neckties/floral</span></div>
            <div class="ad-headline">Shop Floral Ties For Weddings - Free Shipping On Orders $40+</div>
            <div class="ad-description">Browse Our Original <b>Floral Ties</b>, <b>Floral</b> Bow <b>Ties</b>, And Other Essentials. Shop DAZI® Today! Free Shipping Over $40. Best Quality. Great For <b>Weddings</b>. Styles: White <b>Floral</b>, Blue Bloom.</div>
        </div>""", unsafe_allow_html=True)
    with col_ad2:
        st.markdown("""
        <div class="ad-copy-box">
            <div><span class="ad-label">Ad</span> <span style="font-size:13px; color:#1a1a1a;">https://www.daziusa.com/neckties/floral</span></div>
            <div class="ad-headline">Shop Floral Ties - DAZI® Original Floral Ties - daziusa.com</div>
            <div class="ad-description">Browse Our Original <b>Floral Ties</b>, <b>Floral</b> Bow <b>Ties</b>, And More. Shop & Save Today! Best Quality.</div>
        </div>""", unsafe_allow_html=True)
    st.markdown("")
    st.markdown('<div class="section-title">Landing Page Preview</div>', unsafe_allow_html=True)
    st.markdown("The ads direct users to the DAZI floral ties collection page:")
    st.markdown("""
    <div style="background: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0;">
        <div style="background: #333; color: #fff; padding: 14px 24px; display: flex; align-items: center; gap: 24px; font-size: 13px;">
            <span style="font-size: 22px; font-weight: 700; letter-spacing: 0.05em; font-family: serif;">DAZI</span>
            <span>NECKTIES</span><span>BOW TIES</span><span>SWATCHES</span><span>ACCESSORIES</span><span>NEW ARRIVALS</span><span>WEDDINGS</span>
        </div>
        <div style="padding: 24px; text-align: center;">
            <div style="font-size: 12px; color: #888; margin-bottom: 8px;">Home > Floral > Page 1 of 2</div>
            <div style="font-size: 24px; font-weight: 700; color: #333; margin-bottom: 20px;">FLORAL</div>
            <div style="display: flex; justify-content: center; gap: 30px; flex-wrap: wrap;">
                <div style="text-align: center;"><div style="width: 180px; height: 180px; background: linear-gradient(135deg, #f5e6e0, #e8d5c8); border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-bottom: 10px;"><span style="font-size: 40px;">🌸</span></div><div style="font-size: 14px; color: #333; font-weight: 600;">Quicksand Roses</div><div style="font-size: 12px; color: #f5a623;">★★★★★ <span style="color: #888;">68 reviews</span></div><div style="font-size: 16px; color: #333; font-weight: 700;">$32.00</div></div>
                <div style="text-align: center;"><div style="width: 180px; height: 180px; background: linear-gradient(135deg, #e0f0e0, #c8e8c8); border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-bottom: 10px;"><span style="font-size: 40px;">🌿</span></div><div style="font-size: 14px; color: #333; font-weight: 600;">Hidden Garden</div><div style="font-size: 12px; color: #f5a623;">★★★★★ <span style="color: #888;">31 reviews</span></div><div style="font-size: 16px; color: #333; font-weight: 700;">$32.00</div></div>
                <div style="text-align: center;"><div style="width: 180px; height: 180px; background: linear-gradient(135deg, #e0e5f0, #c8d5e8); border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-bottom: 10px;"><span style="font-size: 40px;">💐</span></div><div style="font-size: 14px; color: #333; font-weight: 600;">Scorpion Grass</div><div style="font-size: 12px; color: #f5a623;">★★★★★ <span style="color: #888;">2 reviews</span></div><div style="font-size: 16px; color: #333; font-weight: 700;">$32.00</div></div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)
    st.markdown("")
    st.caption("Landing page: www.daziusa.com/collections/floral — Products priced at $32.00 each")

# ─── TAB 4: Glossary ───
with tab_glossary:
    st.markdown('<div class="section-title">Glossary of Terms</div>', unsafe_allow_html=True)
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
        "ROAS (Return on Ad Spend)": "Profitability measure: (Margin − CPA) ÷ CPA. Positive = profitable.",
        "Budget": "The $5,000 cap. If spend exceeds this, everything scales down proportionally.",
    }.items():
        with st.expander(f"**{term}**"):
            st.markdown(defn)
