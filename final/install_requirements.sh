#!/bin/bash

# Script to install all requirements from client and server requirements.txt files
# Checks if virtual environment is activated, activates if needed, then installs requirements

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Retail Intelligence Platform - Requirements Installer${NC}"
echo "============================================================"

# Function to check if venv is activated
is_venv_activated() {
    if [ -n "$VIRTUAL_ENV" ]; then
        return 0  # True - venv is activated
    else
        return 1  # False - venv is not activated
    fi
}

# Function to activate virtual environment
activate_venv() {
    local venv_path=""
    
    # Check for Linux/Mac venv (bin/activate)
    if [ -f "venv/bin/activate" ]; then
        venv_path="venv/bin/activate"
        echo -e "${YELLOW}Found Linux/Mac virtual environment${NC}"
    # Check for Windows venv (Scripts/activate)
    elif [ -f "venv/Scripts/activate" ]; then
        venv_path="venv/Scripts/activate"
        echo -e "${YELLOW}Found Windows virtual environment${NC}"
    else
        echo -e "${RED}Error: Virtual environment not found!${NC}"
        echo "Please create a virtual environment first:"
        echo "  Linux/Mac/WSL: python3 -m venv venv"
        echo "  Windows: python -m venv venv"
        exit 1
    fi
    
    echo -e "${YELLOW}Activating virtual environment...${NC}"
    source "$venv_path"
    
    if is_venv_activated; then
        echo -e "${GREEN}Virtual environment activated successfully!${NC}"
        echo -e "Python: $(which python)"
        echo -e "Pip: $(which pip)"
    else
        echo -e "${RED}Error: Failed to activate virtual environment${NC}"
        exit 1
    fi
}

# Check if virtual environment is already activated
if is_venv_activated; then
    echo -e "${GREEN}Virtual environment is already activated!${NC}"
    echo -e "Python: $(which python)"
    echo -e "Pip: $(which pip)"
else
    echo -e "${YELLOW}Virtual environment is not activated.${NC}"
    activate_venv
fi

echo ""
echo "============================================================"
echo -e "${GREEN}Installing requirements...${NC}"
echo "============================================================"

# Check if requirements files exist
if [ ! -f "client/requirements.txt" ]; then
    echo -e "${RED}Error: client/requirements.txt not found!${NC}"
    exit 1
fi

if [ ! -f "server/requirements.txt" ]; then
    echo -e "${RED}Error: server/requirements.txt not found!${NC}"
    exit 1
fi

# Upgrade pip first
echo -e "${YELLOW}Upgrading pip...${NC}"
python -m pip install --upgrade pip

# Install client requirements
echo ""
echo -e "${GREEN}Installing client requirements...${NC}"
echo "------------------------------------------------------------"
pip install -r client/requirements.txt

# Install server requirements
echo ""
echo -e "${GREEN}Installing server requirements...${NC}"
echo "------------------------------------------------------------"
pip install -r server/requirements.txt

echo ""
echo "============================================================"
echo -e "${GREEN}All requirements installed successfully!${NC}"
echo "============================================================"
echo ""
echo "Installed packages:"
pip list | tail -n +3

echo ""
echo -e "${GREEN}Setup complete! You can now run the application.${NC}"

