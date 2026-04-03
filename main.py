import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

df = pd.read_csv("C:/Users/Daniel/Downloads/SEMA_April 2019 excel sheet exercise.csv")
print(df.shape)
print(df.head(3))
print(df.dtypes)

import pandas as pd

# 4a — Subset and Rename
# We define core_cols to isolate only the variables needed for the research analysis
core_cols = [
    "start", "end", "Location",
    "Satisfaction (1 lowest 5 highest)",
    "Waiting time (minutes)",
    "Gender", "Approximate age", "Language",
    "Corruption", "Cooperative?",
    "Experiences or suggestions of citizens",
]

# Using .copy() ensures df_clean is a standalone object, avoiding SettingWithCopyWarnings
df_clean = df[core_cols].copy()

# Rename to standardized snake_case for easier coding and fewer typos
df_clean.rename(columns={
    "Satisfaction (1 lowest 5 highest)": "satisfaction",
    "Waiting time (minutes)": "wait_mins",
    "Approximate age": "age_group",
    "Cooperative?": "cooperative",
}, inplace=True)


# 4b — Handle Nulls and Fix Types
# Fill missing categorical values with 'Unknown' or 'No' to avoid dropping too much data
df_clean["age_group"]  = df_clean["age_group"].fillna("Unknown")
df_clean["Corruption"] = df_clean["Corruption"].fillna("No")

# Drop rows where 'satisfaction' is null as it is our primary dependent variable
df_clean = df_clean.dropna(subset=["satisfaction"])

# Ensure temporal columns are in datetime format with UTC awareness
df_clean["start"] = pd.to_datetime(df_clean["start"], utc=True)
df_clean["end"]   = pd.to_datetime(df_clean["end"],   utc=True)

# Convert strings to numeric; 'coerce' handles non-numeric entries by setting them to NaN
df_clean["satisfaction"] = pd.to_numeric(df_clean["satisfaction"], errors="coerce")
df_clean["wait_mins"]    = pd.to_numeric(df_clean["wait_mins"],    errors="coerce")

# Calculate duration to analyze service efficiency
df_clean["duration_mins"] = (df_clean["end"] - df_clean["start"]).dt.total_seconds() / 60

# 4c — Standardise Text Casing
# Updated include=["object", "string"] to prevent Pandas 4/3.0 deprecation warnings
# This captures both traditional object strings and the newer PyArrow-backed string types
str_cols = df_clean.select_dtypes(include=["object", "string"]).columns

# Clean up leading/trailing spaces and unify casing for categorical consistency
df_clean[str_cols] = df_clean[str_cols].apply(lambda x: x.str.strip())
df_clean["Gender"]     = df_clean["Gender"].str.title()
df_clean["Corruption"] = df_clean["Corruption"].str.capitalize()

# Check distribution to ensure cleaning worked as expected
print("Cleaned Corruption Counts:")
print(df_clean["Corruption"].value_counts())

# 4d — Export the Cleaned File
# Exporting without the index as it's usually not needed for external tools (Excel/SPSS)
df_clean.to_csv("sema_cleaned.csv", index=False)
print("\nProcess Complete: File saved as 'sema_cleaned.csv'")

import sqlite3

# Establish a connection to a local SQLite database file named 'sema.db'
# If the file doesn't exist, SQLite will create it automatically.
conn = sqlite3.connect("sema.db")

# Load the cleaned DataFrame into a SQL table named "feedback"
# if_exists="replace" ensures the table is overwritten if it already exists
df_clean.to_sql("feedback", conn, if_exists="replace", index=False)

# --- Analysis 1: Average satisfaction by location ---
# This query calculates volume, satisfaction, and efficiency (wait time) per location
sat_query = """
SELECT Location, 
       COUNT(*)                    AS total_responses, 
       ROUND(AVG(satisfaction), 2) AS avg_satisfaction, 
       ROUND(AVG(wait_mins), 1)    AS avg_wait_mins
FROM feedback
GROUP BY Location
ORDER BY avg_satisfaction DESC
"""
# Execute the query and store the results in a new DataFrame
result = pd.read_sql(sat_query, conn)
print("--- Average Satisfaction by Location ---")
print(result)

# --- Analysis 2: Corruption rate by office ---
# This query uses a CASE statement to count "Yes" responses and calculate a percentage
corr_query = """
SELECT Location,
       SUM(CASE WHEN Corruption='Yes' THEN 1 ELSE 0 END) AS corruption_cases,
       COUNT(*) AS total,
       ROUND(100.0 * SUM(CASE WHEN Corruption='Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct
FROM feedback
GROUP BY Location 
ORDER BY pct DESC
"""
corruption = pd.read_sql(corr_query, conn)
print("\n--- Corruption Rate by Office (%) ---")
print(corruption)

# --- Analysis 3: Gender breakdown by location ---
# First, we pull the raw counts of Gender per Location from SQL
gender_query = """
SELECT Location, Gender, COUNT(*) AS count
FROM feedback 
GROUP BY Location, Gender 
ORDER BY Location, Gender
"""
gender_loc = pd.read_sql(gender_query, conn)

# Use Pandas pivot to transform the data:
# Locations become rows, Genders become columns for a "Heatmap" style view.
# .fillna(0) ensures locations with 0 of a specific gender show 0 instead of NaN.
pivot = gender_loc.pivot(index="Location", columns="Gender", values="count").fillna(0)

print("\n--- Gender Distribution Pivot Table ---")
print(pivot)

# Best practice: Close the database connection when finished
# conn.close()

import matplotlib.pyplot as plt
import seaborn as sns

# --- Chart 1: Satisfaction by Location (Horizontal Bar) ---
# Group by location and calculate the mean satisfaction, sorting for a cleaner visual hierarchy
sat_by_loc = df_clean.groupby("Location")["satisfaction"].mean().sort_values()

# Initialize the plot; figsize (width, height) ensures labels aren't cramped
fig, ax = plt.subplots(figsize=(10, 5))

# Plotting a horizontal bar chart (barh) which is easier to read for long location names
sat_by_loc.plot(kind="barh", ax=ax, color="#378ADD", edgecolor="none")

# Customizing labels and titles for clarity
ax.set_xlabel("Average Satisfaction (1–5)")
ax.set_title("Citizen Satisfaction by Office — April 2019")

# Add a vertical reference line at the 'neutral' score (3) to easily identify high/low performers
ax.axvline(x=3, color="gray", linestyle="--", linewidth=0.8)

# Adjust layout to prevent label clipping and save high-resolution PNG (150 DPI)
plt.tight_layout()
plt.savefig("satisfaction_by_location.png", dpi=150)
plt.show()


# --- Chart 2: Gender Distribution (Pie Chart) ---
# Calculate frequencies of each gender category
gender_counts = df_clean["Gender"].value_counts()

fig, ax = plt.subplots(figsize=(5, 5))

# autopct adds percentages automatically; startangle=90 rotates the start for better aesthetics
ax.pie(gender_counts, labels=gender_counts.index,
       autopct="%1.1f%%", colors=["#378ADD", "#D4537E"], startangle=90)

ax.set_title("Survey Respondents by Gender")

# Save the pie chart for use in reports
plt.savefig("gender_distribution.png", dpi=150)
plt.show()


# --- Chart 3: Satisfaction vs Wait Time (Heatmap) ---
# Binning the continuous 'wait_mins' variable into meaningful time categories
df_clean["wait_bin"] = pd.cut(
    df_clean["wait_mins"],
    bins=[0, 15, 30, 60, 120, 999],
    labels=["0–15m", "15–30m", "30–60m", "1–2hr", "2hr+"])

# Create a pivot table where rows are wait times and columns are locations
# The values inside the cells represent the average satisfaction score
pivot_heat = df_clean.pivot_table(
    values="satisfaction", index="wait_bin",
    columns="Location", aggfunc="mean")

fig, ax = plt.subplots(figsize=(11, 4))

# sns.heatmap provides a color-coded matrix; annot=True prints the scores inside the boxes
# fmt=".1f" rounds numbers to one decimal place; cmap="Blues" sets the color intensity
sns.heatmap(pivot_heat, annot=True, fmt=".1f", cmap="Blues", ax=ax, linewidths=0.5)

ax.set_title("Avg Satisfaction by Wait Time and Location")

# Finalize layout and export the visualization
plt.tight_layout()
plt.savefig("heatmap_satisfaction_wait.png", dpi=150)
plt.show()