#!/bin/bash
# Aspect-Pulse Website - Installation Verification Script

echo "=================================================="
echo "Aspect-Pulse Website - Installation Checker"
echo "=================================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counter
PASSED=0
FAILED=0

# Check Python
echo "🔍 Checking Python installation..."
if command -v python3 &> /dev/null; then
    VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓${NC} Python $VERSION found"
    ((PASSED++))
else
    echo -e "${RED}✗${NC} Python not found"
    ((FAILED++))
fi

# Check Flask
echo ""
echo "🔍 Checking Flask installation..."
if python3 -c "import flask" 2>/dev/null; then
    VERSION=$(python3 -c "import flask; print(flask.__version__)")
    echo -e "${GREEN}✓${NC} Flask $VERSION found"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠${NC} Flask not found (run: pip install flask)"
    ((FAILED++))
fi

# Check project files
echo ""
echo "🔍 Checking project structure..."

FILES=(
    "web/app.py"
    "web/templates/index.html"
    "web/templates/dashboard.html"
    "web/templates/about.html"
    "web/templates/404.html"
    "web/templates/500.html"
    "web/static/css/style.css"
    "web/static/js/main.js"
    "web/static/js/dashboard.js"
    "web/README.md"
    "web/CONFIG.md"
    "QUICKSTART.md"
    "WEBSITE_SUMMARY.md"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $file (MISSING)"
        ((FAILED++))
    fi
done

# Check NLP dependencies (optional)
echo ""
echo "🔍 Checking NLP dependencies (optional)..."

NLP_PACKAGES=("nltk" "spacy" "transformers")
for package in "${NLP_PACKAGES[@]}"; do
    if python3 -c "import $package" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $package found"
        ((PASSED++))
    else
        echo -e "${YELLOW}⚠${NC} $package not found"
    fi
done

# Summary
echo ""
echo "=================================================="
echo "Summary"
echo "=================================================="
echo -e "${GREEN}Passed:${NC} $PASSED"
echo -e "${RED}Failed/Missing:${NC} $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    echo ""
    echo "Ready to start? Run:"
    echo "  cd web"
    echo "  python app.py"
    echo ""
    echo "Then open: http://localhost:5000"
else
    echo -e "${YELLOW}⚠ Some items missing or need installation${NC}"
    echo ""
    echo "To fix:"
    echo "1. Install Flask: pip install flask"
    echo "2. Install requirements: pip install -r requirements.txt"
    echo "3. Run this script again"
fi

echo ""
echo "=================================================="
