# 🌍 African Climate Trend Analysis — Week 0 Challenge

**10 Academy | AI Mastery Program | April 2026**

An exploratory and comparative analysis of historical climate data (2015–2026) across Ethiopia, Kenya, Sudan, Tanzania, and Nigeria — conducted in support of Ethiopia's preparation to host **COP32** in Addis Ababa, 2027.

---

## 📋 Project Overview

This project was completed as part of the 10 Academy Week 0 Challenge. It encompasses:

- **Task 1**: Git & Environment Setup with CI/CD
- **Task 2**: Per-country Data Profiling, Cleaning & EDA
- **Task 3**: Cross-Country Climate Vulnerability Comparison & Ranking
- **Bonus**: Interactive Streamlit Dashboard

**Data Source**: NASA POWER (Prediction of Worldwide Energy Resources)  
**Period**: January 2015 – March 2026  
**Countries**: Ethiopia, Kenya, Sudan, Tanzania, Nigeria

---

## 🗂️ Repository Structure

```
climate-challenge-week0/
├── .github/
│   └── workflows/
│       └── ci.yml                  # CI/CD pipeline
├── .gitignore
├── requirements.txt
├── README.md
├── src/
│   └── __init__.py
├── notebooks/
│   ├── __init__.py
│   ├── README.md
│   ├── ethiopia_eda.ipynb
│   ├── kenya_eda.ipynb
│   ├── sudan_eda.ipynb
│   ├── tanzania_eda.ipynb
│   ├── nigeria_eda.ipynb
│   └── compare_countries.ipynb
├── scripts/
│   ├── __init__.py
│   ├── README.md
│   └── data_cleaning.py            # Reusable cleaning functions
├── app/
│   ├── __init__.py
│   ├── main.py                     # Streamlit dashboard
│   └── utils.py                    # Utility functions
├── tests/
│   └── __init__.py
└── dashboard_screenshots/
    └── dashboard_preview.png
```

---

## ⚙️ Environment Setup

### Prerequisites
- Python 3.11+
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/climate-challenge-week0.git
cd climate-challenge-week0
```

### 2. Create Virtual Environment

**Using venv:**
```bash
python -m venv venv
source venv/bin/activate        # On Linux/Mac
venv\Scripts\activate           # On Windows
```

**Using conda:**
```bash
conda create -n climate-env python=3.11
conda activate climate-env
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Data Files

Download the NASA POWER CSVs from the challenge data link and place them in the `data/` directory:

```
data/
├── ethiopia.csv
├── kenya.csv
├── sudan.csv
├── tanzania.csv
└── nigeria.csv
```

> ⚠️ The `data/` directory is listed in `.gitignore` — **never commit raw or cleaned CSVs**.

---

## 🚀 Running the Notebooks

```bash
jupyter notebook notebooks/
```

Run notebooks in this order:
1. `ethiopia_eda.ipynb` (and repeat for other countries)
2. `compare_countries.ipynb`

---

## 📊 Running the Streamlit Dashboard

```bash
streamlit run app/main.py
```

The dashboard will open at `http://localhost:8501`

### Dashboard Features:
- 🌍 **Country multi-select** — filter by one or more countries
- 📅 **Year range slider** — zoom into specific periods
- 🌡️ **Variable selector** — switch between T2M, PRECTOTCORR, RH2M, and more
- 📈 **Temperature trend line chart**
- 🌧️ **Precipitation distribution boxplot**
- 🔥 **Extreme heat event frequency**

---

## 🔬 Key Findings

1. **Sudan** is the most thermally stressed country, with the highest mean temperatures and most extreme heat days (T2M_MAX > 35°C)
2. **Ethiopia** shows a statistically significant warming trend of ~0.3°C per decade
3. **Nigeria** exhibits the most volatile precipitation patterns, with increasing flood/drought alternation
4. **Tanzania** shows measurable shifts in rainy season onset (Masika rains arriving ~1–2 weeks later than the 2015 baseline)
5. The **Horn of Africa** (Ethiopia + Kenya) experienced its worst multi-year drought in 40 years (2020–2023), visible in the PRECTOTCORR time series

---

## 📄 Final Report

The final report (Medium blog style) is available as a PDF in this repository:  
📎 `final_report.pdf`

---

## 🔁 CI/CD

This repository uses **GitHub Actions** for continuous integration. On every push to `main`, the pipeline:
1. Sets up Python 3.11
2. Installs all dependencies from `requirements.txt`
3. Runs available unit tests
4. Validates core scripts

---

## 👤 Author

**[Your Name]**  
10 Academy — Week 0 Challenge, April 2026  
Data Engineering / Machine Learning Engineering Track

---

## 📚 References

- [NASA POWER Data](https://power.larc.nasa.gov/)
- [WMO State of Climate in Africa 2024](https://wmo.int/publication-series/state-of-climate-africa-2024)
- [World Bank Climate Risk Country Profiles](https://climateknowledgeportal.worldbank.org/)
- [IPCC Sixth Assessment Report — Africa Chapter](https://www.ipcc.ch/report/ar6/wg2/)
- [Power Shift Africa COP30 Scorecard](https://www.powershiftafrica.org/publications/cop30scorecard)
