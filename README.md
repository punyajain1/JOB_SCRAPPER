# 🔍 Job Scraper Automation

An automated job scraping tool that collects job listings from multiple job boards and sends them to an n8n webhook for further automation (like sending to Google Sheets, email notifications, etc.).

## 🔄 Two Automation Modes

This project supports **two types of automation workflows**:

### 1. 🤖 AI-Powered Job Matching (Premium)
> ⚠️ **Note:** Due to AI API costs, this mode is not included in the free version.

- Uses AI (Gemini) to analyze your resume skills
- Matches job descriptions & requirements with your profile
- Scores and ranks jobs by compatibility
- Returns only the **most favorable jobs** for you
- Create CSV file of them and Sends results as **CSV file to your email**
- Best for: Quality over quantity

### 2. 📧 Basic Automation (Free) ✅ **Currently Active**
- Fetches jobs based on your search parameters
- Collects all matching jobs from multiple sites
- Sends results as **CSV file to your email**
- No AI filtering - you get all results
- Best for: Casting a wide net, manual review

**Current workflow:** Jobs are scraped → Sent to n8n webhook → Converted to CSV → Emailed to you

---

## ✨ Features

- **Multi-Site Scraping**: Scrapes jobs from 8 different job boards simultaneously
- **India-Focused**: Includes India-specific sites like Naukri and Internshala
- **Configurable**: Easy configuration via `.env` file
- **n8n Integration**: Sends scraped jobs directly to n8n webhook
- **Local Backup**: Saves jobs to JSON file as backup
- **Fresher/Intern Friendly**: Optimized for entry-level job searches

## 📋 Supported Job Sites

| Site | Region | Best For | Notes |
|------|--------|----------|-------|
| **Indeed** | Global | All jobs | Best scraper, no rate limiting |
| **LinkedIn** | Global | Professional jobs | Rate limits quickly, use proxies for best results |
| **Glassdoor** | Global | Company reviews + jobs | May block requests |
| **Google Jobs** | Global | Aggregated listings | Requires specific search syntax |
| **Naukri** | 🇮🇳 India | IT/Software jobs | Best for India tech jobs |
| **Internshala** | 🇮🇳 India | Internships | Best for freshers/interns |
| **ZipRecruiter** | 🇺🇸🇨🇦 US/Canada | All jobs | US/Canada only |
| **Bayt** | 🌍 Middle East | All jobs | Only uses search term |

## 🚀 Quick Start

### Option 1: Automated Installation (Recommended)

```bash
# Run the installation script
./install.sh
```

This script will:
- ✅ Check Python version (requires 3.10+)
- ✅ Upgrade pip
- ✅ Install **all dependencies** (Job scraper + JobSpy + SSL libraries)
- ✅ Show you next steps

### Option 2: Manual Installation

```bash
pip install -r requirements.txt
```

This single command installs **all dependencies** including:
- Job scraper requirements (requests, dotenv, pandas)
- JobSpy library requirements (beautifulsoup4, tls-client, pydantic)
- SSL/TLS handling (certifi, urllib3)
- Data processing (numpy, regex)

No need to install anything else separately!

### 2. Configure Environment

Copy the example file and edit it:
```bash
cp .env.example.btech .env   # For B.Tech/Software jobs
# OR
cp .env.example.bcom .env    # For B.Com/Commerce jobs
```

### 3. Edit `.env` File

Set your webhook URL and customize search parameters (see Configuration Guide below).

### 4. Run the Scraper

```bash
python3 job_scraper_webhook.py
```

Or with command line arguments:
```bash
python3 job_scraper_webhook.py "software developer intern" "Bangalore"
```

---

## ⚙️ Complete Configuration Guide

### 📁 `.env` File Structure

```env
# ===========================================
# REQUIRED SETTINGS
# ===========================================
WEBHOOK_URL=https://your-n8n-instance.com/webhook/job-scraper

# ===========================================
# SEARCH PARAMETERS
# ===========================================
SEARCH_TERM=software developer intern
LOCATION=Bangalore
```

---

### 🔑 All Configuration Options

#### **WEBHOOK_URL** (Required)
Your n8n webhook URL to receive the scraped jobs.
```env
WEBHOOK_URL=https://your-n8n.app.n8n.cloud/webhook/job-scraper
```

---

#### **SEARCH_TERM** (Required)
The main job search query. Used by most sites.

```env
# Simple search
SEARCH_TERM=software developer intern

# With exact match (quotes)
SEARCH_TERM="python developer" intern

# Exclude words (minus sign)
SEARCH_TERM=software developer -senior -lead -manager

# Complex Indeed query (Indeed searches description too)
SEARCH_TERM="software intern" python (react OR angular) 2026 -senior
```

**Tips for better Indeed results:**
- Use `"quotes"` for exact phrase match
- Use `-word` to exclude words
- Use `(word1 OR word2)` for alternatives
- Indeed searches job descriptions too, so be specific

---

#### **LOCATION**
Where to search for jobs. Different sites handle this differently:

```env
# City only (works best for Naukri)
LOCATION=Bangalore

# City + Country
LOCATION=Mumbai, India

# Country only
LOCATION=India

# Remote jobs
LOCATION=Remote
```

**Per-site behavior:**
| Site | How it uses LOCATION |
|------|---------------------|
| LinkedIn | Searches globally, very flexible |
| Indeed/Glassdoor | Uses with DEFAULT_COUNTRY |
| Naukri | City names work best |
| Internshala | ❌ Doesn't use location |
| Google | ❌ Uses GOOGLE_SEARCH_TERM instead |

---

#### **GOOGLE_SEARCH_TERM**
Google Jobs requires a specific search syntax. Search on Google Jobs in your browser, apply filters, then copy the exact search text.

```env
# Include location in the search term
GOOGLE_SEARCH_TERM=software developer intern jobs in Bangalore, India

# With filters
GOOGLE_SEARCH_TERM=python developer internship in Mumbai
```

---

#### **JOB_SITES**
Comma-separated list of sites to scrape.

```env
# All India sites
JOB_SITES=indeed,linkedin,glassdoor,naukri,internshala

# Only Indian job boards
JOB_SITES=naukri,internshala

# US/Canada search
JOB_SITES=indeed,linkedin,glassdoor,google,zip_recruiter

# Middle East
JOB_SITES=indeed,linkedin,bayt
```

---

#### **RESULTS_WANTED**
Number of jobs to fetch per site. Max is ~1000.

```env
RESULTS_WANTED=15    # 15 jobs per site
RESULTS_WANTED=50    # 50 jobs per site (slower)
RESULTS_WANTED=100   # 100 jobs per site (much slower)
```

---

#### **HOURS_OLD**
Only fetch jobs posted within the last X hours.

```env
HOURS_OLD=24     # Last 24 hours (1 day)
HOURS_OLD=72     # Last 72 hours (3 days)
HOURS_OLD=168    # Last 168 hours (1 week)
```

**⚠️ Note:** ZipRecruiter and Glassdoor round up to the next day.

---

#### **DEFAULT_COUNTRY**
Country for Indeed & Glassdoor. Use exact spelling:

```env
DEFAULT_COUNTRY=India
DEFAULT_COUNTRY=USA
DEFAULT_COUNTRY=UK
DEFAULT_COUNTRY=Canada
DEFAULT_COUNTRY=Germany
DEFAULT_COUNTRY=Australia
```

<details>
<summary>📋 All Supported Countries (click to expand)</summary>

Argentina, Australia, Austria, Bahrain, Bangladesh, Belgium, Brazil, Canada, Chile, China, Colombia, Costa Rica, Czech Republic, Denmark, Ecuador, Egypt, Finland, France, Germany, Greece, Hong Kong, Hungary, India, Indonesia, Ireland, Israel, Italy, Japan, Kuwait, Luxembourg, Malaysia, Mexico, Morocco, Netherlands, New Zealand, Nigeria, Norway, Oman, Pakistan, Panama, Peru, Philippines, Poland, Portugal, Qatar, Romania, Saudi Arabia, Singapore, South Africa, South Korea, Spain, Sweden, Switzerland, Taiwan, Thailand, Turkey, Ukraine, United Arab Emirates, UK, USA, Uruguay, Venezuela, Vietnam

</details>

---

#### **JOB_TYPE**
Filter by job type. Leave empty for all types.

```env
JOB_TYPE=internship    # Internships only
JOB_TYPE=fulltime      # Full-time only
JOB_TYPE=parttime      # Part-time only
JOB_TYPE=contract      # Contract only
JOB_TYPE=              # All types (empty)
```

**⚠️ Indeed Limitation:** Cannot use `JOB_TYPE` with `HOURS_OLD` at the same time.

---

#### **IS_REMOTE**
Filter for remote jobs only.

```env
IS_REMOTE=true     # Remote jobs only
IS_REMOTE=false    # All jobs (default)
```

---

#### **INTERNSHALA_SEARCH_TERM**
Internshala uses category slugs instead of free text search.

```env
# Tech categories
INTERNSHALA_SEARCH_TERM=software-development
INTERNSHALA_SEARCH_TERM=web-development
INTERNSHALA_SEARCH_TERM=mobile-app-development
INTERNSHALA_SEARCH_TERM=data-science
INTERNSHALA_SEARCH_TERM=machine-learning
INTERNSHALA_SEARCH_TERM=python-django
INTERNSHALA_SEARCH_TERM=java
INTERNSHALA_SEARCH_TERM=frontend-development
INTERNSHALA_SEARCH_TERM=backend-development
INTERNSHALA_SEARCH_TERM=full-stack-development

# Commerce categories
INTERNSHALA_SEARCH_TERM=accounting-finance
INTERNSHALA_SEARCH_TERM=finance
INTERNSHALA_SEARCH_TERM=accounts
INTERNSHALA_SEARCH_TERM=audit
INTERNSHALA_SEARCH_TERM=banking

# Other categories
INTERNSHALA_SEARCH_TERM=marketing
INTERNSHALA_SEARCH_TERM=content-writing
INTERNSHALA_SEARCH_TERM=graphic-design
INTERNSHALA_SEARCH_TERM=human-resources
```

---

#### **Advanced Options**

```env
# Distance in miles from location (default: 50)
DISTANCE=50

# Verbosity: 0=errors only, 1=errors+warnings, 2=all logs
VERBOSE=1

# Fetch full job descriptions from LinkedIn (slower but more details)
LINKEDIN_FETCH_DESCRIPTION=true
```

---

## 📝 Example Configurations

### 🖥️ B.Tech Software Developer (India)

```env
WEBHOOK_URL=https://your-webhook-url
SEARCH_TERM=software developer intern
LOCATION=Bangalore
GOOGLE_SEARCH_TERM=software developer intern jobs in Bangalore, India
JOB_SITES=indeed,linkedin,glassdoor,naukri,internshala
RESULTS_WANTED=15
HOURS_OLD=72
DEFAULT_COUNTRY=India
JOB_TYPE=internship
IS_REMOTE=false
INTERNSHALA_SEARCH_TERM=software-development
DISTANCE=50
VERBOSE=1
LINKEDIN_FETCH_DESCRIPTION=true
```

### 📊 B.Com Accounts/Finance (India)

```env
WEBHOOK_URL=https://your-webhook-url
SEARCH_TERM=accounts intern fresher finance
LOCATION=Mumbai
GOOGLE_SEARCH_TERM=accounts intern jobs in Mumbai, India
JOB_SITES=indeed,linkedin,glassdoor,naukri,internshala
RESULTS_WANTED=15
HOURS_OLD=72
DEFAULT_COUNTRY=India
JOB_TYPE=internship
IS_REMOTE=false
INTERNSHALA_SEARCH_TERM=accounting-finance
DISTANCE=50
VERBOSE=1
LINKEDIN_FETCH_DESCRIPTION=true
```

### 🇺🇸 US Software Jobs

```env
WEBHOOK_URL=https://your-webhook-url
SEARCH_TERM=software engineer new grad
LOCATION=San Francisco, CA
GOOGLE_SEARCH_TERM=software engineer entry level jobs in San Francisco
JOB_SITES=indeed,linkedin,glassdoor,google,zip_recruiter
RESULTS_WANTED=20
HOURS_OLD=72
DEFAULT_COUNTRY=USA
JOB_TYPE=fulltime
IS_REMOTE=false
DISTANCE=50
VERBOSE=1
LINKEDIN_FETCH_DESCRIPTION=true
```

### 🏠 Remote Jobs Only

```env
WEBHOOK_URL=https://your-webhook-url
SEARCH_TERM=python developer
LOCATION=Remote
GOOGLE_SEARCH_TERM=remote python developer jobs
JOB_SITES=indeed,linkedin,glassdoor
RESULTS_WANTED=25
HOURS_OLD=168
DEFAULT_COUNTRY=USA
JOB_TYPE=
IS_REMOTE=true
DISTANCE=50
VERBOSE=1
LINKEDIN_FETCH_DESCRIPTION=true
```

---

## 🔧 Troubleshooting

### No jobs from Google?
Google requires very specific syntax. Search on [Google Jobs](https://www.google.com/search?q=jobs) in your browser, apply filters, then copy the exact text from the search box into `GOOGLE_SEARCH_TERM`.

### No jobs from Glassdoor?
Glassdoor aggressively blocks automated requests. Try:
- Reducing `RESULTS_WANTED`
- Adding delays between runs
- Using proxies

### No jobs from LinkedIn?
LinkedIn rate limits quickly. Try:
- Reducing `RESULTS_WANTED` to 10-15
- Using proxies for more requests
- Setting `LINKEDIN_FETCH_DESCRIPTION=false` for faster scraping

### Indeed giving unrelated jobs?
Indeed searches job descriptions too. Use specific queries:
```env
SEARCH_TERM="software intern" python -senior -manager -lead
```

### 429 Error (Too Many Requests)?
You've been rate limited. Wait a few minutes and try again, or use proxies.

### SSL Certificate Errors (macOS + Python 3.13)?
If you see errors like `DECRYPTION_FAILED_OR_BAD_RECORD_MAC` or `CERTIFICATE_VERIFY_FAILED`:

**Quick Fix (already applied in code):**
The code automatically disables SSL verification for compatibility.

**Alternative Fix (if issues persist):**
```bash
# Install/update SSL certificates for Python
/Applications/Python\ 3.13/Install\ Certificates.command

# Or via pip
pip install --upgrade certifi
```

**Note:** This is a known issue with Python 3.13 + macOS + OpenSSL 3.x. The fix works on:
- ✅ macOS (Intel & Apple Silicon)
- ✅ Windows
- ✅ Linux
- ✅ Cloud servers (AWS, GCP, Azure)

---

## 📂 Output

### n8n Webhook Payload
```json
{
  "timestamp": "2026-02-01T12:00:00",
  "search_term": "software developer intern",
  "location": "Bangalore",
  "total_jobs": 45,
  "jobs": [
    {
      "title": "Software Developer Intern",
      "company": "Tech Company",
      "location": "Bangalore, India",
      "job_url": "https://...",
      "description": "...",
      "date_posted": "2026-01-30",
      "site": "linkedin",
      ...
    }
  ]
}
```

### Local Backup
Jobs are also saved locally as `jobs_backup_YYYYMMDD_HHMM.json`

---

## 📜 Credits & License

**Built with ❤️ by [Punya Jain](https://github.com/punyajain1)**

Special thanks to **[JobSpy](https://github.com/Bunsly/JobSpy)** for providing the amazing job scraping library that powers this automation.

---

## 🤝 Contributing

Feel free to submit issues and pull requests!
