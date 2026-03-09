"""
clean_data.py

This script reads the raw dataset from data/raw/, performs basic cleaning,
creates useful derived variables, and saves a cleaned version to data/clean/.

Cleaning steps include:
- renaming unclear variable names
- handling missing values and inconsistent coding
- converting quarter labels (Q1-Q4) into a numeric quarter_num variable
- creating employment rate as 100 - unemployment_rate
- sorting rows by state, year, and quarter_num

The raw data file is never overwritten.
"""

from pathlib import Path
import pandas as pd

# Define file paths
project_root = Path(__file__).resolve().parents[1]
raw_file = project_root / "data" / "raw" / "your_raw_file.csv"
clean_file = project_root / "data" / "clean" / "cleaned_data.csv"

# Read raw data
df = pd.read_csv(raw_file)

# Preview columns
print("Original columns:", df.columns.tolist())

# Rename unclear columns if needed
df = df.rename(columns={
    "State": "state",
    "Year": "year",
    "Quarter": "quarter",
    "UnemploymentRate": "unemployment_rate"
})

# Standardise text values
if "state" in df.columns:
    df["state"] = df["state"].astype(str).str.strip()

if "quarter" in df.columns:
    df["quarter"] = df["quarter"].astype(str).str.strip().str.upper()

# Convert quarter labels to numeric
quarter_map = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4}
if "quarter" in df.columns:
    df["quarter_num"] = df["quarter"].map(quarter_map)

# Convert numeric columns
for col in ["year", "unemployment_rate"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Handle obvious missing values
df = df.dropna(subset=["state", "year", "quarter", "unemployment_rate"])

# Create employment rate
df["emp_rate"] = 100 - df["unemployment_rate"]

# Sort rows
df = df.sort_values(by=["state", "year", "quarter_num"]).reset_index(drop=True)

# Save cleaned data
clean_file.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(clean_file, index=False)

print(f"Cleaned data saved to: {clean_file}")
