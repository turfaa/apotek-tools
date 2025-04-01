#!/bin/sh
# Setup script for apotek-tools development environment using uv

# Check if uv is installed
if ! command -v uv &> /dev/null; then
  echo "uv is not installed. Please install it first:"
  echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
  exit 1
fi

# Create virtual environment
echo "Creating virtual environment with uv..."
uv venv

# Install in development mode using uv
echo "Installing package in development mode using uv..."
uv pip install -e .

echo "Development environment setup successfully!"
echo "To use the tool, you can either:"
echo "  1. Activate the virtual environment and run normally:"
echo "     source .venv/bin/activate"
echo "     python -m apotek_tools"
echo "  or"
echo "  2. Run directly with uv (no activation needed):"
echo "     uv run apotek_tools"
echo ""
echo "For development, you can use these commands:"
echo "  uv run python -m apotek_tools  # Run the module"
echo "  uv add <package>               # Install a new dependency" 