"""Generate a SYNTHETIC file in the RAW UCI 'bank-additional-full' format (semicolon separated).
Used only so the project runs out of the box. Replace with the real file for real insights."""
import numpy as np
import pandas as pd

JOBS = ["admin.", "blue-collar", "technician", "services", "management", "retired", "entrepreneur",
        "self-employed", "housemaid", "unemployed", "student", "unknown"]
JOB_P = [0.25, 0.22, 0.16, 0.10, 0.07, 0.04, 0.035, 0.035, 0.026, 0.025, 0.02, 0.01]
EDU = ["university.degree", "high.school", "basic.9y", "professional.course", "basic.4y", "basic.6y", "unknown", "illiterate"]
EDU_P = [0.30, 0.23, 0.15, 0.13, 0.10, 0.055, 0.035, 0.0005]
MONTHS = ["may", "jul", "aug", "jun", "nov", "apr", "oct", "sep", "mar", "dec"]
MONTH_P = [0.334, 0.174, 0.150, 0.129, 0.100, 0.064, 0.017, 0.014, 0.013, 0.005]
MONTH_FX = dict(may=-0.5, jul=0.0, aug=0.0, jun=-0.1, nov=-0.2, apr=0.6, oct=2.2, sep=2.0, mar=2.2, dec=2.3)
JOB_FX = {"student": 0.8, "retired": 0.6, "blue-collar": -0.4, "services": -0.2, "unemployed": 0.2}


def norm(p):
    p = np.array(p, float)
    return p / p.sum()


def make(n=30_000, seed=21):
    rng = np.random.default_rng(seed)
    age = np.clip(rng.normal(40, 10.5, n).round(), 17, 95).astype(int)
    job = rng.choice(JOBS, n, p=norm(JOB_P))
    month = rng.choice(MONTHS, n, p=norm(MONTH_P))
    contact = rng.choice(["cellular", "telephone"], n, p=[0.63, 0.37])
    prev_contacted = rng.random(n) < 0.04
    pdays = np.where(prev_contacted, rng.integers(1, 28, n), 999)
    previous = np.where(prev_contacted, rng.integers(1, 4, n), 0)
    poutcome = np.where(~prev_contacted, "nonexistent", np.where(rng.random(n) < 0.35, "success", "failure"))
    campaign = np.minimum(rng.geometric(0.4, n), 30)
    housing = rng.choice(["yes", "no", "unknown"], n, p=[0.52, 0.45, 0.03])
    loan = rng.choice(["yes", "no", "unknown"], n, p=[0.15, 0.82, 0.03])
    default = rng.choice(["no", "unknown", "yes"], n, p=[0.79, 0.209, 0.001])

    z = (-2.6 + np.array([MONTH_FX[m] for m in month]) + np.array([JOB_FX.get(j, 0) for j in job])
         + 2.8 * (poutcome == "success") + 0.1 * (poutcome == "failure") + 0.5 * (contact == "cellular")
         + 0.8 * (age < 25) + 1.3 * (age >= 60) - 0.12 * (np.minimum(campaign, 10) - 1)
         - 0.15 * (housing == "yes") - 2.0 * (default == "yes"))
    y = rng.random(n) < 1 / (1 + np.exp(-z))
    duration = np.where(y, rng.gamma(2.0, 280, n), rng.gamma(2.0, 110, n)).clip(0, 3000).round().astype(int)
    df = pd.DataFrame({
        "age": age, "job": job, "marital": rng.choice(["married", "single", "divorced", "unknown"], n, p=[0.61, 0.28, 0.105, 0.005]),
        "education": rng.choice(EDU, n, p=norm(EDU_P)), "default": default, "housing": housing, "loan": loan,
        "contact": contact, "month": month, "day_of_week": rng.choice(["mon", "tue", "wed", "thu", "fri"], n),
        "duration": duration, "campaign": campaign, "pdays": pdays, "previous": previous, "poutcome": poutcome,
        "emp.var.rate": rng.choice([1.4, -1.8, 1.1, -0.1, -2.9, -3.4], n), "cons.price.idx": 93.5,
        "cons.conf.idx": -40.0, "euribor3m": rng.uniform(0.6, 5.0, n).round(3), "nr.employed": 5100.0,
        "y": np.where(y, "yes", "no")})
    return df


if __name__ == "__main__":
    d = make()
    d.to_csv("data/sample_raw_bank.csv", index=False, sep=";")
    print(f"Wrote {len(d):,} synthetic raw rows to data/sample_raw_bank.csv (conversion {(d.y == 'yes').mean():.1%})")
