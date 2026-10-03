# Report layout (3 pages, 16:9 canvas)

Slicers on every page (sync them): **Month** (`dim_month[month]`) and **Contact channel** (`fact_campaign[contact]`).
Page 3 also has the **Cost per Contact** What-if slicer.

## Page 1: Campaign Overview
```
+------------------------------------------------------------------+
| Term Deposit Campaign Overview            [Month] [Contact]      |
+--------+--------+--------+--------+--------+---------------------+
|Customers|Subscri-|Conver- |Avg     |Avg Call|Cost per             |
|Contacted|ptions  |sion    |Contacts|Duration|Subscription         |
+--------+--------+--------+--------+--------+---------------------+
| Customers contacted + conversion | Conversion by contact channel |
| rate by month (combo chart)      | (column)                      |
+----------------------------------+-------------------------------+
| Conversion by number of contacts | Outcome mix (donut)           |
| (column)                         |                               |
+----------------------------------+-------------------------------+
```
| Visual | Type | Fields |
|---|---|---|
| 6 KPI cards | Card | `Customers Contacted`, `Subscriptions`, `Conversion Rate`, `Avg Contacts per Customer`, `Avg Call Duration (min)`, `Cost per Subscription` |
| Month combo | Line and clustered column | X `dim_month[month]`, columns `Customers Contacted`, line `Conversion Rate` |
| Channel | Clustered column | X `fact_campaign[contact]`, Y `Conversion Rate` |
| Contacts | Clustered column | X `contacts_band`, Y `Conversion Rate` |
| Outcome mix | Donut | Legend `outcome_label`, values `Customers Contacted` |

## Page 2: Customer Segments
```
+------------------------------------------------------------------+
| Who says yes?                             [Month] [Contact]      |
+---------------------------------+--------------------------------+
| Conversion by age band (column) | Conversion by job (bar, sorted)|
+---------------------------------+--------------------------------+
| Heat matrix: Age band x Job     | Education group | Marital     |
| group (conversion rate)         | (column)        | (column)    |
+---------------------------------+--------------------------------+
| Decomposition tree: Subscriptions, explain by Age band, Job group,|
| Education group, Contact, Previous outcome                        |
+------------------------------------------------------------------+
```
| Visual | Type | Fields |
|---|---|---|
| Age band | Clustered column | X `age_band`, Y `Conversion Rate` |
| Job | Bar | Y `dim_job[job]`, X `Conversion Rate (min 100 customers)`, sort descending |
| Heat matrix | Matrix | Rows `age_band`, Columns `dim_job[job_group]`, Values `Conversion Rate`; Background colour gradient (white to `#2A9D8F`) |
| Education | Clustered column | X `dim_education[education_group]`, Y `Conversion Rate` |
| Marital | Clustered column | X `marital`, Y `Conversion Rate` |
| Decomposition tree | AI visual | Analyze `Subscriptions`; Explain by the five fields listed |

## Page 3: Campaign Efficiency and Targeting
```
+------------------------------------------------------------------+
| Where does effort pay off?     [Month] [Contact] [Cost slicer]   |
+---------------------------------+--------------------------------+
| Cost per subscription by number | Conversion by previous campaign|
| of contacts (column)            | outcome (column, with Lift)    |
+---------------------------------+--------------------------------+
| Conversion by call duration     | Bubble: job, X customers,      |
| band (column)                   | Y conversion, size subscriptions|
+---------------------------------+--------------------------------+
| Top segments table (job group, age band, customers, conversion,  |
| lift), sorted by Lift                                            |
+------------------------------------------------------------------+
```
| Visual | Type | Fields |
|---|---|---|
| Cost by contacts | Clustered column | X `contacts_band`, Y `Cost per Subscription` |
| Previous outcome | Clustered column | X `poutcome`, Y `Conversion Rate`; add `Lift` in tooltips |
| Duration band | Clustered column | X `duration_band`, Y `Conversion Rate` |
| Job bubbles | Scatter | Details `dim_job[job]`, X `Customers Contacted`, Y `Conversion Rate`, Size `Subscriptions` |
| Top segments | Table | `dim_job[job_group]`, `age_band`, `Customers Contacted`, `Conversion Rate`, `Lift`; visual filter `Customers Contacted >= 100`; sort by `Lift` descending |

## Optional extras (good for interviews)
- A **balance band** chart (`balance_band`) if your file has the `balance` column (the bank-full version does).
- **Drill-through** from a job bar to a detail table of customers.
- A **Key influencers** AI visual on `outcome_label = Subscribed`.

## Insights to write in your README (after you build it)
Answer in plain business language: which months, channels and segments convert best, how conversion changes with the number of
contacts, whether a previous success predicts a new one, and what the cost per subscription tells you about when to stop calling.
