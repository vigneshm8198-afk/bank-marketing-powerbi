# Build Guide: Bank Marketing Campaign Performance (Power BI Desktop)

Time needed: about 1 hour. Power BI Desktop (free, Windows) is required.

## Step 0: Prepare the data (once)
```bash
pip install -r requirements.txt
python src/prepare_data.py
```
Creates four files in `data/powerbi/`: `campaign_clean.csv`, `dim_month.csv`, `dim_job.csv`, `dim_education.csv`.
(For real data, first follow `data/README.md`.)

## Step 1: Load the data
1. Open Power BI Desktop > **Home > Transform data**.
2. **Manage Parameters > New Parameter**: Name `DataFolder`, Type `Text`, value = full path of `data\powerbi\` **ending with a slash**
   (see `powerquery/00_parameter_DataFolder.m`).
3. For each file in `powerquery/` (`fact_campaign.m`, `dim_month.m`, `dim_job.m`, `dim_education.m`):
   **New Source > Blank Query > Advanced Editor**, delete the default text, paste the file, Done,
   then rename the query exactly `fact_campaign`, `dim_month`, `dim_job`, `dim_education`.
4. **Close & Apply**.

## Step 2: Build the model (Model view)
Create these relationships (many-to-one, single direction, dimension to fact). Diagram in `data_model.md`.

| From (fact_campaign) | To (dimension) |
|---|---|
| `month` | `dim_month[month]` |
| `job` | `dim_job[job]` |
| `education` | `dim_education[education]` |

Then:
- `dim_month[month]`: **Sort by column > month_num** (so Jan to Dec, not alphabetical).
- Hide the original `month`, `job` and `education` columns in `fact_campaign` and use the ones from the dimensions in visuals
  (`job_group` and `education_group` live only in the dimensions).

## Step 3: Add the What-if parameter
**Modeling > New parameter > Numeric range**: name `Cost per Contact`, Decimal, min 1, max 20, increment 0.5, default 5,
keep "Add slicer to this page" ticked. Details in `dax/whatif_cost_parameter.dax`.
This cost is an **illustrative assumption**, not a figure from the dataset.

## Step 4: Add the measures
1. **Home > Enter data**, create an empty table named `_Measures`, Load.
2. Select `_Measures`, then **Modeling > New measure** for each measure in `dax/measures.dax`.
3. Apply the number formats written next to each measure.

## Step 5: Check your numbers
With no slicers selected and Cost per Contact = 5, compare your cards with:
```bash
python src/validate_kpis.py
```
Customers Contacted, Subscriptions, Conversion Rate, Total Contacts, Avg Call Duration and Cost per Subscription must match.
Fix the DAX before building visuals if they do not.

## Step 6: Theme and pages
1. **View > Themes > Browse for themes** > `theme/marketing_theme.json`.
2. Build 3 pages as described in `report_layout.md`.

## Step 7: Polish
- Plain business titles on every visual.
- **Sync slicers** for Month and Contact channel across pages.
- Page 3: set the "Top segments" table visual filter `Customers Contacted >= 100`.
- Use **View > Page view > Fit to page**, and align visuals with the Format > Align tools.

## Step 8: Save and publish to GitHub
1. Save as `powerbi/Bank_Marketing_Dashboard.pbix`.
2. Take 3 screenshots into `screenshots/`: `page1_overview.png`, `page2_segments.png`, `page3_efficiency.png`.
3. Commit the `.pbix` and screenshots; update the README links and the Key findings table.
