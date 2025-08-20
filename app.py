"""Streamlit UI for mortgage payment and DTI calculators."""

import streamlit as st

from core.calculators import compute_dti, housing_payment
from core.models import Housing


st.title("Mortgage Income & DTI Dashboard")

program = st.sidebar.selectbox(
    "Program", ["Conventional", "FHA", "VA", "USDA", "Jumbo"], index=0
)

with st.form("housing_form"):
    purchase_price = st.number_input(
        "Purchase price", min_value=0.0, value=300_000.0, step=1_000.0
    )
    down_payment_amt = st.number_input(
        "Down payment", min_value=0.0, value=60_000.0, step=1_000.0
    )
    rate_pct = st.number_input("Rate %", min_value=0.0, value=6.5, step=0.125)
    term_years = st.number_input("Term (years)", min_value=1, value=30)
    tax_rate_pct = st.number_input("Tax rate %", min_value=0.0, value=1.25, step=0.01)
    hoi_annual = st.number_input("Annual HOI", min_value=0.0, value=1_800.0, step=100.0)
    hoa_monthly = st.number_input("Monthly HOA", min_value=0.0, value=0.0, step=10.0)
    finance_upfront = st.checkbox("Finance upfront fee", value=True)
    first_use = st.checkbox("First use (VA only)", value=True)
    total_income = st.number_input(
        "Total monthly income", min_value=0.0, value=8_000.0, step=100.0
    )
    other_debts = st.number_input(
        "Other monthly debts", min_value=0.0, value=0.0, step=50.0
    )
    submitted = st.form_submit_button("Calculate")

if submitted:
    housing = Housing(
        purchase_price=purchase_price,
        down_payment_amt=down_payment_amt,
        rate_pct=rate_pct,
        term_years=term_years,
        tax_rate_pct=tax_rate_pct,
        hoi_annual=hoi_annual,
        hoa_monthly=hoa_monthly,
        finance_upfront=finance_upfront,
        first_use=first_use,
    )
    payments = housing_payment(housing, program)
    st.subheader("Housing Payment")
    st.write(
        {
            "P&I": payments["p_i"],
            "Taxes": payments["taxes"],
            "HOI": payments["hoi"],
            "HOA": payments["hoa"],
            "MI": payments["mi"],
            "Total": payments["housing_total"],
        }
    )
    fe, be = compute_dti(
        total_income=total_income,
        housing_total=payments["housing_total"],
        other_debts=other_debts,
    )
    st.subheader("DTI Ratios")
    st.write({"Front-end": fe, "Back-end": be})
