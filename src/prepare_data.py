"""Turn the raw UCI Bank Marketing CSV into the 4 clean files Power BI loads:
data/powerbi/campaign_clean.csv, dim_month.csv, dim_job.csv, dim_education.csv

Works with bank-additional-full.csv (semicolon) and bank-full.csv / bank.csv (semicolon or comma).

Usage:
    python src/prepare_data.py                  # uses a real file in data/ if present, else a synthetic demo
    python src/prepare_data.py --input my.csv
"""
import argparse
import sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "powerbi"
RAW_NAMES = ["bank-additional-full.csv", "bank-full.csv", "bank.csv", "bank_marketing.csv"]
CORE = ["age", "job", "marital", "education", "default", "housing", "loan", "contact", "month",
        "duration", "campaign", "pdays", "previous", "poutcome", "y"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

JOB_GROUP = {"Admin": "Professional & office", "Management": "Professional & office", "Technician": "Professional & office",
             "Blue-Collar": "Service & manual", "Services": "Service & manual", "Housemaid": "Service & manual",
             "Entrepreneur": "Self-employed", "Self-Employed": "Self-employed",
             "Retired": "Not working", "Student": "Not working", "Unemployed": "Not working", "Unknown": "Unknown"}
EDU_MAP = {"basic.4y": ("Basic (4 yrs)", "1. Primary or less"), "basic.6y": ("Basic (6 yrs)", "1. Primary or less"),
           "basic.9y": ("Basic (9 yrs)", "1. Primary or less"), "illiterate": ("Illiterate", "1. Primary or less"),
           "primary": ("Primary", "1. Primary or less"), "high.school": ("High school", "2. Secondary"),
           "secondary": ("Secondary", "2. Secondary"), "professional.course": ("Professional course", "3. Tertiary or professional"),
           "university.degree": ("University degree", "3. Tertiary or professional"),
           "tertiary": ("Tertiary", "3. Tertiary or professional"), "unknown": ("Unknown", "4. Unknown")}


def read_any(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        head = f.readline()
    sep = ";" if head.count(";") > head.count(",") else ","
    df = pd.read_csv(path, sep=sep)
    df.columns = [c.strip().strip('"').lower() for c in df.columns]
    return df


def yes_no(s):
    return s.astype(str).str.lower().map({"yes": "Yes", "no": "No"}).fillna("Unknown")


def clean(raw):
    missing = [c for c in CORE if c not in raw.columns]
    if missing:
        sys.exit(f"ERROR: input is missing columns: {missing}")
    d = pd.DataFrame(index=raw.index)
    d["customer_id"] = np.arange(1, len(raw) + 1)
    d["age"] = pd.to_numeric(raw["age"], errors="coerce")
    d["job"] = raw["job"].astype(str).str.replace(".", "", regex=False).str.title()
    d["marital"] = raw["marital"].astype(str).str.title()
    d["education"] = raw["education"].astype(str).str.lower().map(lambda x: EDU_MAP.get(x, (x.title(), "4. Unknown"))[0])
    d["credit_default"] = yes_no(raw["default"])
    d["housing_loan"] = yes_no(raw["housing"])
    d["personal_loan"] = yes_no(raw["loan"])
    d["contact"] = raw["contact"].astype(str).str.title().replace({"Unknown": "Unknown"})
    d["month"] = raw["month"].astype(str).str.title().str[:3]
    d["month_num"] = d["month"].map({m: i + 1 for i, m in enumerate(MONTHS)})
    d["day_of_week"] = raw["day_of_week"].astype(str).str.title() if "day_of_week" in raw.columns else np.nan
    d["balance"] = pd.to_numeric(raw["balance"], errors="coerce") if "balance" in raw.columns else np.nan
    d["duration_sec"] = pd.to_numeric(raw["duration"], errors="coerce")
    d["campaign"] = pd.to_numeric(raw["campaign"], errors="coerce")
    d["pdays"] = pd.to_numeric(raw["pdays"], errors="coerce")
    d["previous"] = pd.to_numeric(raw["previous"], errors="coerce")
    d["previously_contacted"] = np.where(d["pdays"].isin([999, -1]) | d["pdays"].isna(), "No", "Yes")
    po = raw["poutcome"].astype(str).str.lower().map(
        {"success": "Success", "failure": "Failure", "other": "Other", "nonexistent": "No previous campaign",
         "unknown": "No previous campaign"}).fillna("No previous campaign")
    d["poutcome"] = po
    ylab = raw["y"].astype(str).str.lower()
    d["subscribed"] = (ylab == "yes").astype(int)
    d["outcome_label"] = np.where(d["subscribed"] == 1, "Subscribed", "Not subscribed")
    d = d[d["age"].notna() & d["month_num"].notna() & ylab.isin(["yes", "no"])]
    return d


def write_dims(d):
    pd.DataFrame({"month": MONTHS, "month_num": range(1, 13),
                  "quarter": ["Q1"] * 3 + ["Q2"] * 3 + ["Q3"] * 3 + ["Q4"] * 3}).to_csv(OUT / "dim_month.csv", index=False)
    jobs = sorted(d["job"].unique())
    pd.DataFrame({"job": jobs, "job_group": [JOB_GROUP.get(j, "Unknown") for j in jobs]}).to_csv(OUT / "dim_job.csv", index=False)
    edus = sorted(d["education"].unique())
    lookup = {v[0]: v[1] for v in EDU_MAP.values()}
    pd.DataFrame({"education": edus, "education_group": [lookup.get(e, "4. Unknown") for e in edus]}
                 ).to_csv(OUT / "dim_education.csv", index=False)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    src = Path(a.input) if a.input else next((ROOT / "data" / n for n in RAW_NAMES if (ROOT / "data" / n).exists()), None)
    if src is None:
        print("NOTE: real Bank Marketing file not found in data/. Using the SYNTHETIC demo data.")
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from make_sample_data import make
        raw, label = make(), "SYNTHETIC DEMO"
    else:
        raw, label = read_any(src), f"REAL: {src.name}"
    d = clean(raw)
    d.to_csv(OUT / "campaign_clean.csv", index=False)
    write_dims(d)
    print(f"[{label}] wrote {len(d):,} customers to data/powerbi/campaign_clean.csv "
          f"(conversion {d.subscribed.mean():.1%}); balance column {'present' if d.balance.notna().any() else 'not in this file'}")
    print("Also wrote dim_month.csv, dim_job.csv, dim_education.csv. Next: powerbi/BUILD_GUIDE.md")
