# 🏛️ SEMA Citizen Feedback — Data Analysis Project

> **Analysing citizen satisfaction, wait times, corruption incidents, and gender distribution across 8 Kampala public offices using Python, SQL, and data visualisation.**

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-Visualisation-4C72B0)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Table of Contents

- [About the Project](#-about-the-project)
- [About SEMA](#-about-sema)
- [Dataset Overview](#-dataset-overview)
- [Project Structure](#-project-structure)
- [Key Findings](#-key-findings)
- [Visualisations](#-visualisations)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [SQL Analyses](#-sql-analyses)
- [Author](#-author)

---

## 📖 About the Project

This project was completed as a **Research Data Manager assignment** for SEMA Uganda. It demonstrates an end-to-end data pipeline — from raw survey data ingestion, through cleaning and transformation, to SQL-powered analysis and publication-ready visualisations.

The dataset consists of **1,106 in-person citizen feedback responses** collected in **April 2019** across **8 public offices** in Kampala, Uganda — covering 5 Uganda Police stations and 3 KCCA (Kampala Capital City Authority) service centres.

The work directly supports SEMA's alignment with **United Nations SDG 16.6**: *"Develop effective, accountable, and transparent institutions at all levels."*

---

## 🌍 About SEMA

[SEMA](https://talktosema.org) is an award-winning Ugandan civic technology and social enterprise founded in 2018. Their mission is to amplify citizens' voices and drive evidence-based reform across East Africa's public institutions — using accessible feedback tools (IoT smiley-face devices, USSD, IVR phone lines, WhatsApp) to bridge the gap between citizens and the institutions that serve them.

| Impact Metric | Value |
|---|---|
| Citizens Reached | 100,000+ |
| Partner Offices | 26 |
| Data Reports Published | 192+ |
| Feedback Channels | 3 |
| Wait Time Reduction | 80% |
| Satisfaction Increase | 62% |
| UN Goal | SDG 16.6 Aligned |

---

## 📊 Dataset Overview

| Field | Description |
|---|---|
| `start` / `end` | Survey start and end timestamps (UTC) |
| `Location` | Public office name (8 locations) |
| `satisfaction` | Citizen rating: 1 (lowest) to 5 (highest) |
| `wait_mins` | Time spent waiting before service (minutes) |
| `Gender` | Respondent gender |
| `age_group` | Approximate age bracket |
| `Language` | Language used during interaction |
| `Corruption` | Whether a corruption incident was reported (Yes/No) |
| `cooperative` | Whether the officer was cooperative |
| `Experiences or suggestions` | Open-ended citizen feedback |
| `duration_mins` | Derived: total service duration in minutes |
| `wait_bin` | Derived: categorised wait time band |

**Source:** `SEMA_April 2019 excel sheet exercise.csv` → Cleaned output: `sema_cleaned.csv`

---

## 🗂️ Project Structure

```
Research_Data_Manager_Task_Charles/
│
├── main.py                          # Core pipeline: ingest → clean → analyse → visualise
├── sema_cleaned.csv                 # Cleaned dataset (exported from main.py)
├── sema.db                          # SQLite database (feedback table)
│
├── satisfaction_by_location.png     # Chart 1: Avg satisfaction per office
├── gender_distribution.png          # Chart 2: Gender breakdown pie chart
├── heatmap_satisfaction_wait.png    # Chart 3: Satisfaction × Wait Time heatmap
│
├── Impact_Statement_Charles_Daniel.pdf   # Written impact and findings report
└── SEMA_Citizen_Feedback_Short_Presentation.ppt  # Stakeholder slide deck
```

---

## 🔍 Key Findings

### 🏆 Satisfaction by Office
All 8 offices scored **above the neutral midpoint of 3/5**, reflecting a baseline of adequate service delivery.

| Rank | Office | Avg Satisfaction |
|---|---|---|
| 1 | KCCA (Headquarters) | 3.35 / 5 |
| 2 | UG Police (Ntinda) | 3.33 / 5 |
| 3 | KCCA (Naguru) | 3.30 / 5 |
| 4 | KCCA (Central Division) | 3.26 / 5 |
| 5 | UG Police (Jinja Rd) | 3.19 / 5 |
| 6 | UG Police (Kira Road) | 3.17 / 5 |
| 7 | UG Police (CPS) | 3.06 / 5 |
| 8 | UG Police (Wandegeya) | 3.05 / 5 |

### ⏱️ Wait Time vs. Satisfaction
Citizens who waited **under 15 minutes** consistently recorded the highest satisfaction scores across all offices — confirming that **reducing queue times is one of the most actionable levers** for improving citizen experience.

### 👥 Gender Distribution
- **58.9% Male** | **41.1% Female** respondents
- 65% of respondents were aged 30–50
- SEMA's longitudinal data shows women wait longer and are less likely to receive resolutions — making gender-disaggregated tracking essential

### 🚨 Corruption Monitoring
| Metric | Value |
|---|---|
| Corruption Incidents Reported | 33 |
| Overall Corruption Rate | 3% |
| Respondents Reporting No Corruption | 97% |

> ⚠️ While April 2019 data shows a 3% rate, Transparency International (2018) reports that nearly **40% of Ugandans** have paid a bribe to access public services at some point — underscoring the value of SEMA's real-time, anonymous reporting system.

---

## 📈 Visualisations

### Chart 1 — Citizen Satisfaction by Office
Horizontal bar chart showing average satisfaction per location, sorted by score, with a neutral reference line at 3.0.

### Chart 2 — Survey Respondents by Gender
Pie chart showing the gender split across all 1,106 responses.

### Chart 3 — Satisfaction vs. Wait Time Heatmap
Cross-tabulated heatmap showing how average satisfaction scores vary by both **wait time band** and **office location**.

All charts are saved at **150 DPI** as PNG files for use in reports and presentations.

---

## 🛠️ Tech Stack

| Tool / Library | Purpose |
|---|---|
| **Python 3.10+** | Core programming language |
| **pandas** | Data ingestion, cleaning, transformation |
| **openpyxl** | Excel (.xlsx) file reading engine |
| **matplotlib** | Base plotting framework |
| **seaborn** | Statistical heatmap visualisation |
| **sqlite3** | Embedded SQL database creation and querying |
| **sqlalchemy** | pandas ↔ SQLite ORM bridge |
| **PyCharm** | Development IDE |
| **Claude AI** | Code review, debugging, and structure guidance |

---

## 🚀 Getting Started

### Prerequisites
Make sure you have Python 3.10+ installed.

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/sema-citizen-feedback-analysis.git
cd sema-citizen-feedback-analysis
```

### 2. Create a Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows
```

### 3. Install Dependencies
```bash
pip install pandas openpyxl matplotlib seaborn sqlalchemy
```

### 4. Add the Raw Data File
Place the raw survey file in the project root and update the file path in `main.py`:
```python
df = pd.read_csv("your_path/SEMA_April_2019_excel_sheet_exercise.csv")
```

### 5. Run the Pipeline
```bash
python main.py
```

This will:
- ✅ Load and inspect the raw dataset
- ✅ Clean and standardise all columns
- ✅ Export `sema_cleaned.csv`
- ✅ Load data into `sema.db` (SQLite)
- ✅ Run SQL analyses and print results
- ✅ Generate and save all 3 visualisation charts

---

## 🗄️ SQL Analyses

Three SQL queries are executed against the `feedback` table in `sema.db`:

**1. Average Satisfaction by Location**
```sql
SELECT Location,
       COUNT(*)                    AS total_responses,
       ROUND(AVG(satisfaction), 2) AS avg_satisfaction,
       ROUND(AVG(wait_mins), 1)    AS avg_wait_mins
FROM feedback
GROUP BY Location
ORDER BY avg_satisfaction DESC;
```

**2. Corruption Rate by Office**
```sql
SELECT Location,
       SUM(CASE WHEN Corruption='Yes' THEN 1 ELSE 0 END) AS corruption_cases,
       COUNT(*) AS total,
       ROUND(100.0 * SUM(CASE WHEN Corruption='Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct
FROM feedback
GROUP BY Location
ORDER BY pct DESC;
```

**3. Gender Distribution by Location**
```sql
SELECT Location, Gender, COUNT(*) AS count
FROM feedback
GROUP BY Location, Gender
ORDER BY Location, Gender;
```

---

## ✍️ Author

**Charles Daniel Apollo**
Research Data Manager | Civic Technology Enthusiast

This project represents 12 hours of end-to-end analysis work — from raw data to insights. It deepened my appreciation for SEMA's mission and the significant potential to expand this citizen feedback model across other East African countries including Kenya, Tanzania, and Rwanda, where similar accountability gaps exist at the public service level.

---

## 🙏 Acknowledgements

- [SEMA Uganda](https://talktosema.org) — for the dataset and the remarkable mission of amplifying citizen voices
- [Transparency International](https://www.transparency.org) — corruption perception benchmarks
- [United Nations SDG 16](https://sdgs.un.org/goals/goal16) — the global framework this work supports

---

*"By 2030, all public service providers in East Africa will use citizen feedback to improve their service delivery." — SEMA's Big Hairy Audacious Goal*
