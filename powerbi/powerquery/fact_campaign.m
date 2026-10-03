// Query name: fact_campaign
// Home > Transform data > New Source > Blank Query > Advanced Editor > paste all of this.
let
    Source = Csv.Document(
        File.Contents(DataFolder & "campaign_clean.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),

    // Empty text cells become real nulls so number conversion does not fail (balance may be empty)
    BlanksToNull = Table.ReplaceValue(Promoted, "", null, Replacer.ReplaceValue, Table.ColumnNames(Promoted)),

    Typed = Table.TransformColumnTypes(
        BlanksToNull,
        {
            {"customer_id", Int64.Type}, {"age", Int64.Type},
            {"job", type text}, {"marital", type text}, {"education", type text},
            {"credit_default", type text}, {"housing_loan", type text}, {"personal_loan", type text},
            {"contact", type text}, {"month", type text}, {"month_num", Int64.Type},
            {"day_of_week", type text}, {"balance", type number},
            {"duration_sec", Int64.Type}, {"campaign", Int64.Type}, {"pdays", Int64.Type}, {"previous", Int64.Type},
            {"previously_contacted", type text}, {"poutcome", type text},
            {"subscribed", Int64.Type}, {"outcome_label", type text}
        },
        "en-US"
    ),

    // Bands. The leading number makes them sort correctly on charts.
    AddAgeBand = Table.AddColumn(Typed, "age_band", each
        if [age] < 25 then "1. Under 25"
        else if [age] < 35 then "2. 25 to 34"
        else if [age] < 45 then "3. 35 to 44"
        else if [age] < 55 then "4. 45 to 54"
        else if [age] < 65 then "5. 55 to 64"
        else "6. 65 and over", type text),

    AddDurationBand = Table.AddColumn(AddAgeBand, "duration_band", each
        if [duration_sec] < 60 then "1. Under 1 min"
        else if [duration_sec] < 180 then "2. 1 to 3 min"
        else if [duration_sec] < 300 then "3. 3 to 5 min"
        else if [duration_sec] < 600 then "4. 5 to 10 min"
        else "5. 10 min and over", type text),

    AddContactsBand = Table.AddColumn(AddDurationBand, "contacts_band", each
        if [campaign] = 1 then "1. One contact"
        else if [campaign] = 2 then "2. Two contacts"
        else if [campaign] = 3 then "3. Three contacts"
        else if [campaign] = 4 then "4. Four contacts"
        else "5. Five or more", type text),

    AddBalanceBand = Table.AddColumn(AddContactsBand, "balance_band", each
        if [balance] = null then "5. Not in dataset"
        else if [balance] < 0 then "1. Negative"
        else if [balance] < 1000 then "2. 0 to 999"
        else if [balance] < 5000 then "3. 1,000 to 4,999"
        else "4. 5,000 and above", type text)
in
    AddBalanceBand
