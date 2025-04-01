"""Command line interface for Apotek Tools."""

import json
import os
import sys
from typing import Dict, Optional

import click
from rich.console import Console
from rich.table import Table

from apotek_tools.fetcher import fetch_drug_list, process_drug_data, get_current_date
from apotek_tools.excel_generator import generate_excel
from apotek_tools.config import get_contact_info, update_contact_info, DEFAULT_CONFIG_FILE

console = Console()


def display_drug_table(drugs, limit=10):
    """Display a table of drugs.
    
    Args:
        drugs: List of drug dictionaries
        limit: Maximum number of drugs to display
    """
    table = Table(title=f"Drug List (showing {min(limit, len(drugs))} of {len(drugs)})")
    
    table.add_column("Name", style="cyan")
    table.add_column("Discount Price", style="green")
    table.add_column("Stock", style="yellow")
    
    for i, drug in enumerate(drugs):
        if i >= limit:
            break
        
        table.add_row(
            drug["name"],
            drug["discount_price"] or "N/A",
            drug["stock"] or "N/A"
        )
    
    console.print(table)


@click.group()
@click.version_option()
def cli():
    """Apotek Tools - CLI for interacting with Apotek Aulia Farma API."""
    pass


# Price List Commands Group
@cli.group()
def pricelist():
    """Commands for managing price lists."""
    pass


@pricelist.command("fetch")
@click.option("--cookie", "-c", help="Cookie value to use for authentication (JSON format)")
@click.option("--cookie-file", default="cookie.json", help="Path to cookie file (default: cookie.json)")
@click.option("--output", "-o", help="Output file path")
@click.option("--preview/--no-preview", default=True, help="Preview the data before generating Excel")
@click.option("--preview-limit", default=10, help="Number of items to preview")
@click.option("--config-file", help=f"Path to config file (default: {DEFAULT_CONFIG_FILE})")
def fetch_pricelist(cookie: Optional[str], cookie_file: Optional[str], output: Optional[str], 
         preview: bool, preview_limit: int, config_file: Optional[str]):
    """Fetch drug price list from the API and generate an Excel file."""
    cookies = {}
    
    # Load cookies from command line
    if cookie:
        try:
            cookies = json.loads(cookie)
        except json.JSONDecodeError:
            console.print("Invalid cookie JSON format", style="bold red")
            sys.exit(1)
    
    # Load cookies from file
    elif cookie_file:
        try:
            with open(cookie_file, "r") as f:
                cookies = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            console.print(f"Could not load cookies from {cookie_file}", style="bold yellow")
    
    try:
        # Fetch the drug list
        drug_list = fetch_drug_list(cookies)
        console.print(f"Fetched {len(drug_list)} drugs", style="bold green")
        
        # Process the drug data
        processed_drugs = process_drug_data(drug_list)
        console.print(f"Processed {len(processed_drugs)} drugs with stock", style="bold green")
        
        # Preview the data
        if preview and processed_drugs:
            display_drug_table(processed_drugs, preview_limit)
            
            if not click.confirm("Generate Excel file?", default=True):
                console.print("Operation cancelled", style="bold yellow")
                return
        
        # Generate the Excel file
        if processed_drugs:
            excel_file = generate_excel(processed_drugs, output, config_file)
            if excel_file:
                console.print(f"Excel file generated: {excel_file}", style="bold green")
        else:
            console.print("No data to export", style="bold yellow")
            
    except Exception as e:
        console.print(f"Error: {e}", style="bold red")
        sys.exit(1)


# Config Commands Group
@cli.group()
def config():
    """Commands for managing application configuration."""
    pass


@config.command("contact")
@click.option("--whatsapp", help="Set WhatsApp contact number")
@click.option("--email", help="Set email contact address")
@click.option("--show", is_flag=True, help="Show current contact info")
@click.option("--config-file", help=f"Path to config file (default: {DEFAULT_CONFIG_FILE})")
def manage_contact(whatsapp: Optional[str], email: Optional[str], 
                  show: bool, config_file: Optional[str]):
    """Manage contact information shown in the Excel file."""
    # If no action specified, default to showing current info
    if not any([whatsapp, email, show]):
        show = True
    
    # Get current contact info
    contact_info = get_contact_info(config_file)
    
    # Update contact info if requested
    if whatsapp or email:
        contact_info = update_contact_info(whatsapp, email, config_file)
        console.print("Contact information updated:", style="bold green")
    
    # Show current contact info
    if show or whatsapp or email:
        table = Table(title="Contact Information")
        table.add_column("Type", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("WhatsApp", contact_info["whatsapp"])
        table.add_row("Email", contact_info["email"])
        
        console.print(table)


# Auth Commands Group
@cli.group()
def auth():
    """Commands for authentication management."""
    pass


@auth.command("cookie")
@click.option("--set", "set_cookie", is_flag=True, help="Set cookie value")
@click.option("--get", "get_cookie", is_flag=True, help="Get cookie value")
@click.option("--delete", "delete_cookie", is_flag=True, help="Delete cookie file")
@click.option("--file", "-f", default="cookie.json", help="Cookie file path")
def manage_cookie(set_cookie: bool, get_cookie: bool, delete_cookie: bool, file: str):
    """Manage cookies for API authentication."""
    if delete_cookie:
        if os.path.exists(file):
            os.remove(file)
            console.print(f"Cookie file deleted: {file}", style="bold green")
        else:
            console.print(f"Cookie file not found: {file}", style="bold yellow")
        return
    
    if get_cookie:
        if os.path.exists(file):
            try:
                with open(file, "r") as f:
                    cookies = json.load(f)
                console.print(json.dumps(cookies, indent=2), style="bold cyan")
            except json.JSONDecodeError:
                console.print(f"Invalid JSON in cookie file: {file}", style="bold red")
        else:
            console.print(f"Cookie file not found: {file}", style="bold yellow")
        return
    
    if set_cookie:
        console.print("Enter cookies in JSON format (e.g., {\"key\": \"value\"}):", style="bold cyan")
        cookie_json = click.prompt("", type=str)
        
        try:
            cookies = json.loads(cookie_json)
            with open(file, "w") as f:
                json.dump(cookies, f, indent=2)
            console.print(f"Cookies saved to {file}", style="bold green")
        except json.JSONDecodeError:
            console.print("Invalid JSON format", style="bold red")
        return
    
    # If no option is specified, show help
    ctx = click.get_current_context()
    click.echo(ctx.get_help())


# For backward compatibility, add the cookie command to the main group as well
@cli.command("cookie")
@click.option("--set", "set_cookie", is_flag=True, help="Set cookie value")
@click.option("--get", "get_cookie", is_flag=True, help="Get cookie value")
@click.option("--delete", "delete_cookie", is_flag=True, help="Delete cookie file")
@click.option("--file", "-f", default="cookie.json", help="Cookie file path")
def cookie_command(set_cookie: bool, get_cookie: bool, delete_cookie: bool, file: str):
    """Manage cookies for API authentication."""
    # Call the auth cookie function
    ctx = click.get_current_context()
    ctx.invoke(manage_cookie, set_cookie=set_cookie, get_cookie=get_cookie, 
              delete_cookie=delete_cookie, file=file)


@cli.command("info")
@click.option("--config-file", help=f"Path to config file (default: {DEFAULT_CONFIG_FILE})")
def show_info(config_file: Optional[str]):
    """Display information about the API and tool."""
    # Get contact info
    contact_info = get_contact_info(config_file)
    
    table = Table(title="Apotek Tools Information")
    
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("API Endpoint", "https://auliafarma.co.id/api/drugs")
    table.add_row("Current Date", get_current_date())
    table.add_row("Cookie File", "cookie.json")
    table.add_row("Config File", config_file or DEFAULT_CONFIG_FILE)
    table.add_row("WhatsApp Contact", contact_info["whatsapp"])
    table.add_row("Email Contact", contact_info["email"])
    
    console.print(table)


def main():
    """Main entry point for the CLI."""
    try:
        cli()
    except Exception as e:
        console.print(f"Unexpected error: {e}", style="bold red")
        sys.exit(1)


if __name__ == "__main__":
    main()
