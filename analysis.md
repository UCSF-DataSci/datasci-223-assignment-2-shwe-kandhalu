## Approach

goal was to examine trends in patient glucose and age levels based on BMI categories. We used a large dataset (`patients_large.csv`) containing 5 million synthetic patient records and converted it to a Parquet file to improve data processing performance.

after filtering out BMI outliers (BMI < 10 or > 60), we categorized patients into four standard WHO BMI groups:
- Underweight: 10 ≤ BMI < 18.5
- Normal: 18.5 ≤ BMI < 25
- Overweight: 25 ≤ BMI < 30
- Obese: 30 ≤ BMI ≤ 60

for each BMI range, we calculated:
- avg glucose (`avg_glucose`)
- avg age (`avg_age`)
- patient count (`patient_count`)

final output was a Polars DataFrame summarizing this information

## Insights

from cohort analysis, we observed tat:
- Obese group tended to have higher average glucose levels
- Normal and Overweight categories contain majority of patients
- Mild positive trend between age and BMI in some groups

these patterns can be helpful for identifying at-risk populations

## use of Polars for Efficiency

to process the dataset:
- used Polars' **lazy evaluation** via `scan_parquet()` to defer execution
- enabled **streaming** with `.collect(streaming=True)` to handle large-scale computation

using Polars lets us process millions of rows fast and w low memory usage, which is ideal for health data analysis at scale
