# Data model (star schema)

```mermaid
erDiagram
    dim_month     ||--o{ fact_campaign : "month"
    dim_job       ||--o{ fact_campaign : "job"
    dim_education ||--o{ fact_campaign : "education"

    fact_campaign {
        int customer_id
        int age
        text job
        text education
        text contact
        text month
        int duration_sec
        int campaign
        int pdays
        text poutcome
        int subscribed
    }
    dim_month {
        text month
        int month_num
        text quarter
    }
    dim_job {
        text job
        text job_group
    }
    dim_education {
        text education
        text education_group
    }
```

`fact_campaign` has one row per customer contacted. Power Query adds `age_band`, `duration_band`, `contacts_band`, `balance_band`.
`_Measures` holds only measures. `Cost per Contact` is the What-if parameter table (no relationships).

## Key definitions
| Term | Definition |
|---|---|
| Customer contacted | One row in the dataset |
| Subscription | Customer said yes to the term deposit (`subscribed = 1`) |
| Conversion rate | Subscriptions / customers contacted |
| Lift | Segment conversion rate / overall conversion rate (above 1 means better than average) |
| Contacts | Number of calls made to the customer in this campaign (`campaign` column) |
| Cost per subscription | (Total contacts x assumed cost per contact) / subscriptions |
| Previous campaign outcome | Result of an earlier campaign; "No previous campaign" if the customer was not contacted before |
