"""Mortgage payment and qualification calculators."""

from __future__ import annotations

from typing import Dict, Tuple

from .models import Housing
from . import presets


def amortization(principal: float, rate_pct: float, term_years: int) -> float:
    """Return monthly principal and interest payment."""
    n = term_years * 12
    if n <= 0:
        raise ValueError("term_years must be positive")
    r = rate_pct / 100 / 12
    if r == 0:
        return principal / n
    return principal * r * (1 + r) ** n / ((1 + r) ** n - 1)


def inverse_amortization(payment: float, rate_pct: float, term_years: int) -> float:
    """Return loan amount that yields the given payment."""
    n = term_years * 12
    if n <= 0:
        raise ValueError("term_years must be positive")
    r = rate_pct / 100 / 12
    if r == 0:
        return payment * n
    return payment * ((1 + r) ** n - 1) / (r * (1 + r) ** n)


def _lookup_conventional_mi(ltv: float) -> float:
    for threshold, rate in presets.CONVENTIONAL_MI:
        if ltv >= threshold:
            return rate
    return 0.0


def housing_payment(housing: Housing, program: str) -> Dict[str, float]:
    """Compute housing payment components for a program."""
    base_loan = max(0.0, housing.purchase_price - housing.down_payment_amt)
    ltv = 0.0
    if housing.purchase_price:
        ltv = 100 * base_loan / housing.purchase_price

    upfront_fee = 0.0
    mi_monthly = 0.0
    adjusted_loan = base_loan

    if program == "Conventional":
        mi_rate = _lookup_conventional_mi(ltv)
        mi_monthly = base_loan * mi_rate / 12
    elif program == "FHA":
        ufmip = base_loan * presets.FHA_UFMIP
        upfront_fee = ufmip
        if housing.finance_upfront:
            adjusted_loan += ufmip
        key = (ltv <= 95, housing.term_years <= 15)
        annual_mip = presets.FHA_MIP[key]
        mi_monthly = adjusted_loan * annual_mip / 12
    elif program == "VA":
        rate = presets.VA_FUNDING_FEE[housing.first_use]
        fee = base_loan * rate
        upfront_fee = fee
        if housing.finance_upfront:
            adjusted_loan += fee
    elif program == "USDA":
        fee = base_loan * presets.USDA_GUARANTEE_FEE
        upfront_fee = fee
        if housing.finance_upfront:
            adjusted_loan += fee
        mi_monthly = adjusted_loan * presets.USDA_ANNUAL_FEE / 12
    else:  # Jumbo or other
        pass

    p_i = amortization(adjusted_loan, housing.rate_pct, housing.term_years)
    taxes = housing.purchase_price * (housing.tax_rate_pct / 100) / 12
    hoi = housing.hoi_annual / 12
    hoa = housing.hoa_monthly
    housing_total = p_i + taxes + hoi + hoa + mi_monthly
    return {
        "base_loan": base_loan,
        "adjusted_loan": adjusted_loan,
        "ltv": ltv,
        "p_i": p_i,
        "taxes": taxes,
        "hoi": hoi,
        "hoa": hoa,
        "mi": mi_monthly,
        "housing_total": housing_total,
        "upfront_fee": upfront_fee,
    }


def compute_dti(
    total_income: float, housing_total: float, other_debts: float
) -> Tuple[float, float]:
    """Return front-end and back-end DTI ratios."""
    if total_income <= 0:
        return float("inf"), float("inf")
    fe = housing_total / total_income
    be = (housing_total + other_debts) / total_income
    return fe, be
