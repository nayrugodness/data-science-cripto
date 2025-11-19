"""
Dune Utility Functions
Helper functions for processing and transforming Dune data
"""
import pandas as pd
from typing import List, Dict, Any


def normalize_token_balance(df: pd.DataFrame, decimals: int = 18, balance_col: str = 'balance', 
                            output_col: str = 'balance_token') -> pd.DataFrame:
    """
    Normalize token balances from wei to token units
    
    Args:
        df: DataFrame with balance column
        decimals: Number of decimals for the token (default: 18)
        balance_col: Name of the balance column (default: 'balance')
        output_col: Name of the output column (default: 'balance_token')
        
    Returns:
        DataFrame with normalized balance column added
    """
    if not df.empty and balance_col in df.columns:
        df[output_col] = df[balance_col] / (10**decimals)
    return df


def filter_by_token_address(df: pd.DataFrame, token_address: str, 
                            token_col: str = 'token') -> pd.DataFrame:
    """
    Filter DataFrame by token address
    
    Args:
        df: DataFrame with token column
        token_address: Token contract address to filter by
        token_col: Name of the token column (default: 'token')
        
    Returns:
        Filtered DataFrame
    """
    if df.empty or token_col not in df.columns:
        return pd.DataFrame()
    return df[df[token_col] == token_address]


def calculate_holder_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate metrics for token holders
    
    Args:
        df: DataFrame with holder data
        
    Returns:
        Dictionary with metrics:
        - total_holders: Total number of holders
        - active_holders: Number of holders who initiated transfers
        - average_balance: Average token balance (if balance_token column exists)
    """
    if df.empty:
        return {
            'total_holders': 0,
            'active_holders': 0,
            'average_balance': 0.0
        }
    
    metrics = {
        'total_holders': len(df),
        'active_holders': df['has_initiated_transfer'].sum() if 'has_initiated_transfer' in df.columns else 0
    }
    
    if 'balance_token' in df.columns:
        metrics['average_balance'] = df['balance_token'].mean()
    
    return metrics


def create_comparison_dataframe(copm_df: pd.DataFrame, copw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a comparison DataFrame for COPM vs COPW tokens
    
    Args:
        copm_df: DataFrame with COPM holder data
        copw_df: DataFrame with COPW holder data
        
    Returns:
        DataFrame with comparison metrics
    """
    copm_metrics = calculate_holder_metrics(copm_df)
    copw_metrics = calculate_holder_metrics(copw_df)
    
    return pd.DataFrame({
        "Token": ["COPM", "COPW"],
        "Total Holders": [copm_metrics['total_holders'], copw_metrics['total_holders']],
        "Active Holders": [copm_metrics['active_holders'], copw_metrics['active_holders']]
    })


def prepare_holder_display_columns(df: pd.DataFrame, 
                                   columns: List[str] = None) -> pd.DataFrame:
    """
    Prepare DataFrame for display with specific columns
    
    Args:
        df: DataFrame with holder data
        columns: List of columns to include (default: wallet_address, balance, 
                has_initiated_transfer, first_acquired)
        
    Returns:
        DataFrame with selected columns
    """
    if columns is None:
        columns = ['wallet_address', 'balance', 'has_initiated_transfer', 'first_acquired']
    
    if df.empty:
        return df
    
    available_columns = [col for col in columns if col in df.columns]
    return df[available_columns] if available_columns else df
