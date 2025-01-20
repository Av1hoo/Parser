import polars as pl

# Create a sample CSV for testing
import pandas as pd

sample_data = {
    "Sample Name": ["FORMULATION A", "FORMULATION B", "STD 1", "FORMULATION A"],
    "Zeta Potential (mV)": [15, 20, 10, 25]
}

# Save to a temporary CSV
pd.DataFrame(sample_data).to_csv("temp_test.csv", index=False)

# Read with Polars
df = pl.read_csv("temp_test.csv")
print(f"Type of df: {type(df)}")

# Rename columns
df = df.rename({
    "Sample Name": "SampleName",
    "Zeta Potential (mV)": "ZetaPotential"
})

# Filter formulations
formulation_df = df.filter(pl.col("SampleName").str.starts_with("FORMULATION"))
print(f"Type of formulation_df: {type(formulation_df)}")

# Groupby
grouped = (
    formulation_df
    .group_by("SampleName", maintain_order=True)
    .agg(pl.col("ZetaPotential").mean().alias("mean_reading"))
)

print(grouped)
