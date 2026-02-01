import requests
import urllib3
import ssl
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ===========================================
# SSL FIX for macOS + Python 3.13 + OpenSSL 3.x
# Fixes "DECRYPTION_FAILED_OR_BAD_RECORD_MAC" error
# ===========================================
try:
    # Method 1: Lower security level for ciphers
    urllib3.util.ssl_.DEFAULT_CIPHERS = 'DEFAULT@SECLEVEL=1'
    
    # Method 2: Create a custom SSL context with relaxed settings
    import ssl
    
    # Monkey-patch ssl to use a more permissive context
    _original_create_default_context = ssl.create_default_context
    
    def _create_relaxed_context(purpose=ssl.Purpose.SERVER_AUTH, *, cafile=None, capath=None, cadata=None):
        context = _original_create_default_context(purpose, cafile=cafile, capath=capath, cadata=cadata)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        context.set_ciphers('DEFAULT@SECLEVEL=1')
        return context
    
    ssl.create_default_context = _create_relaxed_context
    
    # Method 3: Disable SSL warnings
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    print("✅ SSL fix applied for Python 3.13 + macOS")
except Exception as e:
    print(f"⚠️ Warning: Could not apply SSL fix: {e}")

# Use local JobSpy-main folder instead of installed package
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'JobSpy-main'))
from jobspy import scrape_jobs
import json
import sys
from datetime import datetime, date
import pandas as pd

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if pd.isna(obj):
        return None
    raise TypeError(f"Type {type(obj)} not serializable")

def scrape_and_send_to_n8n(webhook_url, search_term="software intern", location="United States", 
                           site_name=["indeed", "linkedin", "glassdoor", "google", "zip_recruiter"],
                           results_wanted=20, hours_old=72, country_indeed='USA',
                           internshala_search_term=None, google_search_term=None,
                           job_type=None, is_remote=False, distance=50, verbose=1,
                           linkedin_fetch_description=True):
    """
    Scrape jobs and send directly to n8n webhook
    
    Parameters:
    - google_search_term: Specific search term for Google Jobs (requires exact syntax)
    - job_type: fulltime, parttime, internship, contract
    - is_remote: Filter for remote jobs only
    - distance: Distance in miles from location (default 50)
    """
    
    print(f"🔍 Searching for: {search_term}")
    print(f"📍 Location: {location}")
    print(f"🌐 Sites: {', '.join(site_name)}")
    if google_search_term and 'google' in site_name:
        print(f"🔎 Google search term: {google_search_term}")
    if internshala_search_term and 'internshala' in site_name:
        print(f"🎓 Internshala search term: {internshala_search_term}")
    if job_type:
        print(f"💼 Job type: {job_type}")
    if is_remote:
        print(f"🏠 Remote: Yes")
    print("⏳ Scraping jobs... This may take 1-2 minutes\n")
    
    try:
        # Scrape jobs with all parameters
        jobs = scrape_jobs(
            site_name=site_name,
            search_term=search_term,
            google_search_term=google_search_term,
            location=location,
            distance=distance,
            results_wanted=results_wanted,
            hours_old=hours_old,
            country_indeed=country_indeed,
            job_type=job_type,
            is_remote=is_remote,
            linkedin_fetch_description=linkedin_fetch_description,
            internshala_search_term=internshala_search_term,
            verbose=verbose,
        )
        
        if len(jobs) == 0:
            print("❌ No jobs found. Try different search terms.")
            return
        
        print(f"\n✅ Found {len(jobs)} jobs total!")
        
        # Show breakdown by site
        if 'site' in jobs.columns:
            site_counts = jobs['site'].value_counts()
            print("\n📊 Jobs per site:")
            for site, count in site_counts.items():
                print(f"   {site}: {count} jobs")
            
            # Show which sites returned no jobs
            missing_sites = set(site_name) - set(site_counts.index)
            if missing_sites:
                print(f"\n⚠️  No jobs from: {', '.join(missing_sites)}")
        
        # Convert DataFrame to dict and handle date serialization
        jobs_data = jobs.to_dict('records')
        
        # Clean the data - convert any remaining date objects and NaN values
        cleaned_jobs = []
        for job in jobs_data:
            cleaned_job = {}
            for key, value in job.items():
                # Handle date objects
                if isinstance(value, (datetime, date)):
                    cleaned_job[key] = value.isoformat()
                # Handle NaN/None
                elif pd.isna(value):
                    cleaned_job[key] = None
                # Handle everything else
                else:
                    cleaned_job[key] = value
            cleaned_jobs.append(cleaned_job)
        
        # Preview first job
        if cleaned_jobs:
            print("\n📋 Sample job:")
            print(f"   Title: {cleaned_jobs[0].get('title', 'N/A')}")
            print(f"   Company: {cleaned_jobs[0].get('company', 'N/A')}")
            print(f"   Location: {cleaned_jobs[0].get('location', 'N/A')}\n")
        
        # Send to n8n webhook
        print(f"📤 Sending {len(cleaned_jobs)} jobs to n8n...")
        
        payload = {
            'timestamp': datetime.now().isoformat(),
            'search_term': search_term,
            'location': location,
            'total_jobs': len(cleaned_jobs),
            'jobs': cleaned_jobs
        }
        
        response = requests.post(
            webhook_url,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            print(f"✅ Successfully sent to n8n!")
            print(f"   Response: {response.text[:100]}")
        else:
            print(f"❌ Failed to send. Status code: {response.status_code}")
            print(f"   Response: {response.text}")
        
        # Also save locally as backup
        filename = f"jobs_backup_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(filename, 'w') as f:
            json.dump(payload, f, indent=2, default=json_serial)
        print(f"💾 Backup saved to: {filename}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

import argparse

if __name__ == "__main__":
    try:
        from importlib.metadata import version
        print(f"📦 JobSpy Version: {version('python-jobspy')}")
    except:
        pass

    # Load configuration from environment variables (with defaults)
    WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://nonamework50.app.n8n.cloud/webhook-test/job-scraper")
    
    # Default Configuration from environment variables
    # Sites can be comma-separated in env: "indeed,linkedin,glassdoor,google,zip_recruiter,naukri,internshala,bayt,bdjobs"
    sites_env = os.getenv("JOB_SITES", "indeed,linkedin,glassdoor,google,zip_recruiter,naukri,internshala")
    DEFAULT_SITES = [site.strip() for site in sites_env.split(",")]
    
    DEFAULT_WANTED = int(os.getenv("RESULTS_WANTED", "20"))
    DEFAULT_HOURS = int(os.getenv("HOURS_OLD", "72"))
    # country_indeed expects Title Case (e.g. 'India', 'USA', 'UK')
    DEFAULT_COUNTRY = os.getenv("DEFAULT_COUNTRY", "India")
    
    # Optional: Pre-set search term and location from env
    ENV_SEARCH_TERM = os.getenv("SEARCH_TERM", "")
    ENV_LOCATION = os.getenv("LOCATION", "")
    
    # Google-specific search term (required for Google Jobs to work properly)
    ENV_GOOGLE_SEARCH_TERM = os.getenv("GOOGLE_SEARCH_TERM", "")
    
    # Internshala specific search term (optional)
    ENV_INTERNSHALA_SEARCH_TERM = os.getenv("INTERNSHALA_SEARCH_TERM", "")
    
    # Job type and remote filters
    ENV_JOB_TYPE = os.getenv("JOB_TYPE", "")  # fulltime, parttime, internship, contract
    ENV_IS_REMOTE = os.getenv("IS_REMOTE", "false").lower() == "true"
    
    # Other options
    ENV_DISTANCE = int(os.getenv("DISTANCE", "50"))
    ENV_VERBOSE = int(os.getenv("VERBOSE", "1"))
    ENV_LINKEDIN_FETCH_DESC = os.getenv("LINKEDIN_FETCH_DESCRIPTION", "true").lower() == "true"

    # 1. Parse Command Line Arguments
    parser = argparse.ArgumentParser(description="Job Spy Scraper")
    
    parser.add_argument("term", nargs="?", help="Search term (e.g. 'Software Engineer')")
    parser.add_argument("location", nargs="?", help="Location (e.g. 'San Francisco, CA')")
    parser.add_argument("--country", "-c", default=DEFAULT_COUNTRY, help=f"Indeed country code (default: {DEFAULT_COUNTRY})")
    parser.add_argument("--results", "-r", type=int, default=DEFAULT_WANTED, help=f"Results wanted per site (default: {DEFAULT_WANTED})")
    parser.add_argument("--hours", type=int, default=DEFAULT_HOURS, help=f"Fetch jobs from last X hours (default: {DEFAULT_HOURS})")
    
    args = parser.parse_args()

    # 2. Interactive Mode if Arguments are Missing
    # Priority: CLI args > Environment variables > Interactive prompt
    if args.term:
        search_term = args.term
    elif ENV_SEARCH_TERM:
        search_term = ENV_SEARCH_TERM
        print(f"📌 Using search term from env: {search_term}")
    else:
        print("\n👋 Welcome to JobSpy Scraper!")
        search_term = input("   💼 Enter job role (e.g. 'Software Intern', 'Management'): ").strip()
        if not search_term:
            search_term = "software engineering intern" # Fallback
            print(f"   Using default: {search_term}")

    if args.location:
        location = args.location
    elif ENV_LOCATION:
        location = ENV_LOCATION
        print(f"📌 Using location from env: {location}")
    else:
        location = input("   🌍 Enter location (e.g. 'London', 'Remote', 'United States'): ").strip()
        if not location:
            location = "United States" # Fallback
            print(f"   Using default: {location}")
        
    # Validating country for Indeed
    # If user passed 'INDIA' it might fail, so let's try to fix common cases or warn
    country_indeed = args.country
    if country_indeed.upper() == 'INDIA':
        country_indeed = 'India'
    elif country_indeed.upper() == 'USA':
        country_indeed = 'USA'
    elif country_indeed.upper() in ['UK', 'UNITED KINGDOM']:
        country_indeed = 'UK'
    elif country_indeed.upper() == 'CANADA':
        country_indeed = 'Canada'

    # Filter out region-specific job sites based on search location
    current_sites = list(DEFAULT_SITES)
    is_india_search = 'India' in location or 'India' in country_indeed or country_indeed == 'India'
    is_bangladesh_search = 'Bangladesh' in location or country_indeed == 'Bangladesh'
    
    if is_india_search:
        if 'zip_recruiter' in current_sites:
            current_sites.remove('zip_recruiter')
            print("ℹ️  Removed ZipRecruiter (US/Canada only) for India search")
        if 'bdjobs' in current_sites:
            current_sites.remove('bdjobs')
            print("ℹ️  Removed BDJobs (Bangladesh only) for India search")
    else:
        # Remove India-specific sites for non-India searches
        if 'naukri' in current_sites:
            current_sites.remove('naukri')
            print("ℹ️  Removed Naukri (India only) for non-India search")
        if 'internshala' in current_sites:
            current_sites.remove('internshala')
            print("ℹ️  Removed Internshala (India only) for non-India search")
    
    # Handle Bangladesh-specific filtering
    if not is_bangladesh_search and 'bdjobs' in current_sites:
        current_sites.remove('bdjobs')
        print("ℹ️  Removed BDJobs (Bangladesh only) for non-Bangladesh search")
    
    # Determine site-specific search terms
    internshala_search_term = ENV_INTERNSHALA_SEARCH_TERM if ENV_INTERNSHALA_SEARCH_TERM else None
    google_search_term = ENV_GOOGLE_SEARCH_TERM if ENV_GOOGLE_SEARCH_TERM else None
    job_type = ENV_JOB_TYPE if ENV_JOB_TYPE else None

    print("\n🚀 Ready to scrape:")
    print(f"   Role:    {search_term}")
    print(f"   Place:   {location}")
    print(f"   Country: {country_indeed} (for Indeed/Glassdoor)")
    print(f"   Sites:   {current_sites}")
    if google_search_term:
        print(f"   Google:  {google_search_term}")
    if job_type:
        print(f"   Type:    {job_type}")
    if ENV_IS_REMOTE:
        print(f"   Remote:  Yes")
    print()

    if WEBHOOK_URL == "YOUR_WEBHOOK_URL_HERE":
        print("⚠️  ERROR: Please set your webhook URL in the script first!")
        print("   Get this from n8n webhook node")
    else:
        scrape_and_send_to_n8n(
            webhook_url=WEBHOOK_URL, 
            search_term=search_term, 
            location=location,
            site_name=current_sites,
            results_wanted=args.results,
            hours_old=args.hours,
            country_indeed=country_indeed,
            internshala_search_term=internshala_search_term,
            google_search_term=google_search_term,
            job_type=job_type,
            is_remote=ENV_IS_REMOTE,
            distance=ENV_DISTANCE,
            verbose=ENV_VERBOSE,
            linkedin_fetch_description=ENV_LINKEDIN_FETCH_DESC
        )