# AGENTS.md
## Project
Mortgage Income & DTI Dashboard (Streamlit, Python)

## Commands
- Install: `pip install -r requirements.txt`
- Run: `streamlit run app.py`
- Test: `pytest -q`

## Style
- Python 3.11+, black/ruff
- Keep business rules in core/calculators.py; add unit tests for FHA/VA/USDA/Conv cases.
- Do not hardcode program overlays; read from core/presets.py.

## Tasks guidance
- When adding features, update tests in tests/*.py and README with usage notes.
- Surface warnings via core/rules.py and ensure PDF export includes new fields.
