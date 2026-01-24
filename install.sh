#!/bin/bash

# GRC Policy Generator - Installation Script
# Checks prerequisites and sets up the environment

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  GRC Policy & Compliance Generator - Installation           ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to compare version numbers
version_ge() {
    [ "$(printf '%s\n' "$1" "$2" | sort -V | head -n1)" = "$2" ]
}

echo -e "${YELLOW}[1/4] Checking Python installation...${NC}"

# Check if Python 3 is installed
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓ Python 3 found: v${PYTHON_VERSION}${NC}"

    # Check if version is 3.7 or higher
    REQUIRED_VERSION="3.7.0"
    if version_ge "$PYTHON_VERSION" "$REQUIRED_VERSION"; then
        echo -e "${GREEN}✓ Python version is sufficient (≥3.7.0)${NC}"
    else
        echo -e "${RED}✗ Python version too old. Required: ≥3.7.0, Found: ${PYTHON_VERSION}${NC}"
        echo ""
        echo "Would you like to see instructions for upgrading Python? [y/N]"
        read -r response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            echo ""
            echo "To upgrade Python:"
            echo "  Ubuntu/Debian: sudo apt update && sudo apt install python3.9"
            echo "  macOS: brew install python@3.9"
            echo "  Or visit: https://www.python.org/downloads/"
        fi
        exit 1
    fi
else
    echo -e "${RED}✗ Python 3 not found${NC}"
    echo ""
    echo "Python 3.7+ is required to run this tool."
    echo ""
    echo "Would you like to install Python 3? [y/N]"
    read -r response

    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        if command_exists apt-get; then
            echo "Installing Python 3 via apt..."
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip
        elif command_exists yum; then
            echo "Installing Python 3 via yum..."
            sudo yum install -y python3 python3-pip
        elif command_exists brew; then
            echo "Installing Python 3 via Homebrew..."
            brew install python3
        else
            echo -e "${RED}Cannot auto-install. Please install Python 3.7+ manually.${NC}"
            echo "Visit: https://www.python.org/downloads/"
            exit 1
        fi
    else
        echo "Installation cancelled. Please install Python 3.7+ and try again."
        exit 1
    fi
fi

echo ""
echo -e "${YELLOW}[2/4] Checking required Python modules...${NC}"

# Check for required standard library modules
REQUIRED_MODULES=("os" "json" "csv" "datetime" "dataclasses" "typing")
MISSING_MODULES=()

for module in "${REQUIRED_MODULES[@]}"; do
    if python3 -c "import $module" 2>/dev/null; then
        echo -e "${GREEN}✓ ${module}${NC}"
    else
        echo -e "${RED}✗ ${module}${NC}"
        MISSING_MODULES+=("$module")
    fi
done

if [ ${#MISSING_MODULES[@]} -gt 0 ]; then
    echo -e "${RED}Missing modules: ${MISSING_MODULES[*]}${NC}"
    echo "These are standard library modules. Your Python installation may be incomplete."
    exit 1
else
    echo -e "${GREEN}✓ All required modules available${NC}"
fi

echo ""
echo -e "${YELLOW}[3/4] Checking file permissions...${NC}"

# Check if main script is readable
if [ -r "grc_policy_generator.py" ]; then
    echo -e "${GREEN}✓ grc_policy_generator.py is readable${NC}"
else
    echo -e "${RED}✗ Cannot read grc_policy_generator.py${NC}"
    exit 1
fi

# Check if we can create output directory
if mkdir -p generated_policies 2>/dev/null; then
    echo -e "${GREEN}✓ Can create output directories${NC}"
    rmdir generated_policies 2>/dev/null || true
else
    echo -e "${RED}✗ Cannot create output directories${NC}"
    echo "Check write permissions in current directory"
    exit 1
fi

# Make script executable if not already
if [ ! -x "grc_policy_generator.py" ]; then
    chmod +x grc_policy_generator.py 2>/dev/null || true
fi

echo ""
echo -e "${YELLOW}[4/4] Verifying installation...${NC}"

# Test import of main modules
if python3 -c "from compliance_engine import INDUSTRY_PRESETS, RiskScorer" 2>/dev/null; then
    echo -e "${GREEN}✓ compliance_engine.py imports successfully${NC}"
else
    echo -e "${RED}✗ Error importing compliance_engine.py${NC}"
    exit 1
fi

if python3 -c "from gap_analyzer import GapAnalyzer" 2>/dev/null; then
    echo -e "${GREEN}✓ gap_analyzer.py imports successfully${NC}"
else
    echo -e "${RED}✗ Error importing gap_analyzer.py${NC}"
    exit 1
fi

if python3 -c "from output_generator import OutputGenerator" 2>/dev/null; then
    echo -e "${GREEN}✓ output_generator.py imports successfully${NC}"
else
    echo -e "${RED}✗ Error importing output_generator.py${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✓ Installation Complete!                                    ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}To run the tool:${NC}"
echo -e "  ${YELLOW}python3 grc_policy_generator.py${NC}"
echo ""
echo -e "${BLUE}For help:${NC}"
echo -e "  See README.md for usage instructions"
echo ""
echo -e "${BLUE}Output location:${NC}"
echo -e "  Generated policies will be saved in: ${YELLOW}generated_policies/YYYY-MM-DD_HHMMSS/${NC}"
echo ""
