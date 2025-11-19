"""
Graph Utility Functions
Reusable functions for creating charts and visualizations
"""
import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure
from typing import Optional


def create_comparison_bar_chart(df: pd.DataFrame, x: str = "Token", 
                                y: list = None, title: str = None,
                                barmode: str = 'group') -> Figure:
    """
    Create a grouped bar chart for comparing metrics
    
    Args:
        df: DataFrame with comparison data
        x: Column name for x-axis (default: "Token")
        y: List of column names for y-axis (default: ["Total Holders", "Active Holders"])
        title: Chart title (optional)
        barmode: Bar mode - 'group' or 'stack' (default: 'group')
        
    Returns:
        Plotly Figure object
    """
    if y is None:
        y = ["Total Holders", "Active Holders"]
    
    fig = px.bar(df, x=x, y=y, barmode=barmode, text_auto=True, title=title,
                 color_discrete_map={
                     "Total Holders": "#636EFA",  # Blue
                     "Active Holders": "#00CC96"  # Green
                 })
    return fig


def create_line_chart(df: pd.DataFrame, x: str, y: str, title: str = None,
                     x_label: str = None, y_label: str = None, 
                     markers: bool = True) -> Figure:
    """
    Create a line chart for time series data
    
    Args:
        df: DataFrame with time series data
        x: Column name for x-axis
        y: Column name for y-axis
        title: Chart title (optional)
        x_label: Label for x-axis (optional)
        y_label: Label for y-axis (optional)
        markers: Whether to show markers (default: True)
        
    Returns:
        Plotly Figure object
    """
    fig = px.line(df, x=x, y=y, markers=markers, title=title)
    
    if x_label or y_label:
        fig.update_layout(
            xaxis_title=x_label or x,
            yaxis_title=y_label or y
        )
    
    return fig


def create_token_volume_chart(df: pd.DataFrame, token_name: str,
                              x_col: str = 'day', y_col: str = 'total_volume') -> Figure:
    """
    Create a volume chart specifically for token transactions
    
    Args:
        df: DataFrame with token transaction history
        token_name: Name of the token for the title
        x_col: Column name for date/time (default: 'day')
        y_col: Column name for volume (default: 'total_volume')
        
    Returns:
        Plotly Figure object
    """
    return create_line_chart(
        df=df,
        x=x_col,
        y=y_col,
        title=f"{token_name} - Volumen diario de transacciones",
        x_label="Día",
        y_label="Volumen (tokens)",
        markers=True
    )
