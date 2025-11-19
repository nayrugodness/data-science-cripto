"""
HTTP Client for Dune API
Handles all HTTP requests to Dune endpoints
"""
import requests
from typing import Dict, Any
from src.config import DUNE_API_KEY


class DuneHttpClient:
    """HTTP client for interacting with Dune APIs"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize the Dune HTTP client
        
        Args:
            api_key: Dune API key for authentication (defaults to config)
        """
        self.api_key = api_key or DUNE_API_KEY
        self.headers = {
            "X-Dune-Api-Key": self.api_key,
            "Authorization": f"Bearer {self.api_key}"
        }
        self.sim_headers = {
            "X-Sim-Api-Key": self.api_key,
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def get(self, url: str, use_sim: bool = False) -> Dict[str, Any]:
        """
        Make a GET request to Dune API
        
        Args:
            url: Full URL to request
            use_sim: If True, use SIM API headers instead of standard headers
            
        Returns:
            JSON response as dictionary
            
        Raises:
            requests.HTTPError: If request fails
        """
        headers = self.sim_headers if use_sim else self.headers
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def post(self, url: str, data: Dict[str, Any] = None, use_sim: bool = False) -> Dict[str, Any]:
        """
        Make a POST request to Dune API
        
        Args:
            url: Full URL to request
            data: JSON payload to send
            use_sim: If True, use SIM API headers instead of standard headers
            
        Returns:
            JSON response as dictionary
            
        Raises:
            requests.HTTPError: If request fails
        """
        headers = self.sim_headers if use_sim else self.headers
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
