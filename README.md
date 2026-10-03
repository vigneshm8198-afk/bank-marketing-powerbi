# Bank Marketing Campaign Performance Dashboard (Power BI)

A 3-page Power BI report that shows **which customers say yes to a term-deposit offer, when, and how much calling effort it takes**,
built on the UCI Bank Marketing dataset (phone campaigns of a Portuguese bank).

<!-- Replace with your screenshot after building the report -->
![Campaign overview](screenshots/page1_overview.png)

## Business questions
1. What is the campaign's conversion rate, and how much effort (contacts, call time, cost) does each subscription take?
2. Which months, channels and customer segments convert best?
3. Do repeated calls still pay off, or does conversion fall while cost rises?
4. Does a successful earlier campaign predict a new subscription?

## Report pages
| Page | What it shows |
|------|---------------|
| 1. Campaign Overview | 6 KPIs, volume and conversion by month, channel, number of contacts, outcome mix |
| 2. Customer Segments | Conversion by age, job, education, marital status, age x job heat matrix, decomposition tree |
| 3. Campaign Efficiency and Targeting | Cost per subscription by contacts, previous-outcome lift, call-duration bands, job bubbles, top segments by lift, cost What-if slider |

![Customer segments](screenshots/page2_segments.png)
![Efficiency](screenshots/page3_efficiency.png)

## Tech
Power BI (Power Query M, DAX, star-schema modelling, What-if parameter, decomposition tree, conditional formatting), Python (pandas) for data preparation.

## How to use this repo
```bash
git clone https://github.com/<your-username>/bank-marketing-powerbi.git
cd bank-marketing-powerbi
pip install -r requirements.txt
python src/prepare_data.py        # creates data/powerbi/*.csv
```
Then follow **[powerbi/BUILD_GUIDE.md](powerbi/BUILD_GUIDE.md)** in Power BI Desktop (about 1 hour).

| File | Purpose |
|------|---------|
| `powerbi/powerquery/*.m` | Power Query code for the fact table and 3 dimensions |
| `powerbi/dax/measures.dax` | 19 documented measures (conversion, lift, cost, call quality, ranking) |
| `powerbi/dax/whatif_cost_parameter.dax` | Adjustable cost-per-contact assumption |
| `powerbi/data_model.md` | Star schema diagram and definitions |
| `powerbi/report_layout.md` | Visual-by-visual spec for all 3 pages |
| `powerbi/theme/marketing_theme.json` | Colour theme |
| `src/validate_kpis.py` | Computes expected KPIs in pandas so you can check your DAX |

With no real data present, `prepare_data.py` uses a **synthetic demo** so you can try the workflow. For real results,
download the dataset first (see [data/README.md](data/README.md)). Both `bank-additional-full.csv` and `bank-full.csv` work.

## Key definitions
- **Subscription:** the customer said yes to the term deposit. **Conversion rate** = subscriptions / customers contacted.
- **Lift:** a segment's conversion rate divided by the overall rate (1.5 = 50% better than average).
- **Contacts:** calls made to a customer in this campaign. **Cost per subscription** = contacts x assumed cost per contact / subscriptions.

## Key findings (fill in from your finished report)
| Question | Your finding |
|----------|--------------|
| Overall conversion rate and cost per subscription | _fill in_ |
| Best and worst months and channel | _fill in_ |
| Highest-lift customer segments | _fill in_ |
| Effect of number of contacts | _fill in_ |
| Previous campaign success vs new subscription | _fill in_ |

## Recommendations (adapt to your findings)
- Prioritise segments with high lift and enough volume, instead of calling everyone equally.
- Set a contact cap where extra calls stop paying back (see cost per subscription by number of contacts).
- Re-contact customers with a previous successful outcome first.
- Use call duration to judge call quality and training, not to pick who to call (see limits).

## Assumptions and limits
- **Call duration is only known after the call**, and long calls strongly go with a "yes". It explains outcomes but cannot be used to choose whom to call, so do not use it as a targeting rule.
- **Cost per contact is an illustrative assumption** (adjustable slider), not a figure from the data.
- The data has month but no year, and covers several years, so "month" mixes years. Seasonality may also reflect how the bank scheduled campaigns.
- Months with few customers (for example March, September, October, December) have small samples, so their high rates are less reliable. Check the customer count before drawing conclusions.
- Association, not causation: a segment that converts well may do so because of other factors.

## Project structure
```
bank-marketing-powerbi/
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
├── data/README.md                 # where to get the real data
├── src/
│   ├── prepare_data.py            # raw UCI file -> 4 clean CSVs
│   ├── make_sample_data.py        # synthetic demo data
│   └── validate_kpis.py           # expected KPI values for checking DAX
├── powerbi/
│   ├── BUILD_GUIDE.md
│   ├── data_model.md
│   ├── report_layout.md
│   ├── powerquery/   dax/   theme/
│   └── Bank_Marketing_Dashboard.pbix   # add after you build it
└── screenshots/
```

## Author
Vignesh M | Data Analytics | Chennai
