# Week 3 – Advanced Data Analysis and Visualization in Logistics

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458.svg)](https://pandas.pydata.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-0.12%2B-4c72b0.svg)](https://seaborn.pydata.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)

An enterprise-grade, reproducible logistics data analytics study evaluating **Logistics Delivery Performance, Shipment Volume, and Transportation Cost Analysis**. This project transforms 1,250 multi-modal freight shipment records into actionable supply chain intelligence through descriptive statistics, bivariate regressions, publication-grade visualizations, and structured bottleneck matrices.

---

## 📑 Table of Contents
- [Project Overview](#project-overview)
- [Objective](#objective)
- [Business Scenario](#business-scenario)
- [Dataset](#dataset)
- [Key Business Questions](#key-business-questions)
- [Enterprise Logistics KPIs](#enterprise-logistics-kpis)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Analysis Performed](#analysis-performed)
- [Visualizations Gallery](#visualizations-gallery)
- [Key Analytical Insights](#key-analytical-insights)
- [Operational Bottlenecks](#operational-bottlenecks)
- [Strategic Recommendations](#strategic-recommendations)
- [Future Data Science Scope](#future-data-science-scope)
- [Academic Documentation](#academic-documentation)

---

## 📦 Project Overview

Fulfillment speed, transportation spend, and delivery predictability directly dictate profitability and customer retention in modern supply chains. This repository contains the complete analytical pipeline for **Week 3: Advanced Data Analysis and Visualization in Logistics**, following the systematic progression:

$$\text{Logistics Data} \longrightarrow \text{EDA \& Descriptive Stats} \longrightarrow \text{Publication Visualizations} \longrightarrow \text{Evidence-Based Insights} \longrightarrow \text{Bottleneck Matrix} \longrightarrow \text{Actionable Recommendations}$$

---

## 🎯 Objective

1. Calculate comprehensive measures of central tendency, dispersion, and distribution symmetry for all logistics variables.
2. Formulate and compute core enterprise logistics Key Performance Indicators (KPIs).
3. Investigate the mathematical relationships and correlations between shipment distance, order quantity, freight mode, and transportation cost.
4. Diagnose localized failure points across regional destination markets and fulfillment origin hubs.
5. Generate 15 publication-grade, 300 DPI visualizations with modern design aesthetics.
6. Synthesize empirical findings into a structured Bottleneck Analysis Matrix and prioritized strategic transformation roadmap.

---

## 🏢 Business Scenario

**GlobalLogix Solutions** operates a multi-modal freight network across five geographic regions (North, South, East, West, Central), five warehouse hubs (`WH-Central`, `WH-East`, `WH-North`, `WH-South`, `WH-West`), and four commercial customer segments (Consumer, Corporate, Home Office, Small Business). 

GlobalLogix provides four freight service tiers:
* **Same-Day Courier** (1-Day SLA)
* **Express Air** (2-Day SLA)
* **Standard Delivery** (5-Day SLA)
* **Ground Freight** (7-Day SLA)

Despite commercial revenue growth in 2024, leadership observed increasing customer complaints regarding missed delivery windows and severe margin erosion in low-value product lines. This project performs an end-to-end diagnostic audit of operations.

---

## 📊 Dataset

* **Source:** Validated enterprise cleaned logistics dataset (`data/processed/logistics_cleaned.csv`).
* **Records Analyzed:** **1,250 shipments** (January 1, 2024 to June 30, 2024).
* **Feature Count:** **42 columns** (numerical, categorical, datetime, engineered, encoded, and normalized).
* **Data Hygiene:** 0 missing values, 0 duplicate rows, verified physical boundaries.

---

## ❓ Key Business Questions

* **BQ1:** What are the baseline central tendencies, dispersion spreads, and skewness characteristics of delivery transit times and shipping costs?
* **BQ2:** To what extent does transit distance determine shipping costs and delivery latency?
* **BQ3:** How reliably are contractual SLA timelines met across different shipping tiers?
* **BQ4:** Which geographic territories exhibit the highest fulfillment latencies, delay percentages, and customer dissatisfaction?
* **BQ5:** Which product categories bear disproportionately high logistics costs relative to their gross commercial value?
* **BQ6:** How do origin warehouse dispatch hubs interact with destination regions to create transit delays?
* **BQ7:** What operational anomalies exist in shipment distances, processing days, or expedited charges?
* **BQ8:** Where should supply chain leadership deploy capital investments to maximize ROI?

---

## 📈 Enterprise Logistics KPIs

| Corporate Logistics KPI | Empirical Metric Value | Operational Benchmark | Health Assessment |
| :--- | :---: | :---: | :--- |
| **Total Order Volume** | **1,250 Shipments** | N/A | Full semi-annual operational throughput |
| **Gross Commercial Sales** | **\$769,293.85** | N/A | Base commercial trading volume |
| **Total Transportation Spend** | **\$114,809.33** | N/A | Direct carrier freight spend |
| **Average Order Value (AOV)** | **\$615.44** | \$500.00 | Strong commercial basket size |
| **Average Shipping Cost** | **\$91.85** | < \$75.00 | Elevated due to express air mix |
| **Shipping Cost-to-Sales Ratio** | **14.92%** | < 10.00% | **High Margin Burden** |
| **Average Delivery Time** | **5.00 Days** | 4.00 Days | Moderate network transit latency |
| **Median Delivery Time** | **5.20 Days** | 4.00 Days | Reflects 5-day standard delivery dominance |
| **On-Time Delivery Rate** | **28.24%** | > 90.00% | **Critical Operational Failure** |
| **Delivery Delay Rate** | **71.76%** | < 10.00% | **Primary Network Bottleneck** (897 late orders) |
| **Average Transit Distance** | **819.43 KM** | N/A | Domestic multi-state distribution baseline |
| **Average Cost per KM** | **\$0.1302 / KM** | < \$0.1000/KM | Premium service tiers drive up unit cost |
| **Average Customer Rating** | **3.63 / 5.0** | > 4.20 / 5.0 | Subdued due to pervasive delivery delays |
| **Average Order Processing Days** | **2.43 Days** | < 1.50 Days | Warehouse dispatch dwell time consumes buffer |

---

## 💻 Technologies Used

* **Core Language:** Python 3.10+
* **Data Processing & Manipulation:** `pandas`, `numpy`
* **Descriptive & Inferential Statistics:** `scipy.stats`
* **Visualization & Plotting:** `matplotlib`, `seaborn`
* **Machine Learning & Preprocessing:** `scikit-learn`
* **Interactive Notebook:** `jupyter`, `nbclient`, `nbformat`, `ipykernel`

---

## 📁 Project Structure

```text
week3-logistics-advanced-analysis/
│
├── data/
│   ├── raw/
│   │   └── logistics_raw.csv                  <- Raw dataset for lineage
│   └── processed/
│       └── logistics_cleaned.csv              <- Primary cleaned dataset (1,250 records)
│
├── notebooks/
│   └── week3_logistics_analysis.ipynb         <- Executed 21-section interactive notebook
│
├── src/
│   ├── __init__.py
│   ├── analysis.py                            <- Data loading, grouping, KPI computation & aggregations
│   ├── statistics.py                          <- Central tendency, dispersion, skewness, correlations
│   ├── visualization.py                       <- 15 publication-quality visualization routines (300 DPI)
│   └── insights.py                            <- Automated insight extraction & bottleneck matrix generator
│
├── outputs/
│   ├── figures/                               <- 15 high-resolution (300 DPI) chart PNGs
│   │   ├── 01_delivery_time_distribution.png
│   │   ├── 02_shipping_cost_distribution.png
│   │   ├── 03_shipment_volume_by_region.png
│   │   ├── 04_avg_delivery_time_by_region_warehouse.png
│   │   ├── 05_shipping_cost_by_mode.png
│   │   ├── 06_delivery_time_by_mode.png
│   │   ├── 07_distance_vs_delivery_time.png
│   │   ├── 08_distance_vs_shipping_cost.png
│   │   ├── 09_correlation_heatmap.png
│   │   ├── 10_monthly_order_volume_cost_trend.png
│   │   ├── 11_quantity_vs_shipping_cost.png
│   │   ├── 12_product_category_performance.png
│   │   ├── 13_delivery_status_delay_rate_by_mode.png
│   │   ├── 14_customer_segment_comparison.png
│   │   └── 15_multivariate_delay_risk_matrix.png
│   └── reports/
│       ├── logistics_kpi_summary.csv
│       ├── descriptive_statistics_summary.csv
│       ├── correlation_matrix.csv
│       ├── correlation_pvalues.csv
│       ├── regional_performance_summary.csv
│       ├── shipping_mode_performance.csv
│       ├── category_performance_summary.csv
│       ├── customer_segment_summary.csv
│       ├── warehouse_performance_summary.csv
│       ├── temporal_trends_summary.csv
│       ├── outliers_iqr_summary.csv
│       ├── logistics_bottleneck_matrix.csv
│       ├── structured_insights.json
│       ├── strategic_recommendations.json
│       └── executive_summary_metrics.json
│
├── docs/
│   └── Week3_Advanced_Data_Analysis_and_Visualization.md <- Exhaustive 27-section academic report
│
├── run_pipeline.py                            <- End-to-end execution script
├── build_and_execute_notebook.py              <- Automated notebook build & execution runner
├── requirements.txt                           <- Strict dependency specifications
├── README.md                                  <- Project documentation
└── .gitignore                                 <- Standard Python & Jupyter ignore rules
```

---

## ⚙️ Installation

1. **Clone or Navigate to the Workspace:**
   ```bash
   cd C:\Users\ajayt\.gemini\antigravity-ide\scratch\week3-logistics-advanced-analysis
   ```

2. **Create a Virtual Environment (Optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   ```

3. **Install Required Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 How to Run

### Option 1: Run Full End-to-End Pipeline
Executes descriptive stats, KPI calculations, exports all 15 figures and 15 report summaries:
```bash
python run_pipeline.py
```

### Option 2: Rebuild & Execute Interactive Jupyter Notebook
Builds and executes `notebooks/week3_logistics_analysis.ipynb` with all outputs rendered:
```bash
python build_and_execute_notebook.py
```

### Option 3: Launch Jupyter Notebook Interactively
```bash
jupyter notebook notebooks/week3_logistics_analysis.ipynb
```

---

## 🔍 Analysis Performed

1. **Descriptive & Distributional Statistics:** Parametric (Mean, Trimmed Mean, Std Dev, Variance) and Non-Parametric (Median, IQR, Range) evaluations, Skewness and Kurtosis shape metrics.
2. **Univariate, Bivariate & Multivariate EDA:** Distribution densities, linear regressions, multi-factor interaction plots.
3. **Inferential Correlation Analysis:** Pearson $r$ coefficient matrix with two-tailed $p$-value hypothesis testing.
4. **Logistics KPI Framework:** Delivery latency, on-time delivery rate, delay rate, cost-per-km, cost-per-unit, shipping-to-sales ratios.
5. **Multidimensional Slicing:** Granular aggregations across geographic regions, carrier modes, warehouse origins, customer tiers, and monthly intervals.
6. **Outlier Detection:** Tukey's IQR rule boundaries and operational justification.
7. **Operational Bottleneck Matrix:** Identification of latency drivers and mitigation strategies.

---

## 🖼️ Visualizations Gallery

| Figure | Chart Name | Description | File Path |
| :---: | :--- | :--- | :--- |
| **01** | Delivery Time Distribution | Histogram + KDE showing probability density & median/mean markers | `outputs/figures/01_delivery_time_distribution.png` |
| **02** | Shipping Cost Distribution | Histogram + KDE showing right-skewed transportation spend | `outputs/figures/02_shipping_cost_distribution.png` |
| **03** | Shipment Volume by Region | Bar chart ranking volume and market share across destination regions | `outputs/figures/03_shipment_volume_by_region.png` |
| **04** | Avg Delivery Time by Hub & Region | Grouped bar chart comparing origin warehouse fulfillment latency | `outputs/figures/04_avg_delivery_time_by_region_warehouse.png` |
| **05** | Shipping Cost by Mode | Boxplot distribution of freight expenditure across service tiers | `outputs/figures/05_shipping_cost_by_mode.png` |
| **06** | Delivery Time vs. SLA | Boxplot comparing actual transit days vs contractual SLA targets | `outputs/figures/06_delivery_time_by_mode.png` |
| **07** | Distance vs Delivery Time | Scatter plot with modal hue and OLS trendline | `outputs/figures/07_distance_vs_delivery_time.png` |
| **08** | Distance vs Shipping Cost | Scatter plot with linear regression fit and $R^2$ annotation | `outputs/figures/08_distance_vs_shipping_cost.png` |
| **09** | Correlation Heatmap | Annotated Pearson correlation matrix of numerical features | `outputs/figures/09_correlation_heatmap.png` |
| **10** | Monthly Volume & Spend Trend | Dual-axis time series of order volume and freight spend | `outputs/figures/10_monthly_order_volume_cost_trend.png` |
| **11** | Quantity vs Shipping Cost | Multi-attribute scatter plot with category hue and sales size bubbles | `outputs/figures/11_quantity_vs_shipping_cost.png` |
| **12** | Product Category Performance | Dual-panel comparison of sales, freight cost, and burden ratio | `outputs/figures/12_product_category_performance.png` |
| **13** | Delivery Status by Mode | 100% stacked bar chart of on-time vs delayed proportions | `outputs/figures/13_delivery_status_delay_rate_by_mode.png` |
| **14** | Customer Segment Comparison | Dual-panel comparison of AOV, delay rate, and satisfaction | `outputs/figures/14_customer_segment_comparison.png` |
| **15** | Multivariate Risk Matrix | Cross-tabulated heatmap of delay rate by region and mode | `outputs/figures/15_multivariate_delay_risk_matrix.png` |

---

## 💡 Key Analytical Insights

1. **Systemic Network Delay Burden:** 71.76% of all network shipments (897 orders) experience delivery delays, driven primarily by internal warehouse dispatch dwell times (2.43 days avg).
2. **The Premium SLA Paradox:** Expedited tiers command extreme price premiums (**Same-Day Courier costs \$172.50/order, 3x Standard Delivery**), yet suffer the **highest delay rates (76.19%)**.
3. **Regional Friction in the South Corridor:** The **South** region records the longest delivery latency (**5.19 days**), highest delay rate (**76.98%**), and lowest customer rating (**3.50 / 5.0**).
4. **Severe Category Margin Destruction:** **Office Supplies** incurs an unsustainable **78.73% freight burden ratio** (\$27,939 shipping spend on \$35,487 sales), wiping out gross product profitability.
5. **Distance Cost Elasticity:** Distance accounts for 45% of total shipping cost variance ($r = +0.6724$, slope = \$0.061/KM), proving that point-to-point long-haul shipments require volume consolidation.

---

## ⚠️ Operational Bottlenecks

| Area | Primary Indicator | Empirical Evidence | Risk Assessment | Corrective Action |
| :--- | :--- | :--- | :--- | :--- |
| **South Region** | Delivery Latency & Delay Rate | **5.19 days** avg delivery time; **76.98% delay rate** | Long-haul distance and remote handoffs causing customer churn. | Establish regional cross-docking hub in Dallas/Atlanta. |
| **Same-Day Courier** | Contractual SLA Breach | **2.21 days** avg delivery (vs 1.0 day SLA); **76.19% delay rate** | Premium surcharge without delivery guarantee; refund exposure. | Restrict courier radius to 50 KM and deploy dedicated point-to-point fleets. |
| **Express Air** | Expedited Schedule Slippage | **2.94 days** avg delivery (vs 2.0 day SLA); **72.97% delay rate** | High spend (\$138.55/order) failing to deliver promised speed. | Enforce warehouse priority picking and strict carrier penalty chargebacks. |
| **Standard Delivery**| Core Network Delay Volume | **5.76 days** avg delivery (vs 5.0 day SLA); **469 delayed orders** | Core delivery backbone fails over 71% of the time. | Optimize line-haul schedules, deploy zone-skipping, and adjust customer EDDs. |
| **Office Supplies** | Freight Cost Drag | Shipping costs consume **78.73% of gross category sales** | Complete erosion of gross product margins; unprofitable fulfillment. | Enforce minimum order quantities (MOQs) and optimize cartonization. |
| **`WH-South` Hub** | Dispatch Dwell Time | **2.52 days** avg processing time; **75.4% delay rate** | Internal staging delays eat into carrier line-haul transit buffers. | Implement automated wave-picking and enforce same-day dispatch cutoffs. |

---

## 🎯 Strategic Recommendations

* **Phase 1: Immediate (0–3 Months):** Enforce carrier SLA penalty chargebacks, implement WMS 12-hour dispatch cutoffs, and mandate minimum order thresholds (\$50) for Office Supplies.
* **Phase 2: Medium-Term (3–6 Months):** Deploy regional cross-docking forward hubs in Dallas and Phoenix, implement automated 3D cartonization software, and deploy dynamic checkout EDD algorithms.
* **Phase 3: Long-Term (6–12 Months):** Build machine learning predictive delay classification engines and deploy a centralized IoT supply chain control tower.

---

## 🔮 Future Data Science Scope

* **Predictive Supervised ML:** Train `XGBoost` and `LightGBM` classifiers to score delay risks at the moment of order placement ($P(\text{Delayed}) > 0.60 \rightarrow \text{Auto-Expedite}$).
* **Continuous Cost Forecasting:** Train multi-variate regularized regressors (`ElasticNet`, `RandomForestRegressor`) to predict dynamic carrier freight costs.
* **Spatial & Customer Clustering:** Implement $K$-Means and DBSCAN algorithms for multi-stop vehicle route consolidation.
* **Facility Location Optimization:** Formulate Mixed-Integer Linear Programming (MILP) gravity models to identify optimal forward stocking coordinates.

---

## 📖 Academic Documentation

For the complete, exhaustive 27-section academic and professional report with formal chart justification frameworks and methodology breakdowns, refer to:
👉 **[docs/Week3_Advanced_Data_Analysis_and_Visualization.md](file:///C:/Users/ajayt/.gemini/antigravity-ide/scratch/week3-logistics-advanced-analysis/docs/Week3_Advanced_Data_Analysis_and_Visualization.md)**

---
*Created as part of the Logistics and Supply Chain Data Science Analytics Curriculum.*
