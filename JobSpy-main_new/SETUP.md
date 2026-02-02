# JobSpy with Internshala Support - n8n Ready

Job scraper with support for **LinkedIn, Indeed, Glassdoor, Google, ZipRecruiter, Internshala, Bayt, Naukri, and BDJobs**.

## Quick Setup

1. **Install dependencies:**
```bash
pip install -e .
```

2. **Test it works:**
```bash
python3 -c "from jobspy import scrape_jobs; print('✅ Ready!')"
```

## Usage

### Command Line (Recommended for n8n)

```bash
# Use built-in presets
python3 jobspy_runner.py --preset tech_india
python3 jobspy_runner.py --preset internships
python3 jobspy_runner.py --preset remote_work

# Custom search
python3 jobspy_runner.py --sites internshala indeed --search "python developer" --location "Delhi" --results 20

# See all options
python3 jobspy_runner.py --help
```

### Python Script

```python
from jobspy import scrape_jobs

jobs = scrape_jobs(
    site_name=["internshala", "indeed", "linkedin", "naukri"],
    search_term="software engineer",
    internshala_search_term="software development",  # Internshala-specific
    location="Bangalore",
    results_wanted=25,
    job_type="fulltime",
    hours_old=168  # Last week
)

# Save results
jobs.to_csv("jobs.csv", index=False)
print(f"Found {len(jobs)} jobs")
```

## Available Presets

- `tech_india` - Tech jobs in India (Internshala, Naukri, Indeed)
- `tech_global` - Global tech jobs (LinkedIn, Indeed, Glassdoor, Google)
- `data_science` - Data science positions
- `internships` - Internships from Internshala
- `remote_work` - Remote positions only
- `full_spectrum` - All Indian job sites

## Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `site_name` | Job sites to scrape | `["internshala", "indeed"]` |
| `search_term` | General search term | `"python developer"` |
| `internshala_search_term` | Internshala-specific term | `"python programming"` |
| `location` | Location to search | `"Delhi"` or `"San Francisco, CA"` |
| `results_wanted` | Results per site | `20` |
| `job_type` | Job type filter | `"fulltime"`, `"internship"`, `"parttime"` |
| `is_remote` | Remote jobs only | `True` / `False` |
| `hours_old` | Posted within X hours | `72` (3 days) |
| `country_indeed` | Country for Indeed | `"India"`, `"USA"` |

## For n8n Integration

### Execute Command Node
```json
{
  "command": "python3 jobspy_runner.py --preset tech_india --results 30 --output jobs.csv"
}
```

### Python Function Node
```python
from jobspy import scrape_jobs

jobs = scrape_jobs(
    site_name=["internshala", "indeed"],
    search_term="{{ $json.search_term }}",
    location="{{ $json.location }}",
    results_wanted=int("{{ $json.results }}")
)

return jobs.to_dict('records')
```

## Output Format

CSV/DataFrame with columns:
- `site` - Source job board
- `title` - Job title
- `company` - Company name
- `location` - Job location
- `job_type` - Employment type
- `min_amount`, `max_amount` - Salary range
- `currency`, `interval` - Salary details
- `job_url` - Direct link
- `description` - Job description
- `date_posted` - Posting date

## Troubleshooting

- **Import Error**: Run `pip install -e .` first
- **No Results**: Try different search terms or locations
- **Rate Limiting**: Add delays or use fewer results per site
- **Network Issues**: Check internet connection or use proxies

## Requirements

- Python 3.10+
- Internet connection
- Dependencies: pandas, requests, beautifulsoup4, pydantic (auto-installed)

---

**Ready for your n8n workflows!** 🚀