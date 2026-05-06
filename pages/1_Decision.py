import streamlit as st
import pandas as pd
import pickle
import os
from style import load_css

# ---------------------------
# CONFIG + CSS
# ---------------------------
st.set_page_config(page_title="Loan Decision", layout="wide")
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
# SESSION STATE
# ---------------------------
if "form_data" not in st.session_state:
        st.session_state["form_data"] = {
            "age": 0,
            "income": 0.0,
            "loan": 0.0,
            "asset": 0.0,
            "credit": 0,
            "interest": 0.0,
            "years": 5
        }
# ---------------------------
# LOAD MODEL
# ---------------------------
base_path = os.path.dirname(__file__)
model_path = os.path.join(base_path, "..", "model", "model.pkl")

if os.path.exists(model_path):
    model = pickle.load(open(model_path, "rb"))
else:
    st.error("❌ Model file not found. Check /model folder.")
    st.stop()

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
    <h1>🏦 Loan Decision System</h1>
    <p>Smart AI + Banking Logic</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# INPUT SECTION
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)
error_box = st.empty()

col1, col2 = st.columns(2)

with col1:
    age = st.number_input(
        "Age",
        min_value=18,
        max_value=75,
        value=(
            st.session_state["form_data"]["age"]
            if st.session_state["form_data"]["age"] != 0
            else None
        ),
        step=1,
        placeholder="Enter your age",
        key="age_input"
    )
    employment = st.selectbox("Employment Status", ["Employed", "Self-employed", "Unemployed"])

    loan_type = st.selectbox("Loan Type", ["Personal", "Education"])

    credit_score = st.number_input(
        "Credit Score (300–900)",
        min_value=300,
        max_value=900,
        value=(
            st.session_state["form_data"]["credit"]
            if st.session_state["form_data"]["credit"] != 0
            else None
        ),
        step=1,
        placeholder="Enter your Credit Score",
        key="credit_input"
    )

with col2:
    annual_income = st.number_input(
        "Annual Income (₹)",
        min_value=0.0,
        value=(
            st.session_state["form_data"]["income"]
            if st.session_state["form_data"]["income"] != 0.0
            else None
        ),
        step=1000.0,
        placeholder="Enter your Annual Income",
        key="income_input"
    )

    # ✅ ADD THIS LINE JUST BELOW
    if annual_income:
        st.caption(f"💰 {format_inr(annual_income)}")

    loan_amount = st.number_input(
        "Loan Amount (₹)",
        min_value=0.0,
        value=(
            st.session_state["form_data"]["loan"]
            if st.session_state["form_data"]["loan"] != 0.0
            else None
        ),
        step=1000.0,
        placeholder="Enter your Loan Amount",
        key="loan_input"
    )

    # ✅ ADD THIS LINE JUST BELOW
    if loan_amount:
        st.caption(f"💰 {format_inr(loan_amount)}")

    asset_value = st.number_input(
        "Asset / Property Value (₹)",
        min_value=0.0,
        value=(
            st.session_state["form_data"]["asset"]
            if st.session_state["form_data"]["asset"] != 0.0
            else None
        ),
        step=10000.0,
        placeholder="Enter your Asset / Property Value",
        key="asset_input"
    )

    # ✅ OPTIONAL (nice touch)
    if asset_value:
        st.caption(f"🏠 {format_inr(asset_value)}")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# LOAN CALCULATION
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.subheader("📊 Loan Calculation")

tenure_years = st.slider(
    "Loan Tenure (Years)",
    1,
    30,
    st.session_state["form_data"].get("years", 5),
    key="years_input"
)

st.markdown(
    "<p style='margin-top:-10px; font-size:13px; color:gray;'>(Slide to adjust your loan repayment period)</p>",
    unsafe_allow_html=True
)

interest_default = st.session_state["form_data"].get("interest")

interest_rate = st.number_input(
    "Interest Rate (%)",
    min_value=0.0,
    value=interest_default if interest_default is not None else None,
    step=0.01,
    placeholder="Enter The Interest Rate",
    key="interest_input"
)

# Save values
st.session_state["form_data"]["years"] = tenure_years

if interest_rate is not None:
    st.session_state["form_data"]["interest"] = interest_rate
emi = None
dti = None
monthly_income = None
ltv = None

if loan_amount and interest_rate and loan_amount > 0 and interest_rate > 0:

    interest_rate = interest_rate / 100
    monthly_rate = interest_rate / 12
    months = tenure_years * 12

    emi = (loan_amount * monthly_rate * (1 + monthly_rate) ** months) / (
        (1 + monthly_rate) ** months - 1
    )

    if annual_income and annual_income > 0:
        monthly_income = annual_income / 12
        dti = emi / monthly_income
        st.info(f"📊 EMI: {format_inr(emi)} | DTI: {dti:.2f}")
    else:

        st.info(f"📊 EMI: {format_inr(emi)} | Student Case (No Income)")

    # 🔥 LTV CALCULATION
    if asset_value and asset_value > 0:
        ltv = loan_amount / asset_value
        st.info(f"🏠 LTV Ratio: {ltv:.2f}")

else:
    st.warning("Enter loan & interest to calculate EMI")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# PREDICTION
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

if st.button("🏦 Generate Decision"):
    st.session_state["predicted"] = True
if st.session_state.get("predicted"):

    if st.session_state.get("predicted"):

        errors = []

        if age is None or age <= 0:
            errors.append("Enter valid age")

        if annual_income is None or annual_income <= 0:
            errors.append("Enter valid annual income")

        if loan_amount is None or loan_amount <= 0:
            errors.append("Enter valid loan amount")

        if credit_score is None:
            errors.append("Enter credit score")

        if interest_rate is None:
            errors.append("Enter interest rate")

        if errors:
            error_box.error("⚠ " + " | ".join(errors))
            st.stop()

    st.session_state["form_data"] = {
        "age": age,
        "income": annual_income,
        "loan": loan_amount,
        "asset": asset_value,
        "credit": credit_score
    }
    model_income = annual_income if annual_income and annual_income > 0 else 1

    data = pd.DataFrame(
        [[model_income, loan_amount, credit_score]],
        columns=["annual_income", "loan_amount", "credit_score"]
    )

    pred = model.predict(data)[0]
    prob = model.predict_proba(data)[0][1]

    final_decision = pred

    # ---------------------------
    # BANK LOGIC
    # ---------------------------
    if loan_type == "Education":
        if credit_score < 500:
            final_decision = 0
    else:
        if credit_score < 550:
            final_decision = 0
        elif dti is not None and dti > 0.75:
            final_decision = 0
        elif employment == "Unemployed" and dti is not None and dti > 0.60:
            final_decision = 0
        elif credit_score < 650 and dti is not None and dti > 0.60:
            final_decision = 0

    # 🔥 COLLATERAL OVERRIDE
    if ltv is not None:
        if ltv <= 0.70 and credit_score >= 600:
            final_decision = 1
            st.success("🏦 Approved based on strong collateral (Low LTV)")

    # 🔥 AI vs POLICY
    if pred == 1 and final_decision == 0:
        st.warning("⚠ AI suggested approval, but bank policy rejected this application")

    # SAVE STATE
    st.session_state["loan_result"] = {
        "income": annual_income,
        "loan": loan_amount,
        "credit_score": credit_score,
        "dti": dti if dti else 0,
        "emi": emi if emi else 0,
        "decision": final_decision,
        "prob": prob,
        "loan_type": loan_type,
        "ltv": ltv if ltv else 0
    }

    # ---------------------------
    # RESULT
    # ---------------------------
    st.markdown("## 📊 Decision Result")

    if final_decision == 1:
        st.success("✅ Loan Approved")
    else:
        st.warning("❌ Loan Not Approved")
        st.info("Decision based on financial risk and bank policy")

    st.metric("Confidence", f"{prob * 100:.2f}%")

    # ---------------------------
    # 🔮 WHAT-IF SIMULATION
    # ---------------------------
    if final_decision == 0 and dti is not None:

        st.markdown("## 🔮 Improve Your Approval Chances")

        colA, colB = st.columns(2)

        with colA:
            new_income = st.slider(
                "Increase Income (₹)",
                int(annual_income or 0),
                int((annual_income or 100000) * 2),
                int(annual_income or 0)
            )

        with colB:
            new_loan = st.slider(
                "Reduce Loan Amount (₹)",
                10000,
                int(loan_amount),
                int(loan_amount)
            )

        # Recalculate
        if new_income > 0:
            new_monthly_income = new_income / 12
            new_emi = (new_loan * monthly_rate * (1 + monthly_rate) ** months) / (
                    (1 + monthly_rate) ** months - 1
            )
            # same EMI assumption
            new_dti = new_emi / new_monthly_income

            st.info(f"New DTI: {new_dti:.2f}")

            if new_dti < 0.5:
                st.success("✅ This scenario is likely to be approved")
            else:
                st.warning("⚠ Still risky — reduce loan more or increase income")

    # ---------------------------
    # RISK
    # ---------------------------
    st.markdown("## ⚠️ Risk Analysis")

    if dti is not None:
        risk_color = get_dti_color(dti)

        if risk_color == "green":
            st.success("🟢 Low Risk (Healthy Debt Level)")
        elif risk_color == "orange":
            st.warning("🟠 Moderate Risk (Monitor Debt)")
        else:
            st.error("🔴 High Risk (Debt Too High)")

    # ---------------------------
    # CREDIT
    # ---------------------------
    if credit_score > 750:
        st.success("💳 Excellent Credit")
    elif credit_score > 650:
        st.info("💳 Good Credit")
    else:
        st.warning("💳 Weak Credit")

    # ---------------------------
    # EDUCATION LOAN
    # ---------------------------
    if loan_type == "Education":
        st.markdown("## 🎓 Education Loan Insights")
        if annual_income == 0:
            st.info("📘 No income? Normal for students")
        if credit_score < 600:
            st.warning("Add co-applicant to improve approval")
        if loan_amount > 2000000:
            st.warning("High loan → collateral may be required")
        st.success("Banks evaluate future earning potential")

    # ---------------------------
    # RECOMMENDATIONS
    # ---------------------------
    st.markdown("## 🤖 Recommendations")

    if credit_score < 650:
        st.warning("Improve credit score")

    if dti is not None and dti > 0.5:
        st.warning("Reduce loan or increase income")

    if employment == "Unemployed" and loan_type != "Education":
        st.warning("Stable job helps approval")

    if annual_income and loan_amount > annual_income * 0.8:
        st.warning("Loan too high vs income")

    if dti is not None and dti < 0.3 and credit_score > 700:
        st.success("Excellent profile")

    # ---------------------------
    # ELIGIBILITY
    # ---------------------------
    if monthly_income:
        max_emi = monthly_income * 0.5
        estimated_loan = (max_emi * ((1 + monthly_rate) ** months - 1)) / (
            monthly_rate * (1 + monthly_rate) ** months
        )
        st.session_state["form_data"]["safe_loan"] = estimated_loan
        st.success(f"💰 Recommended Safe Loan Limit: ₹{format_inr(estimated_loan)}")

    st.markdown("---")
    st.page_link("pages/2_Analytics.py", label="➡ View Analytics")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.caption("© 2026 | AI Loan Decision & Credit Risk Platform | Developed by Subhadip")
