#!/bin/bash

# Personal Finance App - Startup Script
# Run this with: ./start.sh

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting Personal Finance App...${NC}"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Add ~/bin to PATH for Poetry
export PATH="$HOME/bin:$PATH"

# Force Poetry to use Python 3.9
export POETRY_PYTHON=/opt/homebrew/bin/python3.9

# Check if Poetry is available
if ! command -v poetry &> /dev/null; then
    echo -e "${YELLOW}Error: Poetry is not installed!${NC}"
    echo -e "${YELLOW}Install Poetry: brew install poetry${NC}"
    exit 1
fi

# Ensure Poetry is using Python 3.9
echo -e "${BLUE}Setting up Python 3.9 environment...${NC}"
poetry env use 3.9 2>/dev/null || poetry env use /opt/homebrew/bin/python3.9

# Check if dependencies are installed, install if needed
echo -e "${BLUE}Checking dependencies...${NC}"
if ! poetry run python -c "import flask" 2>/dev/null; then
    echo -e "${YELLOW}Installing dependencies (first time setup)...${NC}"
    poetry install --no-root
fi

# Wait a moment then open Chrome
(sleep 2 && open -a "Google Chrome" "http://localhost:5001") &

# Start the Flask app using Poetry
echo -e "${GREEN}App running at: http://localhost:5001${NC}"
echo -e "${GREEN}Press Ctrl+C to stop${NC}"
echo ""

poetry run python app.py
