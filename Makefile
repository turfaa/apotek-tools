.PHONY: setup clean test venv install run help

help:
	@echo "Apotek Tools Makefile"
	@echo "-----------------------"
	@echo "setup     - Set up the development environment using uv"
	@echo "venv      - Create a virtual environment with uv"
	@echo "install   - Install the package in development mode using uv"
	@echo "run       - Run the CLI with all arguments passed using uv"
	@echo "clean     - Remove build artifacts and virtual environments"
	@echo "test      - Run tests using uv (when implemented)"

setup: venv install
	@echo "Development environment setup complete!"

venv:
	@command -v uv >/dev/null 2>&1 || { echo "Please install uv first: curl -LsSf https://astral.sh/uv/install.sh | sh"; exit 1; }
	@echo "Creating virtual environment with uv..."
	@uv venv

install:
	@echo "Installing in development mode using uv..."
	@uv pip install -e .

run:
	@uv run apotek_tools $(filter-out $@,$(MAKECMDGOALS))

clean:
	@echo "Cleaning build artifacts..."
	@rm -rf build/ dist/ *.egg-info/ __pycache__/ .pytest_cache/ .coverage .uv/ .venv/
	@find . -name "__pycache__" -type d -exec rm -rf {} +
	@find . -name "*.pyc" -delete
	@find . -name "*.pyo" -delete
	@find . -name "*.pyd" -delete
	@find . -name ".*.swp" -delete
	@find . -name ".coverage.*" -delete
	@echo "Done cleaning!"

test:
	@echo "Running tests using uv (not implemented yet)..."
	@echo "You can implement tests using uv run pytest in the future."

# Pass arguments to the run target
%:
	@: 