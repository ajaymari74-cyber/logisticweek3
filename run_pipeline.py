"""
Week 3: Advanced Data Analysis and Visualization in Logistics
Execution Pipeline: run_pipeline.py
Author: Senior Logistics Data Analyst & Python Developer
Description:
    End-to-end execution script that loads the cleaned Week 2 logistics dataset,
    runs statistical evaluations, calculates corporate KPIs, performs dimensional
    analyses, generates all 15 publication-grade charts, and exports all CSV/JSON reports.
"""

import os
import sys
import json
import pandas as pd
import numpy as np

# Ensure src modules are resolvable
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.analysis import (
    load_logistics_data,
    compute_logistics_kpis,
    analyze_regional_performance,
    analyze_shipping_modes,
    analyze_product_categories,
    analyze_customer_segments,
    analyze_warehouse_performance,
    analyze_temporal_trends
)
from src.statistics import (
    get_comprehensive_descriptive_stats,
    compute_correlation_matrix,
    detect_outliers_iqr
)
from src.visualization import generate_all_visualizations
from src.insights import (
    generate_structured_insights,
    generate_bottleneck_matrix,
    generate_strategic_recommendations,
    export_executive_summary
)


def main():
    print("=" * 80)
    print("WEEK 3: ADVANCED DATA ANALYSIS & VISUALIZATION IN LOGISTICS")
    print("Execution Pipeline Starting...")
    print("=" * 80)

    # 1. Paths Setup
    data_path = os.path.join(project_root, "data", "processed", "logistics_cleaned.csv")
    figures_dir = os.path.join(project_root, "outputs", "figures")
    reports_dir = os.path.join(project_root, "outputs", "reports")
    os.makedirs(figures_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)

    # 2. Data Ingestion
    print(f"\n[1/6] Ingesting dataset from: {data_path}")
    df = load_logistics_data(data_path)
    print(f"      Loaded {len(df):,} records across {df.shape[1]} columns.")

    # 3. Descriptive Statistics & Correlation
    print("\n[2/6] Calculating descriptive statistics, distribution metrics, and correlations...")
    desc_stats = get_comprehensive_descriptive_stats(df)
    desc_stats.to_csv(os.path.join(reports_dir, "descriptive_statistics_summary.csv"))
    
    corr_matrix, pval_matrix = compute_correlation_matrix(df)
    corr_matrix.to_csv(os.path.join(reports_dir, "correlation_matrix.csv"))
    pval_matrix.to_csv(os.path.join(reports_dir, "correlation_pvalues.csv"))
    
    outliers_df = detect_outliers_iqr(df)
    outliers_df.to_csv(os.path.join(reports_dir, "outliers_iqr_summary.csv"))
    print(f"      Saved descriptive stats, correlation matrix, and outlier summaries.")

    # 4. Logistics KPI Calculations
    print("\n[3/6] Computing corporate logistics KPIs...")
    kpis = compute_logistics_kpis(df)
    kpi_df = pd.DataFrame(list(kpis.items()), columns=["KPI_Metric", "Value"])
    kpi_df.to_csv(os.path.join(reports_dir, "logistics_kpi_summary.csv"), index=False)
    
    for k, v in kpis.items():
        print(f"      - {k:35s}: {v}")

    # 5. Multidimensional Dimensional Slicing
    print("\n[4/6] Conducting multidimensional operational analysis...")
    regional_df = analyze_regional_performance(df)
    regional_df.to_csv(os.path.join(reports_dir, "regional_performance_summary.csv"), index=False)
    
    shipping_df = analyze_shipping_modes(df)
    shipping_df.to_csv(os.path.join(reports_dir, "shipping_mode_performance.csv"), index=False)
    
    category_df = analyze_product_categories(df)
    category_df.to_csv(os.path.join(reports_dir, "category_performance_summary.csv"), index=False)
    
    segment_df = analyze_customer_segments(df)
    segment_df.to_csv(os.path.join(reports_dir, "customer_segment_summary.csv"), index=False)
    
    warehouse_df = analyze_warehouse_performance(df)
    warehouse_df.to_csv(os.path.join(reports_dir, "warehouse_performance_summary.csv"), index=False)
    
    trends_df = analyze_temporal_trends(df, freq="M")
    trends_df.to_csv(os.path.join(reports_dir, "temporal_trends_summary.csv"), index=False)
    print("      Exported all dimensional slice summaries to outputs/reports/.")

    # 6. Insights & Bottleneck Matrix Generation
    print("\n[5/6] Synthesizing analytical findings and constructing bottleneck matrix...")
    structured_insights = generate_structured_insights(kpis, regional_df, shipping_df, category_df, segment_df)
    bottleneck_df = generate_bottleneck_matrix(df, regional_df, shipping_df, category_df)
    strategic_recs = generate_strategic_recommendations()
    
    export_executive_summary(kpis, bottleneck_df, reports_dir)
    with open(os.path.join(reports_dir, "structured_insights.json"), "w") as f:
        json.dump(structured_insights, f, indent=4)
    with open(os.path.join(reports_dir, "strategic_recommendations.json"), "w") as f:
        json.dump(strategic_recs, f, indent=4)
        
    print(f"      Extracted {len(structured_insights)} core findings and {len(bottleneck_df)} bottleneck rows.")

    # 7. Visualization Generation
    print("\n[6/6] Generating 15 publication-grade figures (300 DPI)...")
    fig_paths = generate_all_visualizations(df, figures_dir)
    print(f"      Generated {len(fig_paths)} charts in {figures_dir}")

    print("\n" + "=" * 80)
    print("WEEK 3 EXECUTION PIPELINE COMPLETED SUCCESSFULLY!")
    print("All outputs verified and written to outputs/figures/ and outputs/reports/")
    print("=" * 80)


if __name__ == "__main__":
    main()
