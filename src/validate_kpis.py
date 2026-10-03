"""Compute the headline KPIs with pandas so you can check your Power BI DAX measures
(no slicers selected, Cost per Contact = 5)."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
d = pd.read_csv(ROOT / "data" / "powerbi" / "campaign_clean.csv")
COST = 5.0
subs, n, contacts = d.subscribed.sum(), len(d), d.campaign.sum()
k = {
    "Customers Contacted": n,
    "Subscriptions": subs,
    "Conversion Rate": subs / n,
    "Total Contacts": contacts,
    "Avg Contacts per Customer": contacts / n,
    "Contacts per Subscription": contacts / subs,
    "Avg Call Duration (min)": d.duration_sec.mean() / 60,
    "Avg Duration Subscribed (min)": d[d.subscribed == 1].duration_sec.mean() / 60,
    "Avg Duration Not Subscribed (min)": d[d.subscribed == 0].duration_sec.mean() / 60,
    "Total Campaign Cost": contacts * COST,
    "Cost per Subscription": contacts * COST / subs,
}
print(pd.DataFrame({"measure": k.keys(), "expected_value": [round(float(v), 4) for v in k.values()]}).to_string(index=False))
for col in ["month", "contact", "poutcome"]:
    print(f"\nConversion rate by {col}:")
    print((d.groupby(col).subscribed.mean() * 100).round(1).sort_values(ascending=False).to_string())
