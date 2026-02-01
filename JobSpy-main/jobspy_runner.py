#!/usr/bin/env python3
"""
JobSpy Production Script - Ready to use with all sites
"""

import pandas as pd
from jobspy import scrape_jobs
import argparse
import sys
from datetime import datetime

class JobSpyRunner:
    """Production-ready JobSpy runner with all sites support"""
    
    # All supported sites
    SUPPORTED_SITES = [
        "linkedin", "indeed", "glassdoor", "google", 
        "zip_recruiter", "internshala", "bayt", "naukri", "bdjobs"
    ]
    
    def __init__(self):
        self.results = []
    
    def run_search(self, config):
        """Run a job search with given configuration"""
        
        print(f"🔍 Searching: '{config['search_term']}'")
        print(f"📍 Location: {config.get('location', 'Any')}")
        print(f"🌐 Sites: {', '.join(config['sites'])}")
        
        try:
            jobs = scrape_jobs(
                site_name=config["sites"],
                search_term=config["search_term"],
                internshala_search_term=config.get("internshala_search_term"),
                location=config.get("location"),
                distance=config.get("distance", 50),
                is_remote=config.get("is_remote", False),
                job_type=config.get("job_type"),
                results_wanted=config.get("results_wanted", 20),
                hours_old=config.get("hours_old"),
                country_indeed=config.get("country", "USA"),
                proxies=config.get("proxies"),
                verbose=config.get("verbose", 0)
            )
            
            if len(jobs) > 0:
                print(f"✅ Found {len(jobs)} jobs")
                site_breakdown = jobs['site'].value_counts().to_dict()
                for site, count in site_breakdown.items():
                    print(f"   {site}: {count} jobs")
                
                self.results.append(jobs)
                return jobs
            else:
                print("⚠️  No jobs found")
                return pd.DataFrame()
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return pd.DataFrame()
    
    def save_results(self, filename=None):
        """Save all results to CSV"""
        if not self.results:
            print("No results to save")
            return
        
        combined = pd.concat(self.results, ignore_index=True)
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"jobspy_results_{timestamp}.csv"
        
        combined.to_csv(filename, index=False)
        print(f"💾 Saved {len(combined)} jobs to {filename}")
        
        return combined

def create_presets():
    """Pre-configured search templates"""
    return {
        "tech_global": {
            "sites": ["linkedin", "indeed", "glassdoor", "google"],
            "search_term": "software engineer",
            "location": "San Francisco, CA",
            "country": "USA",
            "results_wanted": 25
        },
        "tech_india": {
            "sites": ["internshala", "naukri", "indeed"],
            "search_term": "python developer", 
            "internshala_search_term": "python programming",
            "location": "Bangalore",
            "country": "India",
            "results_wanted": 30
        },
        "data_science": {
            "sites": ["linkedin", "indeed", "glassdoor"],
            "search_term": "data scientist",
            "location": "New York, NY",
            "results_wanted": 20
        },
        "internships": {
            "sites": ["internshala"],
            "search_term": "software development",
            "internshala_search_term": "computer science internship",
            "job_type": "internship",
            "location": "Mumbai",
            "results_wanted": 40
        },
        "remote_work": {
            "sites": ["linkedin", "indeed", "internshala"],
            "search_term": "remote developer",
            "is_remote": True,
            "results_wanted": 25
        },
        "full_spectrum": {
            "sites": ["linkedin", "indeed", "internshala", "glassdoor", "naukri"],
            "search_term": "software engineer",
            "internshala_search_term": "software development",
            "location": "Delhi",
            "results_wanted": 20
        }
    }

def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(description="JobSpy - Multi-site Job Scraper")
    parser.add_argument("--preset", choices=create_presets().keys(), 
                       help="Use a pre-configured search")
    parser.add_argument("--sites", nargs="+", default=["internshala", "indeed"],
                       help="Sites to search (space-separated)")
    parser.add_argument("--search", default="python developer",
                       help="Search term")
    parser.add_argument("--location", help="Location to search")
    parser.add_argument("--results", type=int, default=20,
                       help="Number of results per site")
    parser.add_argument("--remote", action="store_true",
                       help="Search for remote jobs only")
    parser.add_argument("--job-type", choices=["fulltime", "parttime", "internship", "contract"],
                       help="Job type filter")
    parser.add_argument("--hours", type=int, help="Jobs posted within X hours")
    parser.add_argument("--output", help="Output CSV filename")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    runner = JobSpyRunner()
    
    if args.preset:
        # Use preset configuration
        presets = create_presets()
        config = presets[args.preset]
        print(f"🎯 Using preset: {args.preset}")
    else:
        # Build config from arguments
        config = {
            "sites": args.sites,
            "search_term": args.search,
            "location": args.location,
            "results_wanted": args.results,
            "is_remote": args.remote,
            "job_type": args.job_type,
            "hours_old": args.hours,
            "verbose": 1 if args.verbose else 0
        }
    
    print("🚀 Starting JobSpy search...")
    print("=" * 50)
    
    # Run the search
    results = runner.run_search(config)
    
    if len(results) > 0:
        # Save results
        combined = runner.save_results(args.output)
        
        print("\n📊 Summary:")
        print(f"Total jobs: {len(combined)}")
        print(f"Companies: {combined['company'].nunique()}")
        print(f"Locations: {combined['location'].nunique()}")
        
        # Show top companies
        top_companies = combined['company'].value_counts().head(5)
        print(f"\nTop companies:")
        for company, count in top_companies.items():
            print(f"  {company}: {count} jobs")
    
    print("\n✅ Search completed!")

if __name__ == "__main__":
    # If run directly, use command line arguments
    if len(sys.argv) > 1:
        main()
    else:
        # Interactive mode
        print("🌟 JobSpy Interactive Mode")
        print("Available presets:")
        presets = create_presets()
        for name, config in presets.items():
            print(f"  {name}: {config['search_term']} ({', '.join(config['sites'])})")
        
        choice = input("\nEnter preset name (or 'custom' for manual): ").strip()
        
        runner = JobSpyRunner()
        
        if choice in presets:
            config = presets[choice]
            print(f"Using preset: {choice}")
        elif choice == 'custom':
            config = {
                "sites": input("Sites (comma-separated): ").split(","),
                "search_term": input("Search term: "),
                "location": input("Location (optional): ") or None,
                "results_wanted": int(input("Results wanted (default 20): ") or "20")
            }
        else:
            print("Invalid choice, using 'tech_india' preset")
            config = presets['tech_india']
        
        results = runner.run_search(config)
        if len(results) > 0:
            runner.save_results()