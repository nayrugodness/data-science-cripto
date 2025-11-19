"""
Dune Configuration Module
Loads and exports all Dune-related environment variables
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Dune API Configuration
DUNE_API_KEY = os.getenv("DUNE_API_KEY")

# API URLs
DUNE_SIM_BASE_URL = os.getenv("DUNE_SIM", "https://api.sim.dune.com/v1")
DUNE_BASE_URL = os.getenv("DUNE_DUNE", "https://api.dune.com/api/v1")

# Chain IDs
DUNE_CHAIN_ID_ETH = int(os.getenv("DUNE_CHAIN_ID_ETH", "1"))
DUNE_CHAIN_ID_POLYGON = int(os.getenv("DUNE_CHAIN_ID_POLYGON", "137"))

# Token Addresses
DUNE_COPM_TOKEN_ADDRESS = os.getenv("DUNE_COPM_TOKEN_ADDRESS")
DUNE_COPW_TOKEN_ADDRESS = os.getenv("DUNE_COPW_TOKEN_ADDRESS")

# Validation
def validate_config():
    """Validate that all required environment variables are set"""
    required_vars = {
        "DUNE_API_KEY": DUNE_API_KEY,
        "DUNE_COPM_TOKEN_ADDRESS": DUNE_COPM_TOKEN_ADDRESS,
        "DUNE_COPW_TOKEN_ADDRESS": DUNE_COPW_TOKEN_ADDRESS,
    }
    
    missing_vars = [name for name, value in required_vars.items() if value is None]
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Export all configuration
__all__ = [
    'DUNE_API_KEY',
    'DUNE_SIM_BASE_URL',
    'DUNE_BASE_URL',
    'DUNE_CHAIN_ID_ETH',
    'DUNE_CHAIN_ID_POLYGON',
    'DUNE_COPM_TOKEN_ADDRESS',
    'DUNE_COPW_TOKEN_ADDRESS',
    'validate_config'
]
