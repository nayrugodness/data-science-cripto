"""
Dune API Endpoints
Defines API endpoints and business logic for Dune data retrieval
"""
import pandas as pd
from typing import List, Dict, Any
from .httpClient import DuneHttpClient
from src.config import (
    DUNE_SIM_BASE_URL,
    DUNE_BASE_URL,
    DUNE_CHAIN_ID_ETH,
    DUNE_CHAIN_ID_POLYGON,
    DUNE_COPM_TOKEN_ADDRESS,
    DUNE_COPW_TOKEN_ADDRESS
)


class DuneAPI:
    """API wrapper for Dune endpoints"""
    
    def __init__(self, client: DuneHttpClient = None):
        """
        Initialize Dune API wrapper
        
        Args:
            client: HTTP client for making requests (defaults to new client)
        """
        self.client = client or DuneHttpClient()
        self.sim_base_url = DUNE_SIM_BASE_URL
        self.dune_base_url = DUNE_BASE_URL
    
    def get_token_holders(self, chain_id: int = None, token_address: str = None) -> pd.DataFrame:
        """
        Get token holders from Dune SIM API
        
        Args:
            chain_id: Blockchain chain ID (uses config if not provided)
            token_address: Token contract address (uses config if not provided)
            
        Returns:
            DataFrame with holders data sorted by balance (descending)
        """
        url = f"{self.sim_base_url}/evm/token-holders/{chain_id}/{token_address}"
        data = self.client.get(url, use_sim=True)
        
        holders = data.get("holders", [])
        df = pd.DataFrame(holders)
        
        if not df.empty:
            df['balance'] = df['balance'].astype(float)
            df = df.sort_values(by='balance', ascending=False).reset_index(drop=True)
        
        return df
    
    
    def get_copm_holders(self) -> pd.DataFrame:
        """
        Get COPM token holders (uses config values)
        
        Returns:
            DataFrame with COPM holders data
        """
        return self.get_token_holders(DUNE_CHAIN_ID_POLYGON, DUNE_COPM_TOKEN_ADDRESS)
    
    def get_copw_holders(self) -> pd.DataFrame:
        """
        Get COPW token holders (uses config values)
        
        Returns:
            DataFrame with COPW holders data
        """
        return self.get_token_holders(DUNE_CHAIN_ID_ETH, DUNE_COPW_TOKEN_ADDRESS)
