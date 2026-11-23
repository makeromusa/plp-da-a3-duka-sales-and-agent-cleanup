# Duka Sales Exploration and Agent Network Clean-Up

**Course:** Data Analytics with Python (PLP Academy) — Week 3  
**Author:** Asman Makero Musa  
**Cohort:** PLP Data Analytics Cohort 7  
**Repository:** `plp-da-a3-duka-sales-and-agent-cleanup`

---

## Project Overview

This repository contains two comprehensive analytical engagements addressing data exploration, data quality auditing, programmatic pipeline development, and regulatory compliance.

### Engagement 1: Duka Electronics Half-Year Sales Exploration
An end-to-end retail sales analysis of Duka Electronics across 5 nationwide branches (Nairobi, Mombasa, Kisumu, Nakuru, Eldoret) for the first half of 2026 (January 1 – June 29). The analysis evaluates branch revenue contributions, product category unit/revenue rankings, weekday versus weekend buying patterns, monthly seasonality, and exports high-value customer segments while reconciling findings with an automated Excel model (`excel/duka_branch_summary.xlsx`).

### Engagement 2: Mobile Money Agent Network Data Audit and Cleaning
A production-grade data quality audit and cleaning pipeline for an East African mobile money agent network. The project assesses data health across all six dimensions of data quality (Uniqueness, Consistency, Completeness, Validity, Accuracy, Timeliness), implements a modular cleaning script (`cleaning_pipeline.py`), links transaction records with an agent metadata registry, generates analytical aggregations (county summary and weekly pivot tables), exports the clean dataset (`outputs/agent_transactions_clean.csv`), and documents regulatory compliance under the **Kenya Data Protection Act 2019**.

---

## Duka Electronics Executive Summary

- Duka Electronics generated total revenue of **KES 71,792,500** across **1,000 orders** (3,012 units sold) during H1 2026.
- Nairobi led all branches with **KES 26,106,100** (36.4% share) across **376 orders**, almost double Mombasa in second place at **KES 14,003,700** (186 orders).
- Laptops drove financial performance with **KES 41,535,000** (57.9% of revenue) despite Tablets leading unit sales with **691 units**.
- Weekdays contributed **723 orders** (KES 51,856,200) and weekends produced **277 orders** (KES 19,936,300), with nearly identical average order values of **KES 71,724** and **KES 71,972**.
- April was the peak revenue month at **KES 13,518,300**, exceeding the lowest month, June (**KES 10,903,400**), by **23.98%**.

---

## Agent Network Data: Before-and-After Row Count

| Metric | Raw Dataset (`agent_transactions.csv`) | Cleaned Dataset (`agent_transactions_clean.csv`) | Net Change / Action |
| :--- | :--- | :--- | :--- |
| **Total Rows** | **612** | **600** | **-12 duplicate rows removed** |
| **Unique Transaction IDs** | 600 | 600 | 100% primary key uniqueness |
| **Missing Amounts** | 20 (15 NaN, 5 `'N/A'`) | 0 | Imputed with median (KES 1,776), flagged in `amount_imputed` |
| **Slash Date Formats** | 5 (`YYYY/MM/DD`) | 0 | Converted to standard ISO datetime (`YYYY-MM-DD`) |
| **Unregistered Agents** | 7 (`AG099`) | 7 | Retained and categorized under `county="Unknown"` |
| **High-Value Outliers** | 53 | 53 | Flagged in `is_outlier` (> KES 5,513.75 IQR fence) |

---

## How to Regenerate Data and Run Notebooks

### 1. Environment Setup
Clone the repository and install the verified dependencies:
```bash
git clone https://github.com/makeromusa/plp-da-a3-duka-sales-and-agent-cleanup.git
cd plp-da-a3-duka-sales-and-agent-cleanup
pip install -r requirements.txt
```

### 2. Regenerate Synthetic Datasets
Run `generate_data.py` to generate the raw CSV files using the fixed random seeds (Duka seed: `2026`, Agent seed: `44`):
```bash
python generate_data.py
```
This produces:
- `duka_sales.csv` (1,000 orders)
- `agents.csv` (20 registered agents)
- `agent_transactions.csv` (612 raw transactions)

### 3. Run the Analytical Notebooks
Open and execute the Jupyter notebooks sequentially from top to bottom:
```bash
# Engagement 1: Sales exploration & Excel reconciliation
jupyter notebook duka_sales_exploration.ipynb

# Engagement 2: Agent network data cleaning & audit report
jupyter notebook agent_cleanup.ipynb
```

---

## Repository Structure

```
plp-da-a3-duka-sales-and-agent-cleanup/
├── .gitignore                          # Excludes raw CSVs and temp build files
├── README.md                           # Project documentation, summaries & run guide
├── requirements.txt                    # Project dependencies (pandas, numpy, openpyxl)
├── generate_data.py                    # Unchanged synthetic data generators
├── cleaning_pipeline.py                # Modular clean_agent_data(txns, agents) function
├── duka_sales_exploration.ipynb        # Engagement 1 notebook with all tasks & answers
├── agent_cleanup.ipynb                 # Engagement 2 notebook with audit & data quality report
├── excel/
│   └── duka_branch_summary.xlsx        # Excel workbook (SUMIFS, XLOOKUP, PivotTable)
└── outputs/
    ├── premium_online_coast_capital.csv # Filtered premium online orders (83 rows)
    └── agent_transactions_clean.csv     # Cleaned 600-row agent transaction dataset
```

---

## Key Business Insights & Regulatory Compliance

1. **Revenue Drivers:** Laptop sales are the single greatest driver of Duka's profitability (57.9% of total revenue). Nairobi and Mombasa account for 55.9% of company revenue.
2. **Channel Consistency:** Average basket size is steady across weekdays and weekends (~KES 71k), demonstrating consistent commercial buying patterns across in-store and online channels.
3. **Data Quality & AML Risk:** In the agent network, 5 artificial spikes of KES 250,000 were identified exceeding normal mobile money limits, necessitating automated alerts and Anti-Money Laundering (AML) review.
4. **Kenya Data Protection Act 2019:** Personal transaction identifiers, MSISDN customer contact numbers, and geographic location tags are classified as protected personal data. Analytical pipelines must employ pseudonymisation (salted SHA-256 hashes) and masking (`0712****78`) before data is made available for reporting.
