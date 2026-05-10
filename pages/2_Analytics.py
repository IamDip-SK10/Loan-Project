import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from style import load_css

# ---------------------------
# CONFIG
# ---------------------------
st.set_page_config(page_title="Analytics", layout="wide")
load_css(st)
# ---------------------------
# HELPERS
# ---------------------------
def format_inr(x):
    if x >= 100000:
        return f"₹{x/100000:.2f} Lakh"
    return f"₹{x:,.0f}"

def get_dti_color(dti):
    if dti < 0.3:
        return "green"
    elif dti < 0.5:
        return "orange"
    else:
        return "red"
# ---------------------------
# SIDEBAR LOGO
# ---------------------------
st.sidebar.image("financelogo.png", width=220)
st.sidebar.markdown("<br>", unsafe_allow_html=True)
# ---------------------------
# SIDEBAR NAV (UPDATED LABEL)
# ---------------------------
st.sidebar.markdown("## 📍 System Menu")
st.sidebar.page_link("app.py", label="🏠 Home")
st.sidebar.page_link("pages/1_Decision.py", label="🏦 Decision")
st.sidebar.page_link("pages/2_Analytics.py", label="📊 Analytics")

# ---------------------------
# HEADER
# ---------------------------
st.markdown("""
<div class="glass header-glass">
    <h1>📊 Loan Analytics Dashboard</h1>
    <p>Financial Insights & Risk Breakdown</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# DATA CHECK
# ---------------------------
if not st.session_state.get("loan_result"):
    st.warning("⚠ Run prediction first")
    st.stop()

data = st.session_state["loan_result"]

# ---------------------------
# COLORS
# ---------------------------
GREEN = "#2ecc71"
RED = "#e74c3c"
BLUE = "#3498db"
ORANGE = "#f39c12"

# ---------------------------
# KPI (FIXED + LTV ADDED)
# ---------------------------
st.subheader("📌 Applicant Overview")

c1, c2, c3 = st.columns(3)

c1.metric("Income", format_inr(data['income']))
c2.metric("Loan", format_inr(data['loan']))
c3.metric("Credit Score", data['credit_score'])

c4, c5, c6 = st.columns(3)
c4.metric("DTI Ratio", f"{data['dti']:.2f}")
c5.metric("Monthly EMI", format_inr(data['emi']))
c6.metric("LTV Ratio", f"{data.get('ltv', 0):.2f}")

# ---------------------------
# 🔥 GAUGE SECTION (DTI + PROB + LTV)
# ---------------------------
colG1, colG2, colG3 = st.columns(3)

with colG1:
    st.subheader("📉 DTI Gauge")

    fig, ax = plt.subplots(figsize=(3.5, 2))

    dti = data["dti"]

    color_map = {
        "green": GREEN,
        "orange": ORANGE,
        "red": RED
    }

    color = color_map[get_dti_color(dti)]

    ax.barh(["DTI"], [dti], color=color)

    # ✅ DTI SCALE
    ax.set_xlim(0, 2)

    # ✅ CENTER VALUE
    ax.text(
        dti / 2,
        0,
        f"{dti:.2f}",
        ha='center',
        va='center',
        color='black',
        fontsize=12,
        fontweight='bold'
    )

    fig.tight_layout()

    st.pyplot(fig, width="content")


with colG2:
    st.subheader("🎯 Approval Probability")

    prob = data["prob"]

    fig2, ax2 = plt.subplots(figsize=(3.5, 2))

    ax2.barh(["Probability"], [prob * 100], color=BLUE)

    ax2.set_xlim(0, 100)

    ax2.text(
        50,
        0,
        f"{prob * 100:.1f}%",
        ha='center',
        va='center',
        color='black',
        fontsize=12,
        fontweight='bold'
    )

    fig2.tight_layout()

    st.pyplot(fig2, width="content")


with colG3:
    st.subheader("🏠 LTV Gauge")

    ltv = data.get("ltv", 0)

    fig6, ax6 = plt.subplots(figsize=(3.5, 2))

    color = RED if ltv > 0.9 else ORANGE if ltv > 0.7 else GREEN

    ax6.barh(["LTV"], [ltv], color=color)

    # ✅ LTV SCALE
    ax6.set_xlim(0, )

    # ✅ CENTER VALUE
    ax6.text(
        ltv / 3,
        0,
        f"{ltv:.2f}",
        ha='center',
        va='center',
        color='black',
        fontsize=12,
        fontweight='bold'
    )

    fig6.tight_layout()

    st.pyplot(fig6, width="content")

# ---------------------------
# RISK BLOCK (UNCHANGED STYLE)
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.subheader("📌 Risk Level Analysis")

col1, col2 = st.columns([2, 1])

with col1:

    dti_ratio = data["dti"]

    fig3, ax3 = plt.subplots(figsize=(5, 2.8))

    categories = ["Safe Limit", "Your DTI"]
    values = [0.40, dti_ratio]

    colors = [
        GREEN,
        GREEN if dti_ratio < 0.3
        else ORANGE if dti_ratio < 0.6
        else RED
    ]

    bars = ax3.bar(
        categories,
        values,
        color=colors
    )

    ax3.set_ylim(0, 2)

    ax3.set_ylabel("")

    ax3.set_title("Loan Eligibility Comparison")

    for bar in bars:

        height = bar.get_height()

        ax3.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.03,
            f"{height:.2f}",
            ha='center',
            fontsize=11,
            fontweight='bold'
        )

    fig3.tight_layout()

    st.pyplot(fig3, width="content")

with col2:

    st.markdown("### 🧾 Risk Summary")

    if dti_ratio < 0.3:

        st.success("✅ Low Risk Applicant")
        st.info("Strong repayment capacity")

    elif dti_ratio < 0.6:

        st.warning("⚠️ Moderate Risk Applicant")
        st.info("Requires careful review")

    else:

        st.error("❌ High Risk Applicant")
        st.info("Higher default probability")

    safe_loan = st.session_state["form_data"].get("safe_loan", 0)
    loan = st.session_state["form_data"].get("loan", 0)

    st.metric(
        label="💰 Applied Loan Amount",
        value=f"₹{loan / 100000:.2f} Lakh"
    )

    st.metric(
        label="✅ Suggested Safe Loan Limit",
        value=f"₹{safe_loan / 100000:.2f} Lakh"
    )

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# BAR + PIE (UNCHANGED STYLE)
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

colL, colR = st.columns(2)

monthly_income = data["income"] / 12 if data["income"] else 0
remaining_income = max(monthly_income - data["emi"], 0)

# =========================
# EMI VS INCOME
# =========================
with colL:
    st.subheader("⚖️ EMI vs Income")

    fig4, ax4 = plt.subplots(figsize=(4.2, 3.2))

    bars = ax4.bar(
        ["Income", "EMI"],
        [monthly_income, data["emi"]],
        color=[GREEN, RED],
        width=0.55
    )

    for bar in bars:
        height = bar.get_height()

        ax4.text(
            bar.get_x() + bar.get_width()/2,
            height + 800,
            f"₹{height:,.0f}",
            ha='center',
            fontsize=10,
            fontweight='bold'
        )

    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)

    fig4.tight_layout()

    st.pyplot(fig4, width="content")
    plt.savefig("emi_vs_income.png", bbox_inches="tight")


# =========================
# LOAN BURDEN
# =========================

with colR:
    st.subheader("📉 Loan Burden")

    fig5, ax5 = plt.subplots(figsize=(4.2, 3.2))

    ax5.pie(
        [data["emi"], remaining_income],
        labels=["EMI", "Remaining"],
        autopct='%1.1f%%',
        startangle=90,
        radius=0.88,
        colors=[RED, GREEN],
        textprops={
            'fontsize': 10,
            'fontweight': 'bold'
        }
    )

    ax5.set_aspect('equal')

    fig5.tight_layout()

    st.pyplot(fig5, width="content")

# ---------------------------
# AI DECISION TRANSPARENCY
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.subheader("🔍 AI Decision Transparency")

# ---------------------------
# CREDIT SCORE ANALYSIS
# ---------------------------
if data["credit_score"] > 750:

    st.success(
        "✅ Excellent credit history increased approval confidence"
    )

elif data["credit_score"] >= 650:

    st.info(
        "ℹ Good credit profile supported lending trust"
    )

else:

    st.warning(
        "⚠ Low credit score reduced approval strength"
    )
plt.savefig("loan_burden.png", bbox_inches="tight")

# ---------------------------
# DTI ANALYSIS
# ---------------------------
if data["dti"] > 0.60:

    st.warning(
        "⚠ High debt-to-income ratio increased repayment risk"
    )

elif data["dti"] < 0.30:

    st.success(
        "✅ Low debt burden improved financial stability"
    )

else:

    st.info(
        "ℹ Moderate debt obligations detected"
    )

# ---------------------------
# COLLATERAL / LTV ANALYSIS
# ---------------------------
if data.get("ltv", 0) > 0:

    if data["ltv"] <= 0.70:

        st.success(
            "🏠 Strong collateral support reduced lending risk"
        )

    elif data["ltv"] <= 0.90:

        st.info(
            "ℹ Collateral coverage is acceptable"
        )

    else:

        st.warning(
            "⚠ High LTV increased collateral exposure"
        )

# ---------------------------
# INCOME ANALYSIS
# ---------------------------
if data["income"] == 0:

    st.info(
        "📘 Student profile evaluated under education lending rules"
    )

elif data["income"] < 500000:

    st.warning(
        "⚠ Lower income profile may affect repayment capacity"
    )

else:

    st.success(
        "💰 Stable income profile strengthened affordability"
    )

# ---------------------------
# CONFIDENCE SUMMARY
# ---------------------------
st.markdown("### 📊 Confidence Summary")

if data["prob"] > 0.80:

    st.success(
        "🟢 High confidence lending profile"
    )

elif data["prob"] > 0.60:

    st.info(
        "🟡 Moderate approval confidence"
    )

else:

    st.warning(
        "🔴 Elevated lending uncertainty detected"
    )

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# FINAL DECISION
# ---------------------------
st.subheader("🏦 Final Decision")

if data["decision"] == 1:
 st.success("✅ Loan Approved")
else:
 st.warning("❌ Loan Not Approved")

st.metric("Confidence", f"{data['prob']*100:.2f}%")
# ---------------------------
# 📄 EXPORT REPORT
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.subheader("📄 Export Credit Memo")

st.info(
    "Download a professional AI-generated underwriting report "
    "with governance analysis, risk assessment, and decision transparency."
)

from pages.pdf_generator import generate_pdf

if st.button("📥 Generate PDF Credit Memo"):

    pdf_data = {
        **st.session_state.get("form_data", {}),
        **data
    }

    pdf_data["applicant_name"] = (
        st.session_state.get(
            "applicant_name",
            "Unknown User"
        )
    )

    pdf = generate_pdf(pdf_data)

    st.download_button(
        label="⬇ Download PDF Report",
        data=pdf,
        file_name="FinWithDip_Credit_Memo.pdf",
        mime="application/pdf"
    )

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.caption("© 2026 FinWithDip | AI Loan Decision & Credit Risk Platform | Developed by Subhadip")