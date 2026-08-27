"""
Week 3: Advanced Data Analysis and Visualization in Logistics
Module: statistics.py
Author: Senior Logistics Data Analyst
Description:
    Provides robust statistical computing routines including central tendency,
    dispersion, distribution shape metrics (skewness/kurtosis), IQR outlier detection,
    and parametric/non-parametric correlation analysis with p-values.
"""

from typing import List, Optional, Tuple, Dict, Any
import numpy as np
import pandas as pd
from scipy import stats


def get_default_numeric_columns(df: pd.DataFrame) -> List[str]:
    """
    Returns meaningful numerical logistics columns excluding identifiers,
    one-hot encoded binary columns, and normalized helper columns.
    """
    excluded_prefixes = ("Enc_", "Norm_")
    excluded_exact = {"Order_ID", "Is_Delayed"}
    
    numeric_cols = []
    for col in df.select_dtypes(include=[np.number]).columns:
        if col in excluded_exact:
            continue
        if any(col.startswith(prefix) for prefix in excluded_prefixes):
            continue
        numeric_cols.append(col)
    return numeric_cols


def compute_central_tendency(
    df: pd.DataFrame, 
    cols: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Calculates measures of central tendency: Mean, Median, Mode, 
    and 5% Trimmed Mean for numerical logistics variables.
    """
    if cols is None:
        cols = get_default_numeric_columns(df)
        
    records = []
    for col in cols:
        series = df[col].dropna()
        if len(series) == 0:
            continue
            
        mean_val = float(series.mean())
        median_val = float(series.median())
        mode_series = series.mode()
        mode_val = float(mode_series.iloc[0]) if not mode_series.empty else np.nan
        trimmed_mean_val = float(stats.trim_mean(series, proportiontocut=0.05))
        
        records.append({
            "Variable": col,
            "Count": int(len(series)),
            "Mean": round(mean_val, 4),
            "Median": round(median_val, 4),
            "Mode": round(mode_val, 4),
            "Trimmed_Mean_5%": round(trimmed_mean_val, 4)
        })
        
    return pd.DataFrame(records).set_index("Variable")


def compute_dispersion(
    df: pd.DataFrame, 
    cols: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Calculates measures of statistical dispersion: Standard Deviation,
    Variance, Range, Minimum, Maximum, IQR, and Coefficient of Variation (CV).
    """
    if cols is None:
        cols = get_default_numeric_columns(df)
        
    records = []
    for col in cols:
        series = df[col].dropna()
        if len(series) == 0:
            continue
            
        std_val = float(series.std(ddof=1))
        var_val = float(series.var(ddof=1))
        min_val = float(series.min())
        max_val = float(series.max())
        range_val = max_val - min_val
        q1_val = float(series.quantile(0.25))
        q3_val = float(series.quantile(0.75))
        iqr_val = q3_val - q1_val
        mean_val = float(series.mean())
        cv_val = (std_val / mean_val * 100.0) if mean_val != 0 else np.nan
        
        records.append({
            "Variable": col,
            "Min": round(min_val, 4),
            "Q1_25%": round(q1_val, 4),
            "Q3_75%": round(q3_val, 4),
            "Max": round(max_val, 4),
            "Range": round(range_val, 4),
            "IQR": round(iqr_val, 4),
            "Std_Dev": round(std_val, 4),
            "Variance": round(var_val, 4),
            "CV_Percent": round(cv_val, 2)
        })
        
    return pd.DataFrame(records).set_index("Variable")


def compute_shape_metrics(
    df: pd.DataFrame, 
    cols: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Calculates skewness, kurtosis, and categorical interpretation
    of probability distribution symmetry and tail heaviness.
    """
    if cols is None:
        cols = get_default_numeric_columns(df)
        
    records = []
    for col in cols:
        series = df[col].dropna()
        if len(series) == 0:
            continue
            
        skew_val = float(series.skew())
        kurt_val = float(series.kurtosis())  # Excess kurtosis (Fisher's definition)
        
        # Skewness interpretation
        if abs(skew_val) < 0.5:
            skew_desc = "Approximately Symmetric"
        elif 0.5 <= skew_val <= 1.0:
            skew_desc = "Moderately Positively Skewed (Right Tail)"
        elif skew_val > 1.0:
            skew_desc = "Highly Positively Skewed (Right Tail)"
        elif -1.0 <= skew_val <= -0.5:
            skew_desc = "Moderately Negatively Skewed (Left Tail)"
        else:
            skew_desc = "Highly Negatively Skewed (Left Tail)"
            
        # Kurtosis interpretation
        if abs(kurt_val) < 0.5:
            kurt_desc = "Mesokurtic (Normal Tail Weight)"
        elif kurt_val >= 0.5:
            kurt_desc = "Leptokurtic (Heavy Tails / Outlier Prone)"
        else:
            kurt_desc = "Platykurtic (Light Tails / Flat Peak)"
            
        records.append({
            "Variable": col,
            "Skewness": round(skew_val, 4),
            "Skewness_Interpretation": skew_desc,
            "Excess_Kurtosis": round(kurt_val, 4),
            "Kurtosis_Interpretation": kurt_desc
        })
        
    return pd.DataFrame(records).set_index("Variable")


def get_comprehensive_descriptive_stats(
    df: pd.DataFrame, 
    cols: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Compiles an exhaustive statistical summary table combining central tendency,
    dispersion quartiles, and distribution shape metrics for executive reporting.
    """
    if cols is None:
        cols = get_default_numeric_columns(df)
        
    cent = compute_central_tendency(df, cols)
    disp = compute_dispersion(df, cols)
    shape = compute_shape_metrics(df, cols)
    
    merged = pd.concat([
        cent[["Count", "Mean", "Median", "Mode", "Trimmed_Mean_5%"]],
        disp[["Std_Dev", "Variance", "Min", "Q1_25%", "Q3_75%", "Max", "Range", "IQR", "CV_Percent"]],
        shape[["Skewness", "Excess_Kurtosis"]]
    ], axis=1)
    
    return merged


def compute_correlation_matrix(
    df: pd.DataFrame, 
    cols: Optional[List[str]] = None,
    method: str = "pearson"
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Calculates the correlation coefficient matrix alongside two-tailed p-values.
    
    Returns:
        corr_matrix: pd.DataFrame of correlation coefficients
        pval_matrix: pd.DataFrame of p-values for hypothesis testing (H0: r = 0)
    """
    if cols is None:
        cols = get_default_numeric_columns(df)
        
    clean_sub = df[cols].dropna()
    corr_matrix = clean_sub.corr(method=method)
    
    # Compute p-values matrix
    pval_matrix = pd.DataFrame(index=cols, columns=cols, dtype=float)
    for col1 in cols:
        for col2 in cols:
            if col1 == col2:
                pval_matrix.loc[col1, col2] = 0.0
            else:
                if method == "pearson":
                    _, p_val = stats.pearsonr(clean_sub[col1], clean_sub[col2])
                elif method == "spearman":
                    _, p_val = stats.spearmanr(clean_sub[col1], clean_sub[col2])
                else:
                    p_val = np.nan
                pval_matrix.loc[col1, col2] = p_val
                
    return corr_matrix, pval_matrix


def detect_outliers_iqr(
    df: pd.DataFrame, 
    cols: Optional[List[str]] = None,
    multiplier: float = 1.5
) -> pd.DataFrame:
    """
    Identifies outliers using Tukey's Fences method (Q1 - k*IQR, Q3 + k*IQR).
    Returns boundary thresholds and outlier frequency/percentage per variable.
    """
    if cols is None:
        cols = get_default_numeric_columns(df)
        
    records = []
    n_total = len(df)
    
    for col in cols:
        series = df[col].dropna()
        q1 = float(series.quantile(0.25))
        q3 = float(series.quantile(0.75))
        iqr = q3 - q1
        lower_fence = q1 - (multiplier * iqr)
        upper_fence = q3 + (multiplier * iqr)
        
        outliers = series[(series < lower_fence) | (series > upper_fence)]
        outlier_count = len(outliers)
        outlier_pct = (outlier_count / n_total) * 100.0 if n_total > 0 else 0.0
        
        records.append({
            "Variable": col,
            "Q1": round(q1, 3),
            "Q3": round(q3, 3),
            "IQR": round(iqr, 3),
            "Lower_Fence": round(lower_fence, 3),
            "Upper_Fence": round(upper_fence, 3),
            "Outlier_Count": int(outlier_count),
            "Outlier_Percent": round(outlier_pct, 2)
        })
        
    return pd.DataFrame(records).set_index("Variable")
