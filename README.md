# Apotek Tools

A comprehensive CLI tool for interacting with the Apotek Aulia Farma API. This tool is designed to handle various API operations including fetching price lists, with plans to support additional functionality in the future.

## Features

### Current Features
- Fetch drug price list from Apotek Aulia Farma API
- Generate formatted Excel file with price information


## Installation

### Prerequisites

- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) - Fast, reliable Python package management

### Setup

1. Install uv if you don't have it yet:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/apotek-tools.git
   cd apotek-tools
   ```

3. Create a virtual environment and install the package:
   ```bash
   uv venv
   source .venv/bin/activate  # On Linux/macOS
   # or
   .\.venv\Scripts\activate   # On Windows
   uv pip install -e .
   ```

   Alternatively, use the provided setup script:
   ```bash
   ./setup_uv.sh
   ```

### Setup with Makefile (easiest)

If you have `make` installed, you can use the Makefile for an easy setup:

```bash
make setup
```

## Usage

The CLI is structured using command groups to organize functionality by area:

```
uv run apotek_tools [command-group] [command] [options]
```

### Available Command Groups

- `pricelist`: Commands for managing drug price lists
- `auth`: Commands for authentication management
- `config`: Commands for managing application configuration

### Available Commands

#### Global Commands

- `fetch`: Shortcut for `pricelist fetch` (for backward compatibility)
- `cookie`: Shortcut for `auth cookie` (for backward compatibility)
- `info`: Display information about the API and tool

#### Price List Commands

```bash
uv run apotek_tools pricelist fetch [options]
```

This will:
1. Fetch the drug list from the API
2. Process the data
3. Display a preview of the data
4. Ask for confirmation to generate the Excel file
5. Create an Excel file with price information

Options:
- `--cookie, -c`: Cookie value to use for authentication (JSON format)
- `--cookie-file`: Path to cookie file (default: cookie.json)
- `--output, -o`: Output file path
- `--preview/--no-preview`: Preview the data before generating Excel (default: --preview)
- `--preview-limit`: Number of items to preview (default: 10)
- `--config-file`: Path to config file (default: apotek_config.json)

#### Authentication Commands

```bash
uv run apotek_tools auth cookie [options]
```

Options:
- `--set`: Set cookie value
- `--get`: Get current cookie value
- `--delete`: Delete cookie file
- `--file, -f`: Cookie file path (default: cookie.json)

#### Configuration Commands

```bash
uv run apotek_tools config contact [options]
```

Options:
- `--whatsapp`: Set WhatsApp contact number
- `--email`: Set email contact address
- `--show`: Show current contact info (default behavior if no options)
- `--config-file`: Path to config file (default: apotek_config.json)

Example:
```bash
# Update WhatsApp number
uv run apotek_tools config contact --whatsapp="+6281223556554"

# Update email
uv run apotek_tools config contact --email="new.email@auliafarma.co.id"

# Show current settings
uv run apotek_tools config contact --show
```

### Running with make

You can use the Makefile to run commands easily:

```bash
# Run a command
make run fetch

# With options
make run fetch --no-preview

# Get help
make run --help

# Configure contact info
make run config contact --whatsapp="+6281223556554"
```

### Getting Help

For general help:
```bash
uv run apotek_tools --help
```

For help with a command group:
```bash
uv run apotek_tools [command-group] --help
```

For help with a specific command:
```bash
uv run apotek_tools [command-group] [command] --help
```

## Configuration

### Contact Information

Contact information is stored in `apotek_config.json` and includes:
- WhatsApp number (default: +6281223556554)
- Email address (default: kontak@auliafarma.co.id)

This contact information is included in generated Excel files.

### Cookie Format

The cookie file should be a JSON file with key-value pairs:

```json
{
  "cookie_name": "cookie_value",
  "session_id": "your_session_id"
}
```

## Excel Output Format

The generated Excel file for price lists will have the following format:

```
Daftar Harga Apotek Aulia Farma per [current date]

Kontak WhatsApp: +6281223556554
Email: kontak@auliafarma.co.id

Nama Obat | Harga Diskon | Sisa Stok
--------------------------------------
Drug 1    | Rp xxx       | xx Pcs
Drug 2    | Rp xxx       | xx Pcs
...
```

## Development

For a comprehensive guide on using uv for development, see [UV_DEVELOPMENT.md](UV_DEVELOPMENT.md).

### Project Structure

The codebase is structured to make it easy to add new functionality:

- `apotek_tools/api.py`: Core API interaction module (use this for new API endpoints)
- `apotek_tools/fetcher.py`: Data processing for drug lists
- `apotek_tools/excel_generator.py`: Excel file generation
- `apotek_tools/cli.py`: Command-line interface
- `apotek_tools/config.py`: Configuration management

### Adding New Commands

To add a new command to the CLI, extend the appropriate Click group in `cli.py`. For example:

```python
# Add a command to an existing group
@pricelist.command("search")
@click.argument("query")
def search_drugs(query):
    """Search for drugs by name."""
    # Implementation goes here
    pass

# Create a new command group
@cli.group()
def inventory():
    """Commands for managing inventory."""
    pass

# Add a command to the new group
@inventory.command("check")
@click.argument("drug_code")
def check_inventory(drug_code):
    """Check the inventory for a specific drug."""
    # Implementation goes here
    pass
```

### Using uv for Development

uv provides several commands that make Python development faster:

```bash
# Create a virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate  # Linux/macOS
.\.venv\Scripts\activate   # Windows

# Install dependencies from pyproject.toml
uv pip install -e .

# Install specific packages
uv pip install requests pandas

# Run a Python script directly (no need to activate venv)
uv run python path/to/script.py

# Run the CLI
uv run -m apotek_tools [command]

# Run pip commands with uv's speed improvements
uv pip list
uv pip freeze
```

### Makefile Commands

The project includes a Makefile with useful commands for development:

```
make help            # Show available commands
make setup           # Set up development environment with uv
make venv            # Create a virtual environment with uv
make install         # Install the package in development mode using uv
make run [args]      # Run the CLI with arguments using uv
make clean           # Clean build artifacts
make test            # Run tests using uv (when implemented)
```

## License

MIT
