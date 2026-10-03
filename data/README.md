# Data

## Option A: Demo (automatic)
With no real file present, `python src/prepare_data.py` generates a **synthetic** 30,000-row file in the raw UCI format.
Use it to learn the workflow only; its numbers are not real.

## Option B: Real data (recommended)
Dataset: **Bank Marketing** (UCI Machine Learning Repository, also on Kaggle). Direct marketing phone-call campaigns of a
Portuguese bank selling term deposits. Search "Bank Marketing" on Kaggle or UCI.

Either file works:
- `bank-additional-full.csv` (41,188 rows, includes economic indicators, no balance column)
- `bank-full.csv` (45,211 rows, includes the `balance` column)

1. Download the CSV.
2. Save it in this folder (`data/`) with its original name (or as `bank_marketing.csv`).
3. Run `python src/prepare_data.py`. It detects the separator (`;` or `,`) and handles both layouts.

## Output (what Power BI loads)
`data/powerbi/campaign_clean.csv`, `dim_month.csv`, `dim_job.csv`, `dim_education.csv`
