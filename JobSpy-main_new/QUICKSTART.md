# Quick Start - JobSpy with Internshala

## 1. Installation (One Time)

```bash
./install.sh
```

Or manually:
```bash
pip3 install -e .
```

## 2. Usage Examples

### Command Line
```bash
# Indian tech jobs
python3 jobspy_runner.py --preset tech_india --results 30

# Internships only
python3 jobspy_runner.py --preset internships --results 50

# Custom search
python3 jobspy_runner.py \
  --sites internshala indeed linkedin \
  --search "python developer" \
  --location "Bangalore" \
  --results 25
```

### Python Script
```python
from jobspy import scrape_jobs

jobs = scrape_jobs(
    site_name=["internshala", "indeed", "naukri"],
    search_term="software engineer",
    location="Delhi",
    results_wanted=30
)

jobs.to_csv("output.csv", index=False)
```

## 3. For n8n Workflows

**Execute Command Node:**
```json
{
  "command": "cd /path/to/JobSpy-main && python3 jobspy_runner.py --preset tech_india --output {{$json.filename}}.csv"
}
```

**Read CSV Node:**
```json
{
  "filePath": "{{$json.filename}}.csv"
}
```

## Available Sites
✅ Internshala | ✅ Indeed | ✅ LinkedIn | ✅ Glassdoor  
✅ Google Jobs | ✅ ZipRecruiter | ✅ Naukri | ✅ Bayt | ✅ BDJobs

## Project Structure
```
JobSpy-main/
├── jobspy/              # Core scraping library
├── jobspy_runner.py     # Ready-to-use CLI tool
├── pyproject.toml       # Dependencies
├── install.sh           # Quick installer
└── SETUP.md            # Full documentation
```

**That's it!** Share this folder and run `./install.sh` on any machine.