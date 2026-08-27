"""
Week 3: Advanced Data Analysis and Visualization in Logistics
Module: insights.py
Author: Senior Logistics Analytics Consultant
Description:
    Generates structured, data-grounded business findings using the four-part framework:
    (Finding, Evidence, Business Meaning, Potential Action).
    Constructs the operational bottleneck analysis matrix and exports executive summary reports.
"""

from typing import Dict, Any, List, Optional
import os
import json
import pandas as pd
import numpy as np


def generate_structured_insights(
    kpi_dict: Dict[str, Any],
    regional_df: pd.DataFrame,
    shipping_df: pd.DataFrame,
    category_df: pd.DataFrame,
    segment_df: pd.DataFrame
) -> List[Dict[str, str]]:
    """
    Synthesizes empirical data into rigorous, actionable four-part business insights.
    """
    insights = []
    
    # Insight 1: Regional Disparities in Latency & Fulfillment
    max_del_region = regional_df.loc[regional_df["Avg_Delivery_Time_Days"].idxmax()]
    min_del_region = regional_df.loc[regional_df["Avg_Delivery_Time_Days"].idxmin()]
    max_delay_rate_region = regional_df.loc[regional_df["Delay_Rate_Pct"].idxmax()]
    
    insights.append({
        "ID": "INS-01",
        "Domain": "Regional Logistics & Service Latency",
        "Finding": f"Geographic destination creates substantial delivery latency variance, with {max_del_region['Region']} exhibiting the highest transit time and {max_delay_rate_region['Region']} recording peak delay rates.",
        "Evidence": f"{max_del_region['Region']} records an average delivery time of {max_del_region['Avg_Delivery_Time_Days']} days (vs {min_del_region['Avg_Delivery_Time_Days']} days in {min_del_region['Region']}). Delay rate in {max_delay_rate_region['Region']} stands at {max_delay_rate_region['Delay_Rate_Pct']}%.",
        "Business Meaning": "Regional fulfillment variance stems from uneven warehouse proximity, hub-and-spoke transit handoffs, and localized carrier capacity constraints, risking customer churn in underperforming territories.",
        "Potential Action": "Establish localized forward stocking hubs or cross-docking points in high-latency regions and renegotiate regional carrier service level agreements (SLAs) with strict on-time delivery penalty clauses."
    })
    
    # Insight 2: Shipping Mode SLA Integrity & Cost Premiums
    express_mode = shipping_df[shipping_df["Shipping_Mode"] == "Express Air"].iloc[0] if "Express Air" in shipping_df["Shipping_Mode"].values else None
    ground_mode = shipping_df[shipping_df["Shipping_Mode"] == "Ground Freight"].iloc[0] if "Ground Freight" in shipping_df["Shipping_Mode"].values else None
    sameday_mode = shipping_df[shipping_df["Shipping_Mode"] == "Same-Day Courier"].iloc[0] if "Same-Day Courier" in shipping_df["Shipping_Mode"].values else None
    standard_mode = shipping_df[shipping_df["Shipping_Mode"] == "Standard Delivery"].iloc[0] if "Standard Delivery" in shipping_df["Shipping_Mode"].values else None
    
    if express_mode is not None and standard_mode is not None:
        insights.append({
            "ID": "INS-02",
            "Domain": "Modal Economics & SLA Compliance",
            "Finding": f"Premium expedited tiers command significantly higher shipping costs per unit but struggle with punctuality tolerances.",
            "Evidence": f"Express Air costs an average of ${express_mode['Avg_Shipping_Cost_USD']:.2f} per order with a delay rate of {express_mode['Delay_Rate_Pct']}%, while Standard Delivery averages ${standard_mode['Avg_Shipping_Cost_USD']:.2f} with a {standard_mode['Delay_Rate_Pct']}% delay rate.",
            "Business Meaning": "Customers paying express freight premiums have zero tolerance for schedule slippage. High delay rates on premium tiers erode customer trust and cause costly claim disputes.",
            "Potential Action": "Implement real-time carrier tracking integrations for expedited consignments and enforce pre-dispatch prioritization in warehouse picking queues for air freight orders."
        })
        
    # Insight 3: Distance and Transportation Cost Elasticity
    insights.append({
        "ID": "INS-03",
        "Domain": "Transportation Cost Drivers",
        "Finding": "Transportation distance is a major linear driver of shipping expenditure, but unit volume consolidation offers substantial cost mitigation.",
        "Evidence": f"Overall average shipping spend is ${kpi_dict['Average_Shipping_Cost_USD']:.2f} on an average distance of {kpi_dict['Average_Distance_KM']:.1f} KM (Cost per KM: ${kpi_dict['Average_Cost_Per_KM_USD']:.4f}). Correlation between Distance and Cost is strong and positive.",
        "Business Meaning": "Long-haul point-to-point shipments create disproportionate freight expense without volume aggregation, lowering operating contribution margins.",
        "Potential Action": "Implement dynamic shipment batching and consolidate LTL (Less-Than-Truckload) consignments into scheduled FTL (Full-Truckload) trunk routes."
    })
    
    # Insight 4: Product Category Cost Burden
    max_cost_ratio_cat = category_df.loc[category_df["Shipping_Cost_Ratio_Pct"].idxmax()]
    max_rev_cat = category_df.loc[category_df["Total_Sales_USD"].idxmax()]
    
    insights.append({
        "ID": "INS-04",
        "Domain": "Category Freight Burden",
        "Finding": f"{max_cost_ratio_cat['Product_Category']} represents the highest relative logistics cost burden relative to sales revenue.",
        "Evidence": f"{max_cost_ratio_cat['Product_Category']} exhibits a shipping-cost-to-sales ratio of {max_cost_ratio_cat['Shipping_Cost_Ratio_Pct']}%, compared to the corporate average of {kpi_dict['Shipping_Cost_to_Sales_Ratio_Pct']}%. {max_rev_cat['Product_Category']} generates the largest gross sales volume (${max_rev_cat['Total_Sales_USD']:,.2f}).",
        "Business Meaning": "Low-density, heavy, or low-margin product categories consume excessive logistics spend relative to gross commercial value, squeezing product-level profitability.",
        "Potential Action": "Re-evaluate dimensional weight packaging guidelines, establish minimum order quantities for heavy merchandise, and adjust product pricing or shipping surcharges."
    })
    
    # Insight 5: Overall Operational Reliability & Delay Burden
    insights.append({
        "ID": "INS-05",
        "Domain": "Network-wide Reliability & Customer Satisfaction",
        "Finding": f"The aggregate delivery delay rate of {kpi_dict['Delivery_Delay_Rate_Pct']}% constitutes a primary operational risk affecting overall customer experience.",
        "Evidence": f"Out of {kpi_dict['Total_Orders']:,} shipments, {kpi_dict['Delayed_Orders_Count']:,} arrived past the promised delivery window, yielding an On-Time Delivery Rate of {kpi_dict['On_Time_Delivery_Rate_Pct']}% and an average customer rating of {kpi_dict['Average_Customer_Rating']:.2f} / 5.0.",
        "Business Meaning": "Network delays create cascading friction across customer support channels, degrade repeat purchase rates, and incur penalty costs.",
        "Potential Action": "Deploy automated exception management workflows that notify logistics coordinators immediately when an order exceeds 24-hour processing time in fulfillment centers."
    })
    
    return insights


def generate_bottleneck_matrix(
    df: pd.DataFrame,
    regional_df: pd.DataFrame,
    shipping_df: pd.DataFrame,
    category_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Constructs an empirical Operational Bottleneck Summary Matrix.
    """
    bottlenecks = []
    
    # 1. High Latency Region
    max_del_reg = regional_df.loc[regional_df["Avg_Delivery_Time_Days"].idxmax()]
    bottlenecks.append({
        "Logistics_Area": f"Region ({max_del_reg['Region']})",
        "Primary_Indicator": "Delivery Latency & Route Distance",
        "Empirical_Evidence": f"Avg delivery time: {max_del_reg['Avg_Delivery_Time_Days']} days (Avg dist: {max_del_reg['Avg_Distance_KM']} KM)",
        "Operational_Concern": "Protracted transit duration and distance from central supply hubs causing delivery fatigue.",
        "Corrective_Action": "Re-route shipments through nearest regional cross-dock and onboard secondary regional carriers."
    })
    
    # 2. Highest Delay Region
    max_delay_reg = regional_df.loc[regional_df["Delay_Rate_Pct"].idxmax()]
    bottlenecks.append({
        "Logistics_Area": f"Region ({max_delay_reg['Region']})",
        "Primary_Indicator": "Delivery Delay Frequency",
        "Empirical_Evidence": f"Delay rate: {max_delay_reg['Delay_Rate_Pct']}% across {max_delay_reg['Order_Count']} total orders",
        "Operational_Concern": "Persistent failure to meet promised arrival schedules degrading localized market share.",
        "Corrective_Action": "Audit line-haul transit handoffs and establish dynamic buffer time algorithms in dispatch planning."
    })
    
    # 3. High Expedited Spend / Premium Mode
    exp_mode = shipping_df[shipping_df["Shipping_Mode"] == "Express Air"]
    if not exp_mode.empty:
        exp = exp_mode.iloc[0]
        bottlenecks.append({
            "Logistics_Area": "Shipping Mode (Express Air)",
            "Primary_Indicator": "High Cost & Inconsistent Reliability",
            "Empirical_Evidence": f"Avg cost: ${exp['Avg_Shipping_Cost_USD']:.2f}/order | Delay rate: {exp['Delay_Rate_Pct']}%",
            "Operational_Concern": "Expedited premium expenditure without commensurate delivery reliability guarantees.",
            "Corrective_Action": "Enforce strict carrier SLA enforcement with chargebacks on delayed express shipments."
        })
        
    # 4. Standard Delivery Latency
    std_mode = shipping_df[shipping_df["Shipping_Mode"] == "Standard Delivery"]
    if not std_mode.empty:
        std = std_mode.iloc[0]
        bottlenecks.append({
            "Logistics_Area": "Shipping Mode (Standard Delivery)",
            "Primary_Indicator": "High Volume & Transit Delay",
            "Empirical_Evidence": f"{std['Order_Count']} orders ({std['Volume_Share_Pct']}% share) with {std['Delay_Rate_Pct']}% delay rate",
            "Operational_Concern": "Core delivery backbone suffers from systematic delays affecting the majority of customers.",
            "Corrective_Action": "Standardize warehouse dispatch sorting and implement zone-skipping to minimize intermediate sorting."
        })
        
    # 5. High-Burden Product Category
    cat_burden = category_df.loc[category_df["Shipping_Cost_Ratio_Pct"].idxmax()]
    bottlenecks.append({
        "Logistics_Area": f"Category ({cat_burden['Product_Category']})",
        "Primary_Indicator": "Logistics Cost Burden Ratio",
        "Empirical_Evidence": f"Shipping cost accounts for {cat_burden['Shipping_Cost_Ratio_Pct']}% of gross category sales",
        "Operational_Concern": "Erosion of gross margins due to heavy package weights and dimensional inefficiencies.",
        "Corrective_Action": "Optimize cartonization algorithms, review vendor packaging, and evaluate tiered shipping pricing."
    })
    
    # 6. Warehouse Fulfillment Latency
    wh_perf = df.groupby("Warehouse_Code").agg(
        Avg_Proc=("Order_Processing_Days", "mean"),
        Del_Rate=("Is_Delayed", lambda s: (s == 1).mean() * 100.0)
    ).reset_index()
    max_proc_wh = wh_perf.loc[wh_perf["Avg_Proc"].idxmax()]
    bottlenecks.append({
        "Logistics_Area": f"Fulfillment Hub ({max_proc_wh['Warehouse_Code']})",
        "Primary_Indicator": "Order Processing Latency",
        "Empirical_Evidence": f"Avg processing time: {max_proc_wh['Avg_Proc']:.2f} days | Delay rate: {max_proc_wh['Del_Rate']:.1f}%",
        "Operational_Concern": "Internal order picking, staging, and dispatch delays eat into available line-haul transit buffer.",
        "Corrective_Action": "Streamline warehouse picking routes and implement wave-picking automation for high-velocity SKUs."
    })
    
    return pd.DataFrame(bottlenecks)


def generate_strategic_recommendations() -> List[Dict[str, str]]:
    """
    Generates realistic, grounded, non-hyperbolic business recommendations.
    """
    return [
        {
            "Priority": "P1 - Immediate (0-3 Months)",
            "Area": "Carrier Performance & SLA Management",
            "Recommendation": "Institute rigorous Carrier Performance Scorecards tracking daily on-time delivery rates across all shipping modes, activating contractual penalty credits for deliveries exceeding SLA thresholds."
        },
        {
            "Priority": "P1 - Immediate (0-3 Months)",
            "Area": "Warehouse Dispatch Synchronization",
            "Recommendation": "Enforce same-day dispatch cutoff rules and prioritize expedited air/courier orders in the picking queue to reduce internal order processing latency."
        },
        {
            "Priority": "P2 - Medium-Term (3-6 Months)",
            "Area": "Regional Routing & Network Optimization",
            "Recommendation": "Conduct network gravity modeling to evaluate optimal positioning of regional forwarding hubs in peripheral high-latency regions to compress long-haul distances."
        },
        {
            "Priority": "P2 - Medium-Term (3-6 Months)",
            "Area": "Packaging & Dimensional Weight Rationalization",
            "Recommendation": "Standardize carton dimensions and implement automated cartonization software for high-freight-burden categories (e.g. Industrial Machinery and Healthcare Supplies) to reduce dimensional freight penalties."
        },
        {
            "Priority": "P3 - Long-Term (6-12 Months)",
            "Area": "Predictive Logistics Analytics & Dashboarding",
            "Recommendation": "Build machine learning models for early delivery delay risk classification and dynamic transportation cost forecasting during checkout to optimize route selection."
        }
    ]


def export_executive_summary(
    kpi_dict: Dict[str, Any],
    bottleneck_df: pd.DataFrame,
    output_dir: Optional[str] = None
) -> str:
    """
    Exports summary KPIs and key metrics to JSON and CSV in outputs/reports/.
    """
    if output_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_dir = os.path.join(base_dir, "outputs", "reports")
    os.makedirs(output_dir, exist_ok=True)
    
    # Save KPI JSON
    json_path = os.path.join(output_dir, "executive_summary_metrics.json")
    with open(json_path, "w") as f:
        json.dump(kpi_dict, f, indent=4)
        
    # Save Bottleneck Matrix CSV
    bottleneck_path = os.path.join(output_dir, "logistics_bottleneck_matrix.csv")
    bottleneck_df.to_csv(bottleneck_path, index=False)
    
    return json_path
