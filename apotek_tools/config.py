"""Configuration module for Apotek Tools."""

import json
import os
from typing import Dict, Any, Optional

DEFAULT_CONFIG_FILE = "apotek_config.json"

# Default configuration values
DEFAULT_CONFIG = {
    "contact": {
        "whatsapp": "+6281223556554",
        "email": "kontak@auliafarma.co.id"
    },
    "api": {
        "base_url": "https://auliafarma.co.id/api/",
        "cookie_file": "cookie.json"
    }
}


def load_config(config_file: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration from file.
    
    Args:
        config_file: Path to the configuration file. If None, uses DEFAULT_CONFIG_FILE.
        
    Returns:
        Dict[str, Any]: Configuration dictionary
    """
    config_path = config_file or DEFAULT_CONFIG_FILE
    
    # If the configuration file doesn't exist, create it with defaults
    if not os.path.exists(config_path):
        save_config(DEFAULT_CONFIG, config_path)
        return DEFAULT_CONFIG
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except (json.JSONDecodeError, FileNotFoundError):
        # If there's an error loading the file, return default config
        return DEFAULT_CONFIG


def save_config(config: Dict[str, Any], config_file: Optional[str] = None) -> None:
    """Save configuration to file.
    
    Args:
        config: Configuration dictionary
        config_file: Path to the configuration file. If None, uses DEFAULT_CONFIG_FILE.
    """
    config_path = config_file or DEFAULT_CONFIG_FILE
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)


def get_contact_info(config_file: Optional[str] = None) -> Dict[str, str]:
    """Get contact information from config.
    
    Args:
        config_file: Path to the configuration file. If None, uses DEFAULT_CONFIG_FILE.
        
    Returns:
        Dict[str, str]: Contact information
    """
    config = load_config(config_file)
    return config.get("contact", DEFAULT_CONFIG["contact"])


def update_contact_info(whatsapp: Optional[str] = None, email: Optional[str] = None, 
                      config_file: Optional[str] = None) -> Dict[str, str]:
    """Update contact information in config.
    
    Args:
        whatsapp: WhatsApp number
        email: Email address
        config_file: Path to the configuration file. If None, uses DEFAULT_CONFIG_FILE.
        
    Returns:
        Dict[str, str]: Updated contact information
    """
    config = load_config(config_file)
    
    if "contact" not in config:
        config["contact"] = DEFAULT_CONFIG["contact"]
    
    if whatsapp:
        config["contact"]["whatsapp"] = whatsapp
    
    if email:
        config["contact"]["email"] = email
    
    save_config(config, config_file)
    return config["contact"] 