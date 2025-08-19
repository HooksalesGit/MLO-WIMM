import pathlib
import sys

import pytest

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from core.models import Housing
from core import calculators


def test_amortization_inverse():
    loan = 200000
    rate = 6.0
    term = 30
    payment = calculators.amortization(loan, rate, term)
    assert payment == pytest.approx(1199.10, rel=1e-4)
    assert calculators.inverse_amortization(payment, rate, term) == pytest.approx(
        loan, rel=1e-4
    )


def make_housing(pp, dp, rate=6.0, term=30, tax=1.25, hoi=1800, hoa=0):
    return Housing(
        purchase_price=pp,
        down_payment_amt=dp,
        rate_pct=rate,
        term_years=term,
        tax_rate_pct=tax,
        hoi_annual=hoi,
        hoa_monthly=hoa,
    )


def test_conventional_mi():
    h = make_housing(300000, 45000)
    result = calculators.housing_payment(h, "Conventional")
    assert result["mi"] == pytest.approx(53.125, rel=1e-4)
    assert result["p_i"] == pytest.approx(1528.85, rel=1e-4)
    assert result["housing_total"] == pytest.approx(2044.48, rel=1e-4)


def test_fha_financed():
    h = make_housing(300000, 30000)
    result = calculators.housing_payment(h, "FHA")
    assert result["upfront_fee"] == pytest.approx(4725.0, rel=1e-4)
    assert result["mi"] == pytest.approx(160.25625, rel=1e-4)
    assert result["housing_total"] == pytest.approx(2269.87, rel=1e-4)


def test_va_first_use():
    h = make_housing(300000, 0)
    result = calculators.housing_payment(h, "VA")
    assert result["upfront_fee"] == pytest.approx(6900.0, rel=1e-4)
    assert result["mi"] == 0
    assert result["housing_total"] == pytest.approx(2302.52, rel=1e-4)


def test_usda():
    h = make_housing(250000, 0)
    result = calculators.housing_payment(h, "USDA")
    assert result["upfront_fee"] == pytest.approx(2500.0, rel=1e-4)
    assert result["mi"] == pytest.approx(73.6458, rel=1e-4)
    assert result["housing_total"] == pytest.approx(1997.93, rel=1e-4)
