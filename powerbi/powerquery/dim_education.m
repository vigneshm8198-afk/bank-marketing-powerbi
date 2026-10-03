// Query name: dim_education
let
    Source = Csv.Document(File.Contents(DataFolder & "dim_education.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed = Table.TransformColumnTypes(Promoted, {{"education", type text}, {"education_group", type text}})
in
    Typed
