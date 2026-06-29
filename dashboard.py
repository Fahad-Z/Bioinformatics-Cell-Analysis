from pathlib import Path
import pandas as pd
import streamlit as st


output_folder = Path("outputs")
st.title("Immune Cell Analysis Dashboard")

summary = pd.read_csv(output_folder / "summary_table.csv")
statistics = pd.read_csv(output_folder / "statistics.csv")
baseline = pd.read_csv(output_folder / "baseline_samples.csv")


st.header("Part 2: Cell Population")
st.dataframe(summary)

st.header("Part 3: Statistical Analysis")
st.subheader("Responder vs Non-Responder Statistics")
st.dataframe(statistics)

st.subheader("Boxplot")
html = (output_folder / "responder_boxplot.html").read_text(
    encoding="utf-8"
)
st.components.v1.html(html, height=650)

st.header("Part 4: Baseline Melanoma PBMC Samples")
st.subheader("Baseline Samples")
st.dataframe(baseline)


st.subheader("Samples per Project")
project_counts = (
    baseline.groupby("project")
    .size()
    .reset_index(name="sample_count")
)
st.dataframe(project_counts)


st.subheader("Responders vs Non-Responders")
response_counts = (
    baseline.groupby("response")
    .size()
    .reset_index(name="subject_count")
)

st.dataframe(response_counts)
st.subheader("Males vs Females")
gender_counts = (
    baseline.groupby("sex")
    .size()
    .reset_index(name="subject_count")
)

st.dataframe(gender_counts)
st.subheader("Average B Cells (Male Responders at Baseline)")

average_b_cells = baseline[
    (baseline["sex"] == "M")
    & (baseline["response"].str.lower() == "yes")
]["b_cell"].mean()

st.metric(
    "Average B Cells",
    f"{average_b_cells:.2f}",
)