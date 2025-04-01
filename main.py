#!/usr/bin/env python3
"""Main entry point for Apotek Tools CLI.

This file allows running the program in these ways:
1. With uv: `uv run python main.py`
2. With uv directly: `uv run apotek_tools`
3. As a module: `python -m apotek_tools`
4. As an installed script: `apotek-tools`
"""

from apotek_tools.cli import main

if __name__ == "__main__":
    # Print helpful message if run directly
    print("Running Apotek Tools CLI...")
    main()
