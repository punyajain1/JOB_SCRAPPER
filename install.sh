#!/bin/bash

# Job Scraper + JobSpy Installation Script
# This script installs all requirements in one go

echo "🚀 Job Scraper Installation Script"
echo "===================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Found: Python $python_version"

# Check if Python 3.10+ is installed
required_version="3.10"
if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.10 or higher is required!"
    echo "   Your version: $python_version"
    exit 1
fi

echo "✅ Python version OK"
echo ""

# Upgrade pip
echo "📦 Upgrading pip..."
python3 -m pip install --upgrade pip

echo ""

# Install all requirements
echo "📥 Installing all dependencies from requirements.txt..."
echo "   This includes:"
echo "   - Job scraper dependencies"
echo "   - JobSpy library dependencies"
echo "   - SSL/TLS libraries"
echo "   - Data processing libraries"
echo ""

pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Installation Complete!"
    echo ""
    echo "📝 Next Steps:"
    echo "   1. Copy example environment file:"
    echo "      cp .env.example.btech .env"
    echo ""
    echo "   2. Edit .env file with your settings"
    echo ""
    echo "   3. Run the scraper:"
    echo "      python3 job_scraper_webhook.py"
    echo ""
    echo "🎉 Happy job hunting!"
else
    echo ""
    echo "❌ Installation failed! Please check the error messages above."
    exit 1
fi
