#!/usr/bin/env bash
# Quick installer for JobSpy with Internshala support

echo "🚀 Installing JobSpy with Internshala..."

# Install dependencies
pip3 install -e .

# Quick test
python3 -c "from jobspy import scrape_jobs; print('✅ Installation successful!')"

echo ""
echo "📋 Quick start:"
echo "   python3 jobspy_runner.py --preset tech_india"
echo ""
echo "📖 See SETUP.md for full documentation"
