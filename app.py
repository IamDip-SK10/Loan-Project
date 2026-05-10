import streamlit as st
from style import load_css

# ---------------------------
# CONFIG + CSS
# ---------------------------
st.set_page_config(page_title="Loan AI System", layout="wide")
load_css(st)
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
# HEADER (PREMIUM TOUCH)
# ---------------------------
st.markdown("""
<div class="glass header-glass">
    <h1>🛡️ Loan AI System</h1>
    <p>Advanced Loan Decision & Analytics Platform</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# INTRO (HYBRID SYSTEM)
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.markdown("### 📘 What is Loan AI System?")

st.info("""
This platform simulates how real banks evaluate loan applications through a **Hybrid Decision Framework**:

1. **Prediction** → Machine Learning estimates approval probability  
2. **Governance** → Banking policies override risky approvals (Credit Score, DTI, LTV)  
3. **Consultation** → 'What-If Engine' guides users to improve eligibility  

💡 This ensures decisions are not just intelligent, but also financially safe and compliant.
""")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# FEATURES (REFINED UX + GEMINI PRO TERMS)
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.markdown("### 🚀 Platform Capabilities")

colA, colB = st.columns(2)

with colA:
    st.markdown("#### 🛡️ Risk Management")

    st.write("● **Probability Modeling:** AI-driven approval estimation")
    st.write("● **Policy Guardrails:** Credit Score, DTI & LTV enforcement")
    st.write("● **Compliance Logic:** Final decision governed by banking rules")
    st.write("● **Risk Governance Engine:** AI + banking policy validation")
    st.write("● **Risk Classification:** Low / Moderate / High Risk segmentation")

with colB:
    st.markdown("#### 📈 Customer Advisory")

    st.write("● **Scenario Analysis:** Dynamic 'What-If' simulations")
    st.write("● **Actionable Insights:** Understand rejection reasons")
    st.write("● **Optimization Engine:** Improve approval chances")
    st.write("● **AI Transparency Layer:** Decision explanation & top drivers")
    st.write("● **Executive PDF Reporting:** Enterprise-style governance reports")

st.markdown("---")

st.markdown("#### 🧭 Core System Workflow")

st.markdown("""
1. **[AI Prediction Engine]** → Multi-factor approval probability  
2. **[Risk Governance Layer]** → Credit Score, DTI & LTV validation  
3. **[Decision Intelligence]** → AI transparency & decision breakdown  
4. **[Financial Advisory Engine]** → Smart recommendations & simulations  
5. **[Analytics Dashboard]** → Risk visualization & affordability analysis  
6. **[Enterprise PDF Generator]** → Official governance & approval report  
""")

st.markdown('</div>', unsafe_allow_html=True)
# ---------------------------
# 💳 CREDIT SCORE
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.markdown("### 💳 What is Credit Score?")

st.write("""
A Credit Score (300–900) represents your creditworthiness.

- Repayment history  
- Credit card usage  
- Loan history  
- Credit inquiries  
""")

st.success("""
✔ 750+ → Excellent  
✔ 650–750 → Moderate  
✔ <650 → Risky  
""")

st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------
# 📊 DTI SECTION
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.markdown("### 📊 What is DTI (Debt-to-Income Ratio)?")

st.write("DTI shows how much of your income goes into loan repayment.")

st.latex(r"DTI = \frac{Monthly\ EMI}{Monthly\ Income}")

st.info("""
✔ <0.30 → Healthy  
✔ 0.30–0.50 → Moderate Risk  
✔ >0.50 → High Risk  
""")

st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------
# 💰 EMI SECTION
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.markdown("### 💰 What is EMI?")

st.write("""
EMI is the fixed amount paid monthly to repay a loan.

Depends on:
- Loan amount  
- Interest rate  
- Loan tenure  
""")

st.latex(r"EMI = \frac{P \cdot r \cdot (1+r)^n}{(1+r)^n - 1}")

st.info("""
✔ Higher tenure → Lower EMI  
✔ Higher interest → Higher EMI  
""")

st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------
# 🏦 BANK DECISION
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.markdown("### 🏦 How Banks Decide Loan Approval")

st.info("""
Banks evaluate:

✔ Income stability  
✔ Credit score  
✔ Debt burden (DTI)  
✔ Employment type  
✔ Loan vs income ratio  
✔ Collateral strength (Asset Value & LTV)

👉 Even one weak factor can lead to rejection  
""")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# 🔍 AI TRANSPARENCY
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.markdown("### 🔍 AI Transparency & Governance")

st.write("""
Modern banking systems require AI decisions to be explainable and auditable.

This platform includes:
""")

st.success("""
✔ AI Decision Breakdown  
✔ Top Approval Drivers  
✔ Risk Classification Engine  
✔ Governance Validation Layer  
✔ Financial Affordability Analysis  
✔ Banking Policy Compliance Logic  
✔ Decision Confidence Scoring  
""")

st.info("""
💡 The system ensures that loan approvals are not purely AI-driven,  
but validated using real-world banking governance principles.
""")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# 🏠 LTV & ASSET (NEW 🔥)
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.markdown("### 🏠 What is Asset Value & LTV (Loan-to-Value Ratio)?")

st.write("""
**Asset Value** is the market value of the property or collateral (house, land, etc.)  
used as security for the loan.

Banks rely on assets to reduce risk — if a borrower defaults,  
the asset can recover the loan amount.

**LTV (Loan-to-Value Ratio)** shows how much loan is taken relative to the asset value.
""")

st.latex(r"LTV = \frac{Loan\ Amount}{Asset\ Value}")

st.info("""
✔ LTV ≤ 0.70 → Low Risk (Strong collateral)  
✔ 0.70–0.90 → Moderate Risk  
✔ >0.90 → High Risk (Low security)  

💡 Lower LTV increases approval chances  
💡 Strong collateral can override high DTI or moderate credit risk  
""")

st.markdown('</div>', unsafe_allow_html=True)
# ---------------------------
# ORIGINAL USER JOURNEY (WITH ONE PRO UPGRADE)
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.markdown("### 🚀 What You Can Do")

st.write("""
👉 Go to **Decision Page** → Apply & simulate loan approval  
👉 Go to **Analytics Page** → Understand financial insights  

---

### 🧭 User Journey

#### 🧠 Step 1: Prediction Engine
✔ **Proprietary ML Model:** Predictive scoring for creditworthiness  
✔ Approval Probability Score  

#### 🏦 Step 2: Banking Governance Layer
✔ Credit Score Hard Rules  
✔ DTI (Debt-to-Income) Risk Filtering  
✔ LTV (Loan-to-Value) Collateral Logic  
✔ Policy Override System (AI ≠ Final Decision)

#### 🔮 Step 3: Financial Advisory Engine
✔ What-If Simulation (Income vs Loan adjustment)  
✔ Dynamic Eligibility Recalculation  
✔ Real-Time Risk Adjustment  
✔ AI-Based Loan Optimization Suggestions  
✔ Smart Recommendations to improve approval  
✔ Loan Eligibility Estimation  

#### 📊 Step 4: Analytics Dashboard
✔ EMI vs Income Comparison  
✔ Loan Burden Distribution  
✔ AI Decision Contribution Analysis  
✔ Risk Visualization (DTI + LTV)  
✔ Transparency & Confidence Insights  
✔ Strategic Decision Recommendations  
✔ Risk Governance Summary  

#### 📄 Step 5: Enterprise PDF Reporting Included
✔ Official Loan Evaluation Summary  
✔ AI Governance Reports  
✔ Risk Analysis Documentation  
✔ Financial Snapshot Reports  
✔ Decision Transparency Summaries  
✔ Loan Affordability Analysis  

---

💡 This system replicates real-world **bank underwriting systems** by combining  
Machine Learning + Financial Policy + User Advisory.
""")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# NAVIGATION BUTTONS (WITH TOOLTIPS)
# ---------------------------
col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.page_link(
        "pages/1_Decision.py",
        label="➡ Decision Page",
        help="Start loan evaluation"
    )

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# FOOTER (ENTERPRISE STYLE)
# ---------------------------
st.markdown("---")
st.caption("© 2026 FinWithDip | AI Loan Decision & Credit Risk Platform | Developed by Subhadip")