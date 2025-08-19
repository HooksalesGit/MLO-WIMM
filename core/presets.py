"""Program default parameters.

Values are expressed as decimals, e.g. 0.009 for 0.90%."""

# Conventional MI table: list of (LTV threshold, annual MI rate)
CONVENTIONAL_MI = [
    (97, 0.0090),  # >=97%
    (95, 0.0062),  # 95-97%
    (90, 0.0040),  # 90-95%
    (85, 0.0025),  # 85-90%
    (0, 0.0),  # <85%
]

# FHA parameters
FHA_UFMIP = 0.0175
FHA_MIP = {
    (True, True): 0.0045,  # LTV<=95, term<=15
    (True, False): 0.0070,  # LTV<=95, term>15
    (False, True): 0.0050,  # LTV>95, term<=15
    (False, False): 0.0080,  # LTV>95, term>15
}

# VA funding fee rates (first_use -> rate)
VA_FUNDING_FEE = {True: 0.023, False: 0.036}

# USDA fees
USDA_GUARANTEE_FEE = 0.01
USDA_ANNUAL_FEE = 0.0035
