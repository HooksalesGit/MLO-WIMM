"""Pydantic models used in the calculators."""

from __future__ import annotations

from pydantic import BaseModel


class Housing(BaseModel):
    purchase_price: float
    down_payment_amt: float
    rate_pct: float
    term_years: int
    tax_rate_pct: float
    hoi_annual: float
    hoa_monthly: float
    finance_upfront: bool = True
    first_use: bool = True  # used for VA funding fee
