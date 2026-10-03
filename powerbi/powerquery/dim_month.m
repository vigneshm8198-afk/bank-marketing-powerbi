// Query name: dim_month
let
    Source = Csv.Document(File.Contents(DataFolder & "dim_month.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(Promoted, {{"month", type text}, {"month_num", Int64.Type}, {"quarter", type text}})
in
    Typed
