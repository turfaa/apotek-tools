"""Core API module for interacting with the Apotek Aulia Farma API."""

import json
import os
from typing import Dict, List, Optional, Any, Union
from urllib.parse import urljoin

import requests
from rich.console import Console

# Initialize console for rich output
console = Console()

# Base API configuration
API_BASE_URL = "https://auliafarma.co.id/api/"
COOKIE_FILE = "cookie.json"

# Available endpoints
ENDPOINTS = {
    "drugs": "drugs",
}


def load_cookies() -> Dict[str, str]:
    """Load cookies from the cookie file.
    
    Returns:
        Dict[str, str]: Dictionary of cookies
    """
    if not os.path.exists(COOKIE_FILE):
        return {}
    
    try:
        with open(COOKIE_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_cookies(cookies: Dict[str, str]) -> None:
    """Save cookies to the cookie file.
    
    Args:
        cookies (Dict[str, str]): Dictionary of cookies to save
    """
    with open(COOKIE_FILE, "w") as f:
        json.dump(cookies, f, indent=2)


def api_request(
    endpoint: str,
    method: str = "GET",
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None,
    cookies: Optional[Dict[str, str]] = None,
    headers: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Make a generic API request.
    
    Args:
        endpoint (str): API endpoint (e.g., "drugs")
        method (str, optional): HTTP method. Defaults to "GET".
        params (Optional[Dict[str, Any]], optional): Query parameters. Defaults to None.
        data (Optional[Dict[str, Any]], optional): Request body data. Defaults to None.
        cookies (Optional[Dict[str, str]], optional): Cookies. Defaults to None.
        headers (Optional[Dict[str, str]], optional): HTTP headers. Defaults to None.
    
    Returns:
        Dict[str, Any]: API response data
    
    Raises:
        ValueError: If the endpoint is invalid
        requests.RequestException: If the API request fails
    """
    if endpoint not in ENDPOINTS:
        raise ValueError(f"Invalid endpoint: {endpoint}")
    
    # Load cookies if not provided
    if cookies is None:
        cookies = load_cookies()
    
    # Build URL
    url = urljoin(API_BASE_URL, ENDPOINTS[endpoint])
    
    # Default headers
    if headers is None:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
    
    console.print(f"Making {method} request to {url}...", style="bold cyan")
    
    try:
        response = requests.request(
            method=method,
            url=url,
            params=params,
            json=data,
            cookies=cookies,
            headers=headers,
        )
        response.raise_for_status()
        
        # Save any new cookies
        if response.cookies:
            for key, value in response.cookies.items():
                cookies[key] = value
            save_cookies(cookies)
        
        return response.json()
    except requests.RequestException as e:
        console.print(f"API request failed: {e}", style="bold red")
        raise


def get_drugs(cookies: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
    """Get the drug list from the API.
    
    Args:
        cookies (Optional[Dict[str, str]], optional): Cookies. Defaults to None.
    
    Returns:
        List[Dict[str, Any]]: List of drugs
    """
    response = api_request("drugs", cookies=cookies)
    return response.get("drugs", [])
