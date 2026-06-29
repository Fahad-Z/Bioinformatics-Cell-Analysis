import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
from scipy.stats import mannwhitneyu


database_file = Path("cell_counts.db")
output_folder = Path("outputs")
output_folder.mkdir(exist_ok=True)

cell_types = [
    "b_cell",
    "cd8_t_cell",
    "cd4_t_cell",
    "nk_cell",
    "monocyte",
]


connection = sqlite3.connect(database_file)

data = pd.read_sql(
    "SELECT * FROM samples",
    connection,
)
connection.close()
data["total_count"] = data[cell_types].sum(axis=1)


summary = data.melt(
    id_vars=["sample", "total_count"],
    value_vars=cell_types,
    var_name="population",
    value_name="count",
)

summary["percentage"] = (
    summary["count"] / summary["total_count"]
) * 100

summary.to_csv(
    output_folder / "summary_table.csv",
    index=False,
)


long_data = data.melt(
    id_vars=[
        "project",
        "subject",
        "condition",
        "age",
        "sex",
        "treatment",
        "response",
        "sample",
        "sample_type",
        "time_from_treatment_start",
        "total_count",
    ],
    value_vars=cell_types,
    var_name="population",
    value_name="count",
)

long_data["percentage"] = (
    long_data["count"] / long_data["total_count"]
) * 100


analysis_data = long_data[
    (long_data["condition"].str.lower() == "melanoma")
    & (long_data["treatment"].str.lower() == "miraclib")
    & (long_data["sample_type"].str.upper() == "PBMC")
]

results = []

for population in cell_types:
    population_data = analysis_data[
        analysis_data["population"] == population
    ]
    responders = population_data[
        population_data["response"].str.lower() == "yes"
    ]["percentage"]
    non_responders = population_data[
        population_data["response"].str.lower() == "no"
    ]["percentage"]
    if len(responders) > 0 and len(non_responders) > 0:
        statistic, p_value = mannwhitneyu(
            responders,
            non_responders,
            alternative="two-sided",
        )
    else:
        p_value = None
    results.append(
        {
            "population": population,
            "responder_mean_percentage": responders.mean(),
            "non_responder_mean_percentage": non_responders.mean(),
            "p_value": p_value,
            "significant": (
                p_value is not None
                and p_value < 0.05
            ),
        }
    )

statistics = pd.DataFrame(results)
statistics.to_csv(
    output_folder / "statistics.csv",
    index=False,
)

figure = px.box(
    analysis_data,
    x="population",
    y="percentage",
    color="response",
    title="Responder vs Non-Responder Cell Frequencies",
)

figure.write_html(
    output_folder / "responder_boxplot.html"
)


baseline = data[
    (data["condition"].str.lower() == "melanoma")
    & (data["treatment"].str.lower() == "miraclib")
    & (data["sample_type"].str.upper() == "PBMC")
    & (data["time_from_treatment_start"] == 0)
]

baseline.to_csv(
    output_folder / "baseline_samples.csv",
    index=False,
)


print("\nBaseline Samples")

print(
    baseline.groupby("project")
    .size()
    .reset_index(name="sample_count")
)

print(
    baseline.groupby("response")
    .size()
    .reset_index(name="subject_count")
)

print(
    baseline.groupby("sex")
    .size()
    .reset_index(name="subject_count")
)

average_b_cells = baseline[
    (baseline["sex"] == "M")
    & (baseline["response"].str.lower() == "yes")
]["b_cell"].mean()

print(f"\nAverage B Cells (Male Responders): {average_b_cells:.2f}")