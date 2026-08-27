"""
Week 3: Advanced Data Analysis and Visualization in Logistics
Module: visualization.py
Author: Senior Logistics Visualization Specialist
Description:
    Implements publication-grade, aesthetic visualization functions for logistics analytics.
    Follows corporate design standards: harmonious color palettes, clear typography,
    dynamic annotations (means, medians, thresholds), and high-resolution output (300 DPI).
"""

from typing import Optional, List, Tuple
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Curated Professional Color Palette
PALETTE_PRIMARY = ["#1E3A8A", "#0D9488", "#F59E0B", "#EF4444", "#6366F1", "#10B981", "#8B5CF6", "#EC4899"]
COLOR_NAVY = "#1E3A8A"
COLOR_TEAL = "#0D9488"
COLOR_AMBER = "#F59E0B"
COLOR_RED = "#EF4444"
COLOR_INDIGO = "#6366F1"
COLOR_SLATE_DARK = "#0F172A"
COLOR_SLATE_LIGHT = "#F8FAFC"
COLOR_GRID = "#E2E8F0"


def set_visual_style():
    """
    Applies a clean, modern aesthetic to all matplotlib and seaborn plots.
    """
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Helvetica Neue", "Arial"],
        "figure.titlesize": 16,
        "figure.titleweight": "bold",
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.titlecolor": COLOR_SLATE_DARK,
        "axes.labelsize": 11,
        "axes.labelweight": "semibold",
        "axes.labelcolor": "#334155",
        "axes.edgecolor": "#94A3B8",
        "axes.linewidth": 1.0,
        "axes.grid": True,
        "grid.color": COLOR_GRID,
        "grid.linestyle": "--",
        "grid.linewidth": 0.7,
        "grid.alpha": 0.8,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "xtick.color": "#475569",
        "ytick.color": "#475569",
        "legend.fontsize": 10,
        "legend.title_fontsize": 11,
        "legend.frameon": True,
        "legend.facecolor": "#FFFFFF",
        "legend.edgecolor": "#CBD5E1",
        "figure.facecolor": "#FFFFFF",
        "axes.facecolor": "#FFFFFF",
        "savefig.dpi": 300,
        "savefig.bbox": "tight"
    })
    sns.set_palette(PALETTE_PRIMARY)


def _get_output_path(filename: str, output_dir: Optional[str] = None) -> str:
    """Helper to resolve destination path for generated figures."""
    if output_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_dir = os.path.join(base_dir, "outputs", "figures")
    os.makedirs(output_dir, exist_ok=True)
    return os.path.join(output_dir, filename)


# ==========================================
# 1. Delivery Time Distribution
# ==========================================
def plot_delivery_time_distribution(df: pd.DataFrame, output_dir: Optional[str] = None) -> str:
    set_visual_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    series = df["Delivery_Time_Days"].dropna()
    mean_val = series.mean()
    median_val = series.median()
    
    sns.histplot(series, kde=True, color=COLOR_TEAL, stat="density", bins=25, alpha=0.6, ax=ax, edgecolor="#FFFFFF")
    
    # Statistical annotations
    ax.axvline(mean_val, color=COLOR_RED, linestyle="--", linewidth=2, label=f"Mean: {mean_val:.2f} Days")
    ax.axvline(median_val, color=COLOR_NAVY, linestyle="-.", linewidth=2, label=f"Median: {median_val:.2f} Days")
    
    ax.set_title("Distribution of Delivery Time (Days) Across All Shipments", pad=15)
    ax.set_xlabel("Delivery Time (Days)")
    ax.set_ylabel("Probability Density")
    ax.legend(loc="upper right")
    
    # Text box with key metrics
    textstr = f"N = {len(series):,}\nStd Dev = {series.std():.2f} d\nSkewness = {series.skew():.2f}\nIQR = {series.quantile(0.75)-series.quantile(0.25):.2f} d"
    props = dict(boxstyle="round,pad=0.5", facecolor=COLOR_SLATE_LIGHT, edgecolor="#CBD5E1", alpha=0.9)
    ax.text(0.03, 0.95, textstr, transform=ax.transAxes, fontsize=10, verticalalignment="top", bbox=props)
    
    out_path = _get_output_path("01_delivery_time_distribution.png", output_dir)
    plt.savefig(out_path)
    plt.close()
    return out_path


# ==========================================
# 2. Shipping Cost Distribution
# ==========================================
def plot_shipping_cost_distribution(df: pd.DataFrame, output_dir: Optional[str] = None) -> str:
    set_visual_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    series = df["Shipping_Cost_USD"].dropna()
    mean_val = series.mean()
    median_val = series.median()
    
    sns.histplot(series, kde=True, color=COLOR_NAVY, stat="density", bins=30, alpha=0.6, ax=ax, edgecolor="#FFFFFF")
    
    ax.axvline(mean_val, color=COLOR_RED, linestyle="--", linewidth=2, label=f"Mean: ${mean_val:.2f}")
    ax.axvline(median_val, color=COLOR_AMBER, linestyle="-.", linewidth=2, label=f"Median: ${median_val:.2f}")
    
    ax.set_title("Distribution of Transportation & Shipping Cost (USD)", pad=15)
    ax.set_xlabel("Shipping Cost ($ USD)")
    ax.set_ylabel("Probability Density")
    ax.legend(loc="upper right")
    
    textstr = f"N = {len(series):,}\nMin = ${series.min():.2f}\nMax = ${series.max():.2f}\nStd Dev = ${series.std():.2f}\nSkewness = {series.skew():.2f}"
    props = dict(boxstyle="round,pad=0.5", facecolor=COLOR_SLATE_LIGHT, edgecolor="#CBD5E1", alpha=0.9)
    ax.text(0.03, 0.95, textstr, transform=ax.transAxes, fontsize=10, verticalalignment="top", bbox=props)
    
    out_path = _get_output_path("02_shipping_cost_distribution.png", output_dir)
    plt.savefig(out_path)
    plt.close()
    return out_path


# ==========================================
# 3. Shipment Volume by Region
# ==========================================
def plot_shipment_volume_by_region(df: pd.DataFrame, output_dir: Optional[str] = None) -> str:
    set_visual_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    counts = df["Region"].value_counts().reset_index()
    counts.columns = ["Region", "Order_Count"]
    total = counts["Order_Count"].sum()
    counts["Share"] = (counts["Order_Count"] / total * 100.0)
    
    bars = ax.bar(counts["Region"], counts["Order_Count"], color=PALETTE_PRIMARY[:len(counts)], width=0.6, edgecolor="#334155", linewidth=0.8)
    
    # Add count and percentage labels
    for bar, (_, row) in zip(bars, counts.iterrows()):
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 10, f"{int(row['Order_Count']):,}\n({row['Share']:.1f}%)", 
                ha="center", va="bottom", fontsize=10, fontweight="bold", color="#1E293B")
        
    ax.set_title("Total Shipment Order Volume by Geographic Destination Region", pad=15)
    ax.set_xlabel("Destination Region")
    ax.set_ylabel("Total Number of Orders")
    ax.set_ylim(0, counts["Order_Count"].max() * 1.18)
    
    out_path = _get_output_path("03_shipment_volume_by_region.png", output_dir)
    plt.savefig(out_path)
    plt.close()
    return out_path


# ==========================================
# 4. Average Delivery Time by Region & Warehouse
# ==========================================
def plot_avg_delivery_time_by_region_warehouse(df: pd.DataFrame, output_dir: Optional[str] = None) -> str:
    set_visual_style()
    fig, ax = plt.subplots(figsize=(12, 6))
    
    pivot = df.groupby(["Region", "Warehouse_Code"])["Delivery_Time_Days"].mean().reset_index()
    
    sns.barplot(data=pivot, x="Region", y="Delivery_Time_Days", hue="Warehouse_Code", palette="Set2", ax=ax, edgecolor="#475569")
    
    # Overall benchmark line
    overall_mean = df["Delivery_Time_Days"].mean()
    ax.axhline(overall_mean, color=COLOR_RED, linestyle="--", linewidth=1.5, label=f"Global Mean ({overall_mean:.2f} d)")
    
    ax.set_title("Average Delivery Latency (Days) by Destination Region and Origin Warehouse", pad=15)
    ax.set_xlabel("Destination Region")
    ax.set_ylabel("Average Delivery Time (Days)")
    ax.legend(title="Origin Warehouse", bbox_to_anchor=(1.02, 1), loc="upper left")
    
    out_path = _get_output_path("04_avg_delivery_time_by_region_warehouse.png", output_dir)
    plt.savefig(out_path)
    plt.close()
    return out_path


# ==========================================
# 5. Shipping Cost by Shipping Mode
# ==========================================
def plot_shipping_cost_by_mode(df: pd.DataFrame, output_dir: Optional[str] = None) -> str:
    set_visual_style()
    fig, ax = plt.subplots(figsize=(11, 6))
    
    # Order shipping modes logically
    mode_order = ["Same-Day Courier", "Express Air", "Ground Freight", "Standard Delivery"]
    actual_modes = [m for m in mode_order if m in df["Shipping_Mode"].unique()]
    
    sns.boxplot(data=df, x="Shipping_Mode", y="Shipping_Cost_USD", hue="Shipping_Mode", order=actual_modes, palette="crest", ax=ax, width=0.5, fliersize=3, legend=False)
    
    # Annotate median values
    medians = df.groupby("Shipping_Mode")["Shipping_Cost_USD"].median()
    means = df.groupby("Shipping_Mode")["Shipping_Cost_USD"].mean()
    
    for i, mode in enumerate(actual_modes):
        if mode in medians:
            med = medians[mode]
            avg = means[mode]
            ax.text(i, med + 3, f"Med: ${med:.1f}\nAvg: ${avg:.1f}", ha="center", va="bottom", fontsize=9, fontweight="bold", color="#0F172A",
                    bbox=dict(boxstyle="square,pad=0.2", facecolor="#FFFFFF", edgecolor="#94A3B8", alpha=0.8))
            
    ax.set_title("Transportation Spend Distribution Across Shipping Modes", pad=15)
    ax.set_xlabel("Shipping Mode Service Tier")
    ax.set_ylabel("Shipping Cost ($ USD)")
    
    out_path = _get_output_path("05_shipping_cost_by_mode.png", output_dir)
    plt.savefig(out_path)
    plt.close()
    return out_path


# ==========================================
# 6. Delivery Time by Shipping Mode
# ==========================================
def plot_delivery_time_by_mode(df: pd.DataFrame, output_dir: Optional[str] = None) -> str:
    set_visual_style()
    fig, ax = plt.subplots(figsize=(11, 6))
    
    mode_order = ["Same-Day Courier", "Express Air", "Ground Freight", "Standard Delivery"]
    actual_modes = [m for m in mode_order if m in df["Shipping_Mode"].unique()]
    
    sns.boxplot(data=df, x="Shipping_Mode", y="Delivery_Time_Days", hue="Shipping_Mode", order=actual_modes, palette="viridis", ax=ax, width=0.5, fliersize=3, legend=False)
    
    # Estimated SLA targets
    sla_map = {"Same-Day Courier": 1.0, "Express Air": 2.0, "Standard Delivery": 5.0, "Ground Freight": 7.0}
    
    for i, mode in enumerate(actual_modes):
        if mode in sla_map:
            sla = sla_map[mode]
            ax.scatter(i, sla, color=COLOR_RED, s=80, zorder=5, marker="D", label="Contractual SLA" if i == 0 else "")
            
    ax.set_title("Actual Delivery Time vs Contractual SLA Benchmarks by Shipping Mode", pad=15)
    ax.set_xlabel("Shipping Mode")
    ax.set_ylabel("Delivery Time (Days)")
    ax.legend(loc="upper left")
    
    out_path = _get_output_path("06_delivery_time_by_mode.png", output_dir)
    plt.savefig(out_path)
    plt.close()
    return out_path


# ==========================================
# 7. Distance vs Delivery Time
# ==========================================
def plot_distance_vs_delivery_time(df: pd.DataFrame, output_dir: Optional[str] = None) -> str:
    set_visual_style()
    fig, ax = plt.subplots(figsize=(11, 6))
    
    sns.scatterplot(data=df, x="Distance_KM", y="Delivery_Time_Days", hue="Shipping_Mode", palette="tab10", alpha=0.7, s=40, ax=ax)
    
    # Overall linear trend
    slope, intercept, r_value, p_value, _ = stats.linregress(df["Distance_KM"].dropna(), df["Delivery_Time_Days"].dropna())
    x_vals = np.linspace(df["Distance_KM"].min(), df["Distance_KM"].max(), 100)
    ax.plot(x_vals, intercept + slope * x_vals, color=COLOR_RED, linestyle="--", linewidth=2, label=f"Trendline (r = {r_value:.2f}, p < 0.001)")
    
    ax.set_title("Relationship Between Transit Distance (KM) and Delivery Latency (Days)", pad=15)
    ax.set_xlabel("Transportation Distance (KM)")
    ax.set_ylabel("Delivery Time (Days)")
    ax.legend(title="Shipping Mode", bbox_to_anchor=(1.02, 1), loc="upper left")
    
    out_path = _get_output_path("07_distance_vs_delivery_time.png", output_dir)
    plt.savefig(out_path)
    plt.close()
    return out_path


# ==========================================
# 8. Distance vs Shipping Cost
# ==========================================
def plot_distance_vs_shipping_cost(df: pd.DataFrame, output_dir: Optional[str] = None) -> str:
    set_visual_style()
    fig, ax = plt.subplots(figsize=(11, 6))
    
    sns.scatterplot(data=df, x="Distance_KM", y="Shipping_Cost_USD", hue="Shipping_Mode", palette="Set1", alpha=0.7, s=40, ax=ax)
    
    # Regression fit
    slope, intercept, r_value, p_value, _ = stats.linregress(df["Distance_KM"].dropna(), df["Shipping_Cost_USD"].dropna())
    x_vals = np.linspace(df["Distance_KM"].min(), df["Distance_KM"].max(), 100)
    ax.plot(x_vals, intercept + slope * x_vals, color=COLOR_SLATE_DARK, linestyle="-", linewidth=2.2, 
            label=f"Linear Fit (Slope = ${slope:.3f}/KM, R² = {r_value**2:.2f})")
    
    ax.set_title("Impact of Transit Distance on Transportation Shipping Cost", pad=15)
    ax.set_xlabel("Transportation Distance (KM)")
    ax.set_ylabel("Shipping Cost ($ USD)")
    ax.legend(title="Shipping Mode", bbox_to_anchor=(1.02, 1), loc="upper left")
    
    out_path = _get_output_path("08_distance_vs_shipping_cost.png", output_dir)
    plt.savefig(out_path)
    plt.close()
    return out_path


# ==========================================
# 9. Correlation Heatmap
# ==========================================
def plot_correlation_heatmap(df: pd.DataFrame, output_dir: Optional[str] = None) -> str:
    set_visual_style()
    fig, ax = plt.subplots(figsize=(11, 9))
    
    # Select primary business metrics
    cols = [
        "Quantity", "Sales_USD", "Shipping_Cost_USD", "Delivery_Time_Days", 
        "Estimated_Delivery_Days", "Distance_KM", "Order_Processing_Days", 
        "Customer_Rating", "Cost_Per_Unit", "Cost_Per_KM", "Speed_Index_KMPD"
    ]
    actual_cols = [c for c in cols if c in df.columns]
    corr = df[actual_cols].corr()
    
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="vlag", vmin=-1.0, vmax=1.0, 
                center=0, square=True, linewidths=0.5, cbar_kws={"shrink": 0.8, "label": "Pearson Correlation (r)"}, ax=ax)
    
    ax.set_title("Correlation Heatmap of Key Numerical Logistics Variables", pad=20)
    
    out_path = _get_output_path("09_correlation_heatmap.png", output_dir)
    plt.savefig(out_path)
    plt.close()
    return out_path


# ==========================================
# 10. Monthly Order Volume and Cost Trend
# ==========================================
def plot_monthly_order_volume_cost_trend(df: pd.DataFrame, output_dir: Optional[str] = None) -> str:
    set_visual_style()
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    df_temp = df.copy()
    df_temp["Month_Str"] = df_temp["Order_Date"].dt.strftime("%Y-%m")
    
    monthly = df_temp.groupby("Month_Str").agg(
        Order_Volume=("Order_ID", "count"),
        Total_Shipping_Cost=("Shipping_Cost_USD", "sum")
    ).reset_index().sort_values("Month_Str")
    
    x = np.arange(len(monthly))
    width = 0.4
    
    # Volume bars on primary axis
    ax1.bar(x, monthly["Order_Volume"], width=width, color=COLOR_NAVY, alpha=0.8, label="Order Volume (Shipments)", edgecolor="#334155")
    ax1.set_xlabel("Order Month")
    ax1.set_ylabel("Order Volume (Shipments)", color=COLOR_NAVY)
    ax1.tick_params(axis="y", labelcolor=COLOR_NAVY)
    ax1.set_xticks(x)
    ax1.set_xticklabels(monthly["Month_Str"], rotation=0)
    ax1.grid(False)
    
    # Cost line on secondary axis
    ax2 = ax1.twinx()
    ax2.plot(x, monthly["Total_Shipping_Cost"], color=COLOR_RED, marker="o", linewidth=2.5, markersize=8, label="Total Shipping Spend ($ USD)")
    ax2.set_ylabel("Total Shipping Cost ($ USD)", color=COLOR_RED)
    ax2.tick_params(axis="y", labelcolor=COLOR_RED)
    ax2.grid(True, linestyle=":", alpha=0.5)
    
    # Format labels
    for i, (_, row) in enumerate(monthly.iterrows()):
        ax1.text(i, row["Order_Volume"] / 2, f"{int(row['Order_Volume'])}", ha="center", va="center", color="#FFFFFF", fontweight="bold")
        ax2.text(i, row["Total_Shipping_Cost"] + 500, f"${row['Total_Shipping_Cost']:,.0f}", ha="center", va="bottom", color=COLOR_RED, fontweight="bold", fontsize=9)
        
    plt.title("Monthly Shipment Volume and Transportation Expenditure Dynamics (2024)", pad=15)
    
    out_path = _get_output_path("10_monthly_order_volume_cost_trend.png", output_dir)
    plt.savefig(out_path)
    plt.close()
    return out_path


# ==========================================
# 11. Quantity vs Shipping Cost
# ==========================================
def plot_quantity_vs_shipping_cost(df: pd.DataFrame, output_dir: Optional[str] = None) -> str:
    set_visual_style()
    fig, ax = plt.subplots(figsize=(11, 6))
    
    sns.scatterplot(data=df, x="Quantity", y="Shipping_Cost_USD", hue="Product_Category", palette="Dark2", alpha=0.75, s=50, ax=ax)
    
    ax.set_title("Shipment Order Quantity vs Shipping Cost by Product Category", pad=15)
    ax.set_xlabel("Order Item Quantity")
    ax.set_ylabel("Shipping Cost ($ USD)")
    ax.legend(title="Product Category", bbox_to_anchor=(1.02, 1), loc="upper left")
    
    out_path = _get_output_path("11_quantity_vs_shipping_cost.png", output_dir)
    plt.savefig(out_path)
    plt.close()
    return out_path


# ==========================================
# 12. Product Category Performance
# ==========================================
def plot_product_category_performance(df: pd.DataFrame, output_dir: Optional[str] = None) -> str:
    set_visual_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    cat_summary = df.groupby("Product_Category").agg(
        Total_Sales=("Sales_USD", "sum"),
        Total_Cost=("Shipping_Cost_USD", "sum")
    ).reset_index()
    cat_summary["Cost_Ratio"] = (cat_summary["Total_Cost"] / cat_summary["Total_Sales"] * 100.0)
    
    # Plot 1: Sales vs Cost
    x = np.arange(len(cat_summary))
    w = 0.35
    ax1.bar(x - w/2, cat_summary["Total_Sales"] / 1000, w, label="Total Sales ($k)", color=COLOR_NAVY, edgecolor="#334155")
    ax1.bar(x + w/2, cat_summary["Total_Cost"] / 1000, w, label="Total Shipping Cost ($k)", color=COLOR_AMBER, edgecolor="#334155")
    ax1.set_xticks(x)
    ax1.set_xticklabels(cat_summary["Product_Category"], rotation=20, ha="right")
    ax1.set_ylabel("Amount ($ in Thousands)")
    ax1.set_title("Total Sales vs Shipping Expenditure")
    ax1.legend()
    
    # Plot 2: Cost Ratio (%)
    bars = ax2.bar(cat_summary["Product_Category"], cat_summary["Cost_Ratio"], color=COLOR_TEAL, width=0.5, edgecolor="#334155")
    for bar in bars:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 0.5, f"{yval:.1f}%", ha="center", va="bottom", fontweight="bold")
    ax2.set_xticks(np.arange(len(cat_summary)))
    ax2.set_xticklabels(cat_summary["Product_Category"], rotation=20, ha="right")
    ax2.set_ylabel("Shipping Cost as % of Sales")
    ax2.set_title("Logistics Cost Burden Ratio by Product Category")
    ax2.set_ylim(0, cat_summary["Cost_Ratio"].max() * 1.25)
    
    plt.suptitle("Logistics and Revenue Performance by Product Category", fontsize=15, fontweight="bold", y=1.02)
    
    out_path = _get_output_path("12_product_category_performance.png", output_dir)
    plt.savefig(out_path)
    plt.close()
    return out_path


# ==========================================
# 13. Delivery Status and Delay Rate by Mode
# ==========================================
def plot_delivery_status_delay_rate_by_mode(df: pd.DataFrame, output_dir: Optional[str] = None) -> str:
    set_visual_style()
    fig, ax = plt.subplots(figsize=(11, 6))
    
    pivot = pd.crosstab(df["Shipping_Mode"], df["Is_Delayed"], normalize="index") * 100.0
    pivot.columns = ["On-Time (%)", "Delayed (%)"]
    
    pivot.plot(kind="bar", stacked=True, color=[COLOR_TEAL, COLOR_RED], ax=ax, width=0.55, edgecolor="#334155")
    
    # Add percentage labels
    for n, c in enumerate(pivot.columns):
        for i, val in enumerate(pivot[c]):
            if val > 5:
                y_pos = pivot.iloc[i, :n].sum() + val / 2.0
                ax.text(i, y_pos, f"{val:.1f}%", ha="center", va="center", color="#FFFFFF", fontweight="bold", fontsize=10)
                
    ax.set_title("On-Time vs Delayed Delivery Proportions Across Shipping Service Tiers", pad=15)
    ax.set_xlabel("Shipping Mode")
    ax.set_ylabel("Percentage of Shipments (%)")
    ax.set_xticks(range(len(pivot)))
    ax.set_xticklabels(pivot.index, rotation=0)
    ax.set_ylim(0, 100)
    ax.legend(title="Delivery Fulfillment Status", loc="upper right")
    
    out_path = _get_output_path("13_delivery_status_delay_rate_by_mode.png", output_dir)
    plt.savefig(out_path)
    plt.close()
    return out_path


# ==========================================
# 14. Customer Segment Comparison
# ==========================================
def plot_customer_segment_comparison(df: pd.DataFrame, output_dir: Optional[str] = None) -> str:
    set_visual_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    seg = df.groupby("Customer_Segment").agg(
        AOV=("Sales_USD", "mean"),
        Avg_Rating=("Customer_Rating", "mean"),
        Delay_Rate=("Is_Delayed", lambda s: (s == 1).mean() * 100.0)
    ).reset_index()
    
    # Plot 1: AOV by Segment
    bars1 = ax1.bar(seg["Customer_Segment"], seg["AOV"], color=COLOR_NAVY, width=0.5, edgecolor="#334155")
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 10, f"${yval:.0f}", ha="center", va="bottom", fontweight="bold")
    ax1.set_title("Average Order Value (AOV) by Segment")
    ax1.set_ylabel("Average Order Value ($ USD)")
    ax1.set_xticks(np.arange(len(seg)))
    ax1.set_xticklabels(seg["Customer_Segment"], rotation=15, ha="right")
    
    # Plot 2: Rating vs Delay Rate
    x = np.arange(len(seg))
    w = 0.35
    ax2.bar(x - w/2, seg["Avg_Rating"], w, label="Avg Rating (1-5)", color=COLOR_AMBER, edgecolor="#334155")
    ax2_twin = ax2.twinx()
    ax2_twin.plot(x + w/2, seg["Delay_Rate"], color=COLOR_RED, marker="s", linewidth=2.5, markersize=8, label="Delay Rate (%)")
    ax2.set_xticks(x)
    ax2.set_xticklabels(seg["Customer_Segment"], rotation=15, ha="right")
    ax2.set_ylabel("Customer Satisfaction Rating (1-5)")
    ax2_twin.set_ylabel("Delay Rate (%)", color=COLOR_RED)
    ax2.set_title("Customer Rating & Delay Rate Dynamics")
    ax2.grid(False)
    
    plt.suptitle("Multidimensional Logistics Comparison Across Customer Segments", fontsize=15, fontweight="bold", y=1.02)
    
    out_path = _get_output_path("14_customer_segment_comparison.png", output_dir)
    plt.savefig(out_path)
    plt.close()
    return out_path


# ==========================================
# 15. Multivariate Delay Risk Matrix Heatmap
# ==========================================
def plot_multivariate_delay_risk_matrix(df: pd.DataFrame, output_dir: Optional[str] = None) -> str:
    set_visual_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    risk_pivot = df.pivot_table(
        index="Region", 
        columns="Shipping_Mode", 
        values="Is_Delayed", 
        aggfunc=lambda s: (s == 1).mean() * 100.0
    )
    
    sns.heatmap(risk_pivot, annot=True, fmt=".1f", cmap="YlOrRd", cbar_kws={"label": "Delay Rate (% of Shipments)"}, 
                linewidths=1.0, linecolor="#CBD5E1", ax=ax)
    
    ax.set_title("Multivariate Operational Risk Matrix: Delay Rate (%) by Region & Shipping Mode", pad=15)
    ax.set_xlabel("Shipping Mode Service Tier")
    ax.set_ylabel("Geographic Region")
    
    out_path = _get_output_path("15_multivariate_delay_risk_matrix.png", output_dir)
    plt.savefig(out_path)
    plt.close()
    return out_path


def generate_all_visualizations(df: pd.DataFrame, output_dir: Optional[str] = None) -> List[str]:
    """
    Executes all 15 visualization routines sequentially and returns list of saved file paths.
    """
    print(">>> Generating comprehensive publication-grade visualizations...")
    generated_files = [
        plot_delivery_time_distribution(df, output_dir),
        plot_shipping_cost_distribution(df, output_dir),
        plot_shipment_volume_by_region(df, output_dir),
        plot_avg_delivery_time_by_region_warehouse(df, output_dir),
        plot_shipping_cost_by_mode(df, output_dir),
        plot_delivery_time_by_mode(df, output_dir),
        plot_distance_vs_delivery_time(df, output_dir),
        plot_distance_vs_shipping_cost(df, output_dir),
        plot_correlation_heatmap(df, output_dir),
        plot_monthly_order_volume_cost_trend(df, output_dir),
        plot_quantity_vs_shipping_cost(df, output_dir),
        plot_product_category_performance(df, output_dir),
        plot_delivery_status_delay_rate_by_mode(df, output_dir),
        plot_customer_segment_comparison(df, output_dir),
        plot_multivariate_delay_risk_matrix(df, output_dir)
    ]
    print(f">>> Successfully generated {len(generated_files)} visualizations in outputs/figures/")
    return generated_files
