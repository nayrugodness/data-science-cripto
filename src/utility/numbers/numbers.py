"""
Number Utility Functions
Reusable functions for number formatting and calculations
"""
import pandas as pd
from typing import Dict, Any, Optional


def format_number_with_commas(value: float, decimals: int = 2) -> str:
    """
    Format a number with commas and specified decimal places
    
    Args:
        value: Number to format
        decimals: Number of decimal places (default: 2)
        
    Returns:
        Formatted string
    """
    return f"{value:,.{decimals}f}"


def calculate_percentage_change(old_value: float, new_value: float, 
                                decimals: int = 2) -> float:
    """
    Calculate percentage change between two values
    
    Args:
        old_value: Original value
        new_value: New value
        decimals: Number of decimal places (default: 2)
        
    Returns:
        Percentage change as float
    """
    if old_value == 0:
        return 0.0
    return round(((new_value - old_value) / old_value) * 100, decimals)


def safe_division(numerator: float, denominator: float, 
                 default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning default if denominator is zero
    
    Args:
        numerator: Numerator value
        denominator: Denominator value
        default: Value to return if denominator is zero (default: 0.0)
        
    Returns:
        Division result or default value
    """
    return numerator / denominator if denominator != 0 else default


def aggregate_metrics(df: pd.DataFrame, column: str, 
                     operations: list = None) -> Dict[str, Any]:
    """
    Calculate multiple aggregate metrics for a column
    
    Args:
        df: DataFrame with data
        column: Column name to aggregate
        operations: List of operations to perform 
                   (default: ['sum', 'mean', 'min', 'max'])
        
    Returns:
        Dictionary with metric results
    """
    if operations is None:
        operations = ['sum', 'mean', 'min', 'max']
    
    if df.empty or column not in df.columns:
        return {op: 0 for op in operations}
    
    results = {}
    for op in operations:
        if op == 'sum':
            results[op] = df[column].sum()
        elif op == 'mean':
            results[op] = df[column].mean()
        elif op == 'min':
            results[op] = df[column].min()
        elif op == 'max':
            results[op] = df[column].max()
        elif op == 'count':
            results[op] = df[column].count()
    
    return results
