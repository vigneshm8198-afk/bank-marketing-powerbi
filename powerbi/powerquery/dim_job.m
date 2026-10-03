// Query name: dim_job
let
    Source = Csv.Document(File.Contents(DataFolder & "dim_job.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(Promoted, {{"job", type text}, {"job_group", type text}})
in
    Typed
