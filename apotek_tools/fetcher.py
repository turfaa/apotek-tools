"""Module for fetching and processing drug data from the Apotek Aulia Farma API."""

from datetime import datetime
from typing import Dict, List, Optional, Any

from rich.console import Console

from apotek_tools.api import get_drugs

console = Console()


def fetch_drug_list(cookies: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
    """Fetch the drug list from the API.
    
    Args:
        cookies (Optional[Dict[str, str]], optional): Dictionary of cookies. Defaults to None.
    
    Returns:
        List[Dict[str, Any]]: List of drugs
    
    Raises:
        requests.RequestException: If the API request fails
    """
    try:
        return get_drugs(cookies)
    except Exception as e:
        console.print(f"Error fetching drug list: {e}", style="bold red")
        raise


def parse_price(price_string: str) -> int:
    """Parse a price string in the format 'Rp X.XXX' to an integer.
    
    Args:
        price_string (str): Price string in the format 'Rp X.XXX'
    
    Returns:
        int: Price as an integer
    """
    # Remove 'Rp ', replace dots, and convert to int
    try:
        clean_price = price_string.replace("Rp ", "").replace(".", "").split(" / ")[0].strip()
        return int(clean_price)
    except (ValueError, IndexError):
        return 0


def parse_stock(stock_string: str) -> int:
    """Parse a stock string in the format 'X Unit' to an integer.
    
    Args:
        stock_string (str): Stock string in the format 'X Unit'
    
    Returns:
        int: Stock as an integer
    """
    try:
        # Extract the number from the stock string (e.g., "10 Pcs" -> 10)
        return int(stock_string.split(" ")[0])
    except (ValueError, IndexError):
        return 0


def get_current_date() -> str:
    """Get the current date in the format '30 Maret 2023'.
    
    Returns:
        str: Current date in Indonesian format
    """
    month_map = {
        1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
        5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
        9: "September", 10: "Oktober", 11: "November", 12: "Desember"
    }
    
    now = datetime.now()
    return f"{now.day} {month_map[now.month]} {now.year}"


def process_drug_data(drugs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Process the drug data into a more usable format.
    
    Args:
        drugs (List[Dict[str, Any]]): List of drugs from the API
    
    Returns:
        List[Dict[str, Any]]: Processed drug list
    """
    processed_drugs = []
    
    for drug in drugs:
        processed_drug = {
            "vmedisCode": drug.get("vmedisCode", ""),
            "name": drug.get("name", ""),
            "discount_price": None,
            "normal_price": None,
            "prescription_price": None,
            "stock": None,
            "min_stock": None
        }
        
        sections = drug.get("sections", [])
        for section in sections:
            title = section.get("title", "")
            rows = section.get("rows", [])
            
            if title == "Harga Diskon" and rows:
                processed_drug["discount_price"] = "\n".join(rows)
            elif title == "Harga Normal" and rows:
                processed_drug["normal_price"] = "\n".join(rows)
            elif title == "Harga Resep" and rows:
                processed_drug["prescription_price"] = "\n".join(rows)
            elif title == "Sisa Stok" and rows:
                if len(rows) == 1 and rows[0] == "Stok habis":
                    processed_drug["stock"] = "Stok habis"
                else:
                    processed_drug["stock"] = "\n".join(rows)
            elif title == "Stok Minimum" and rows:
                processed_drug["min_stock"] = "\n".join(rows)
        
        # Only add drugs with stock
        if processed_drug["stock"] and processed_drug["stock"] != "Stok habis":
            processed_drugs.append(processed_drug)
    
    return processed_drugs
