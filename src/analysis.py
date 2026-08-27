"""
Week 3: Advanced Data Analysis and Visualization in Logistics
Module: analysis.py
Author: Senior Logistics Data Analyst
Description:
    Provides dataset ingestion, validation, core logistics KPI computations,
    and granular multidimensional operational slicing (regional, shipping modes,
    product categories, customer segments, warehouse performance, and temporal trends).
"""

from typing import Dict, Any, Optional
import os
import numpy as np
import pandas as pd


def load_logistics_data(
    filepath: Optional[str] = None
) -> pd.DataFrame:
    """
    Loads the cleaned logistics dataset, enforces datetime formats,
    and verifies essential categorical/numerical columns.
    """
    if filepath is None:
        # Default relative to project structure
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = os.path.join(base_dir, "data", "processed", "logistics_cleaned.csv")
        
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Logistics dataset not found at: {filepath}")
        
    df = pd.read_csv(filepath)
    
    # Parse date columns
    for date_col in ["Order_Date", "Shipping_Date"]:
        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
            
    # Ensure categorical columns have proper string representation
    cat_cols = ["Customer_Segment", "Product_Category", "Warehouse_Code", "Region", "Shipping_Mode", "Delivery_Status"]
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].astype(str)
            
    return df


def compute_logistics_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculates essential corporate logistics KPIs.
    """
    total_orders = len(df)
    total_sales = float(df["Sales_USD"].sum()) if "Sales_USD" in df.columns else 0.0
    total_shipping_cost = float(df["Shipping_Cost_USD"].sum()) if "Shipping_Cost_USD" in df.columns else 0.0
    
    avg_delivery_time = float(df["Delivery_Time_Days"].mean()) if "Delivery_Time_Days" in df.columns else 0.0
    median_delivery_time = float(df["Delivery_Time_Days"].median()) if "Delivery_Time_Days" in df.columns else 0.0
    
    # Delay metrics
    if "Is_Delayed" in df.columns:
        delayed_orders = int((df["Is_Delayed"] == 1).sum())
    elif "Delivery_Status" in df.columns:
        delayed_orders = int((df["Delivery_Status"].str.lower() == "delayed").sum())
    else:
        delayed_orders = 0
        
    delay_rate = (delayed_orders / total_orders * 100.0) if total_orders > 0 else 0.0
    on_time_rate = 100.0 - delay_rate
    
    avg_order_value = (total_sales / total_orders) if total_orders > 0 else 0.0
    avg_shipping_cost = (total_shipping_cost / total_orders) if total_orders > 0 else 0.0
    shipping_cost_pct = (total_shipping_cost / total_sales * 100.0) if total_sales > 0 else 0.0
    
    avg_distance = float(df["Distance_KM"].mean()) if "Distance_KM" in df.columns else 0.0
    avg_cost_per_km = float(df["Cost_Per_KM"].mean()) if "Cost_Per_KM" in df.columns else 0.0
    avg_cost_per_unit = float(df["Cost_Per_Unit"].mean()) if "Cost_Per_Unit" in df.columns else 0.0
    avg_rating = float(df["Customer_Rating"].mean()) if "Customer_Rating" in df.columns else 0.0
    avg_processing_days = float(df["Order_Processing_Days"].mean()) if "Order_Processing_Days" in df.columns else 0.0
    
    kpi_dict = {
        "Total_Orders": total_orders,
        "Total_Sales_USD": round(total_sales, 2),
        "Total_Shipping_Cost_USD": round(total_shipping_cost, 2),
        "Average_Order_Value_USD": round(avg_order_value, 2),
        "Average_Shipping_Cost_USD": round(avg_shipping_cost, 2),
        "Shipping_Cost_to_Sales_Ratio_Pct": round(shipping_cost_pct, 2),
        "Average_Delivery_Time_Days": round(avg_delivery_time, 2),
        "Median_Delivery_Time_Days": round(median_delivery_time, 2),
        "On_Time_Delivery_Rate_Pct": round(on_time_rate, 2),
        "Delivery_Delay_Rate_Pct": round(delay_rate, 2),
        "Delayed_Orders_Count": delayed_orders,
        "Average_Distance_KM": round(avg_distance, 2),
        "Average_Cost_Per_KM_USD": round(avg_cost_per_km, 4),
        "Average_Cost_Per_Unit_USD": round(avg_cost_per_unit, 2),
        "Average_Customer_Rating": round(avg_rating, 2),
        "Average_Order_Processing_Days": round(avg_processing_days, 2)
    }
    return kpi_dict


def analyze_regional_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Evaluates logistics volume, delivery latency, shipping expenditure,
    delay percentage, and customer satisfaction across geographic regions.
    """
    n_total = len(df)
    grouped = df.groupby("Region").agg(
        Order_Count=("Order_ID", "count"),
        Total_Sales_USD=("Sales_USD", "sum"),
        Avg_Sales_USD=("Sales_USD", "mean"),
        Total_Shipping_Cost_USD=("Shipping_Cost_USD", "sum"),
        Avg_Shipping_Cost_USD=("Shipping_Cost_USD", "mean"),
        Avg_Delivery_Time_Days=("Delivery_Time_Days", "mean"),
        Median_Delivery_Time_Days=("Delivery_Time_Days", "median"),
        Avg_Distance_KM=("Distance_KM", "mean"),
        Delayed_Orders=("Is_Delayed", lambda s: (s == 1).sum()),
        Avg_Customer_Rating=("Customer_Rating", "mean")
    ).reset_index()
    
    grouped["Volume_Share_Pct"] = (grouped["Order_Count"] / n_total * 100.0).round(2)
    grouped["Delay_Rate_Pct"] = (grouped["Delayed_Orders"] / grouped["Order_Count"] * 100.0).round(2)
    grouped["Shipping_Cost_Ratio_Pct"] = (grouped["Total_Shipping_Cost_USD"] / grouped["Total_Sales_USD"] * 100.0).round(2)
    
    # Sort by order count descending
    grouped = grouped.sort_values(by="Order_Count", ascending=False).reset_index(drop=True)
    
    # Round numerical outputs for clean reporting
    for col in ["Total_Sales_USD", "Avg_Sales_USD", "Total_Shipping_Cost_USD", "Avg_Shipping_Cost_USD", 
                "Avg_Delivery_Time_Days", "Median_Delivery_Time_Days", "Avg_Distance_KM", "Avg_Customer_Rating"]:
        grouped[col] = grouped[col].round(2)
        
    return grouped


def analyze_shipping_modes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compares operational throughput, transit speed, delivery reliability,
    and cost structure across shipping service tiers.
    """
    n_total = len(df)
    grouped = df.groupby("Shipping_Mode").agg(
        Order_Count=("Order_ID", "count"),
        Avg_Delivery_Time_Days=("Delivery_Time_Days", "mean"),
        Median_Delivery_Time_Days=("Delivery_Time_Days", "median"),
        Avg_Estimated_Days=("Estimated_Delivery_Days", "mean"),
        Avg_Shipping_Cost_USD=("Shipping_Cost_USD", "mean"),
        Avg_Cost_Per_KM=("Cost_Per_KM", "mean"),
        Avg_Cost_Per_Unit=("Cost_Per_Unit", "mean"),
        Avg_Distance_KM=("Distance_KM", "mean"),
        Delayed_Orders=("Is_Delayed", lambda s: (s == 1).sum()),
        Avg_Customer_Rating=("Customer_Rating", "mean")
    ).reset_index()
    
    grouped["Volume_Share_Pct"] = (grouped["Order_Count"] / n_total * 100.0).round(2)
    grouped["Delay_Rate_Pct"] = (grouped["Delayed_Orders"] / grouped["Order_Count"] * 100.0).round(2)
    grouped["On_Time_Rate_Pct"] = (100.0 - grouped["Delay_Rate_Pct"]).round(2)
    
    # Sort by Avg Delivery Time ascending
    grouped = grouped.sort_values(by="Avg_Delivery_Time_Days", ascending=True).reset_index(drop=True)
    
    for col in ["Avg_Delivery_Time_Days", "Median_Delivery_Time_Days", "Avg_Estimated_Days", 
                "Avg_Shipping_Cost_USD", "Avg_Cost_Per_Unit", "Avg_Distance_KM", "Avg_Customer_Rating"]:
        grouped[col] = grouped[col].round(2)
    grouped["Avg_Cost_Per_KM"] = grouped["Avg_Cost_Per_KM"].round(4)
    
    return grouped


def analyze_product_categories(df: pd.DataFrame) -> pd.DataFrame:
    """
    Assesses logistics burden, shipping costs, delivery speed, and sales
    contributions across diverse product categories.
    """
    n_total = len(df)
    grouped = df.groupby("Product_Category").agg(
        Order_Count=("Order_ID", "count"),
        Total_Quantity=("Quantity", "sum"),
        Total_Sales_USD=("Sales_USD", "sum"),
        Avg_Sales_USD=("Sales_USD", "mean"),
        Total_Shipping_Cost_USD=("Shipping_Cost_USD", "sum"),
        Avg_Shipping_Cost_USD=("Shipping_Cost_USD", "mean"),
        Avg_Delivery_Time_Days=("Delivery_Time_Days", "mean"),
        Delayed_Orders=("Is_Delayed", lambda s: (s == 1).sum()),
        Avg_Customer_Rating=("Customer_Rating", "mean")
    ).reset_index()
    
    grouped["Volume_Share_Pct"] = (grouped["Order_Count"] / n_total * 100.0).round(2)
    grouped["Delay_Rate_Pct"] = (grouped["Delayed_Orders"] / grouped["Order_Count"] * 100.0).round(2)
    grouped["Shipping_Cost_Ratio_Pct"] = (grouped["Total_Shipping_Cost_USD"] / grouped["Total_Sales_USD"] * 100.0).round(2)
    
    grouped = grouped.sort_values(by="Total_Sales_USD", ascending=False).reset_index(drop=True)
    
    for col in ["Total_Sales_USD", "Avg_Sales_USD", "Total_Shipping_Cost_USD", "Avg_Shipping_Cost_USD", 
                "Avg_Delivery_Time_Days", "Avg_Customer_Rating"]:
        grouped[col] = grouped[col].round(2)
        
    return grouped


def analyze_customer_segments(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyzes segment-specific logistics patterns, order volumes, revenue generation,
    shipping cost tolerances, and service quality ratings.
    """
    n_total = len(df)
    grouped = df.groupby("Customer_Segment").agg(
        Order_Count=("Order_ID", "count"),
        Total_Sales_USD=("Sales_USD", "sum"),
        Avg_Order_Value_USD=("Sales_USD", "mean"),
        Avg_Quantity=("Quantity", "mean"),
        Avg_Shipping_Cost_USD=("Shipping_Cost_USD", "mean"),
        Avg_Delivery_Time_Days=("Delivery_Time_Days", "mean"),
        Delayed_Orders=("Is_Delayed", lambda s: (s == 1).sum()),
        Avg_Customer_Rating=("Customer_Rating", "mean")
    ).reset_index()
    
    grouped["Volume_Share_Pct"] = (grouped["Order_Count"] / n_total * 100.0).round(2)
    grouped["Delay_Rate_Pct"] = (grouped["Delayed_Orders"] / grouped["Order_Count"] * 100.0).round(2)
    
    grouped = grouped.sort_values(by="Total_Sales_USD", ascending=False).reset_index(drop=True)
    
    for col in ["Total_Sales_USD", "Avg_Order_Value_USD", "Avg_Quantity", "Avg_Shipping_Cost_USD", 
                "Avg_Delivery_Time_Days", "Avg_Customer_Rating"]:
        grouped[col] = grouped[col].round(2)
        
    return grouped


def analyze_warehouse_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Evaluates fulfillment efficiency, dispatch processing times, delay rates,
    and volume throughput across regional warehouse facilities.
    """
    n_total = len(df)
    grouped = df.groupby("Warehouse_Code").agg(
        Order_Count=("Order_ID", "count"),
        Avg_Processing_Days=("Order_Processing_Days", "mean"),
        Avg_Delivery_Time_Days=("Delivery_Time_Days", "mean"),
        Avg_Distance_KM=("Distance_KM", "mean"),
        Avg_Shipping_Cost_USD=("Shipping_Cost_USD", "mean"),
        Delayed_Orders=("Is_Delayed", lambda s: (s == 1).sum()),
        Avg_Customer_Rating=("Customer_Rating", "mean")
    ).reset_index()
    
    grouped["Volume_Share_Pct"] = (grouped["Order_Count"] / n_total * 100.0).round(2)
    grouped["Delay_Rate_Pct"] = (grouped["Delayed_Orders"] / grouped["Order_Count"] * 100.0).round(2)
    
    grouped = grouped.sort_values(by="Order_Count", ascending=False).reset_index(drop=True)
    
    for col in ["Avg_Processing_Days", "Avg_Delivery_Time_Days", "Avg_Distance_KM", 
                "Avg_Shipping_Cost_USD", "Avg_Customer_Rating"]:
        grouped[col] = grouped[col].round(2)
        
    return grouped


def analyze_temporal_trends(df: pd.DataFrame, freq: str = "M") -> pd.DataFrame:
    """
    Aggregates order cadence, revenue, transportation expenditure, delivery speed,
    and delay rates across chronological time windows.
    """
    if "Order_Date" not in df.columns:
        raise ValueError("Order_Date column is required for temporal trend analysis.")
        
    df_temp = df.copy()
    df_temp["Period"] = df_temp["Order_Date"].dt.to_period(freq).astype(str)
    
    trend = df_temp.groupby("Period").agg(
        Order_Volume=("Order_ID", "count"),
        Total_Sales_USD=("Sales_USD", "sum"),
        Total_Shipping_Cost_USD=("Shipping_Cost_USD", "sum"),
        Avg_Delivery_Time_Days=("Delivery_Time_Days", "mean"),
        Delayed_Orders=("Is_Delayed", lambda s: (s == 1).sum()),
        Avg_Customer_Rating=("Customer_Rating", "mean")
    ).reset_index()
    
    trend["Delay_Rate_Pct"] = (trend["Delayed_Orders"] / trend["Order_Volume"] * 100.0).round(2)
    trend["Shipping_Cost_to_Sales_Pct"] = (trend["Total_Shipping_Cost_USD"] / trend["Total_Sales_USD"] * 100.0).round(2)
    
    for col in ["Total_Sales_USD", "Total_Shipping_Cost_USD", "Avg_Delivery_Time_Days", "Avg_Customer_Rating"]:
        trend[col] = trend[col].round(2)
        
    return trend
