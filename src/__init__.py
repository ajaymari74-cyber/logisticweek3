"""
Week 3: Advanced Data Analysis and Visualization in Logistics
Package initialization for logistics analytics modules.
"""

from .statistics import (
    compute_central_tendency,
    compute_dispersion,
    compute_shape_metrics,
    compute_correlation_matrix,
    detect_outliers_iqr,
    get_comprehensive_descriptive_stats
)

from .analysis import (
    load_logistics_data,
    compute_logistics_kpis,
    analyze_regional_performance,
    analyze_shipping_modes,
    analyze_product_categories,
    analyze_customer_segments,
    analyze_temporal_trends
)

from .visualization import (
    set_visual_style,
    plot_delivery_time_distribution,
    plot_shipping_cost_distribution,
    plot_shipment_volume_by_region,
    plot_avg_delivery_time_by_region_warehouse,
    plot_shipping_cost_by_mode,
    plot_delivery_time_by_mode,
    plot_distance_vs_delivery_time,
    plot_distance_vs_shipping_cost,
    plot_correlation_heatmap,
    plot_monthly_order_volume_cost_trend,
    plot_quantity_vs_shipping_cost,
    plot_product_category_performance,
    plot_delivery_status_delay_rate_by_mode,
    plot_customer_segment_comparison,
    plot_multivariate_delay_risk_matrix,
    generate_all_visualizations
)

from .insights import (
    generate_structured_insights,
    generate_bottleneck_matrix,
    generate_strategic_recommendations,
    export_executive_summary
)

__all__ = [
    "load_logistics_data",
    "compute_central_tendency",
    "compute_dispersion",
    "compute_shape_metrics",
    "compute_correlation_matrix",
    "detect_outliers_iqr",
    "get_comprehensive_descriptive_stats",
    "compute_logistics_kpis",
    "analyze_regional_performance",
    "analyze_shipping_modes",
    "analyze_product_categories",
    "analyze_customer_segments",
    "analyze_temporal_trends",
    "set_visual_style",
    "plot_delivery_time_distribution",
    "plot_shipping_cost_distribution",
    "plot_shipment_volume_by_region",
    "plot_avg_delivery_time_by_region_warehouse",
    "plot_shipping_cost_by_mode",
    "plot_delivery_time_by_mode",
    "plot_distance_vs_delivery_time",
    "plot_distance_vs_shipping_cost",
    "plot_correlation_heatmap",
    "plot_monthly_order_volume_cost_trend",
    "plot_quantity_vs_shipping_cost",
    "plot_product_category_performance",
    "plot_delivery_status_delay_rate_by_mode",
    "plot_customer_segment_comparison",
    "plot_multivariate_delay_risk_matrix",
    "generate_all_visualizations",
    "generate_structured_insights",
    "generate_bottleneck_matrix",
    "generate_strategic_recommendations",
    "export_executive_summary"
]
