"""
Dashboard Service
High-level service for dashboard data operations
"""
import pandas as pd
from typing import Tuple, Dict, Any
from src.api import DuneAPI
from src.config import DUNE_COPM_TOKEN_ADDRESS, DUNE_COPW_TOKEN_ADDRESS
from src.helpers.dune import (
    normalize_token_balance,
    filter_by_token_address,
    create_comparison_dataframe,
    prepare_holder_display_columns,
    calculate_holder_metrics
)


class DashboardService:
    """Service class for dashboard data operations"""
    
    def __init__(self):
        """Initialize the dashboard service with Dune API"""
        self.api = DuneAPI()
        self.decimals = 18  # Blockchain storage uses 18 decimals (wei format)
    
    def get_holders_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Get and prepare holders data for both tokens
        
        Returns:
            Tuple of (copm_df, copw_df) with normalized balances
        """
        df_copm = self.api.get_copm_holders()
        df_copw = self.api.get_copw_holders()
        
        df_copm = normalize_token_balance(df_copm, decimals=self.decimals)
        df_copw = normalize_token_balance(df_copw, decimals=self.decimals)
        
        return df_copm, df_copw
    
    def get_display_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare DataFrame for display
        
        Args:
            df: Raw holders DataFrame
            
        Returns:
            DataFrame with display columns and formatted balance
        """
        return prepare_holder_display_columns(df, decimals=self.decimals)
    
    def get_metrics(self, df_copm: pd.DataFrame, df_copw: pd.DataFrame) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Calculate metrics for both tokens
        
        Args:
            df_copm: COPM holders DataFrame
            df_copw: COPW holders DataFrame
            
        Returns:
            Tuple of (copm_metrics, copw_metrics)
        """
        copm_metrics = calculate_holder_metrics(df_copm)
        copw_metrics = calculate_holder_metrics(df_copw)
        return copm_metrics, copw_metrics
    
    def get_comparison_data(self, df_copm: pd.DataFrame, df_copw: pd.DataFrame) -> pd.DataFrame:
        """
        Get comparison data for both tokens
        
        Args:
            df_copm: COPM holders DataFrame
            df_copw: COPW holders DataFrame
            
        Returns:
            Comparison DataFrame
        """
        return create_comparison_dataframe(df_copm, df_copw)

