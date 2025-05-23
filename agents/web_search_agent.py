import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import logging
import time
import random # Added for more randomness in delay


class WebSearchAgent:
    """
    Agent responsible for querying job platforms and aggregating raw data.
    It supports scraping multiple MENA-region specific job boards.
    """

    def __init__(self, platforms: List[str], delay: float = 1.5):
        """
        Initializes the WebSearchAgent with a list of job platforms.

        Args:
            platforms (List[str]): List of platform URLs to scrape.
            delay (float): Delay between requests to avoid bans.
        """
        self.platforms = platforms
        self.delay = delay
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Connection': 'keep-alive',
        }
        # Configure logging specifically for this agent.
        self.logger = logging.getLogger("WebSearchAgent")
        # Ensure that basicConfig is only called once.
        if not logging.root.handlers:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


    def fetch_html(self, url: str, attempt: int = 1) -> str:
        """
        Fetches HTML content from a given URL with retries.

        Args:
            url (str): The URL of the web page to fetch.
            attempt (int): Current retry attempt number.

        Returns:
            str: Raw HTML content.
        """
        max_attempts = 3
        try:
            self.logger.info(f"Fetching HTML from: {url} (Attempt {attempt})")
            response = requests.get(url, headers=self.headers, timeout=15) # Increased timeout
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            return response.text
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching URL {url}: {e}")
            if attempt < max_attempts:
                self.logger.info(f"Retrying fetch for {url} in {self.delay * 2} seconds...")
                time.sleep(self.delay * 2) # Exponential backoff
                return self.fetch_html(url, attempt + 1)
            else:
                self.logger.error(f"Failed to fetch {url} after {max_attempts} attempts.")
                return ""

    def parse_linkedin_jobs(self, html_content: str) -> List[Dict]:
        """
        Parses LinkedIn job search results HTML to extract job titles, companies, and locations.
        Updated selectors for LinkedIn (as of mid-2024, prone to change).

        Args:
            html_content (str): Raw HTML content of the LinkedIn search results page.

        Returns:
            List[Dict]: A list of dictionaries, each representing a job posting with title, company, location.
        """
        jobs = []
        soup = BeautifulSoup(html_content, 'html.parser')

        # Try to find the main list container for jobs
        # LinkedIn often uses 'ul' with class 'jobs-search__results-list'
        job_list_container = soup.find('ul', class_='jobs-search__results-list')

        if job_list_container:
            # If the list container is found, find all list items (li) within it
            job_cards = job_list_container.find_all('li')
            self.logger.info(f"Found {len(job_cards)} 'li' job cards within the main list container.")
        else:
            # Fallback: If the specific list container is not found, try to find general job cards
            # This is less precise but might catch some cases.
            job_cards = soup.find_all('div', class_=lambda x: x and ('job-search-card' in x or 'base-card' in x))
            self.logger.warning(f"Main job list container not found. Trying general 'div' job cards. Found {len(job_cards)} general cards.")


        if not job_cards:
            self.logger.error("Still no specific job cards found on the LinkedIn page. HTML structure might have changed significantly or page is truly empty.")
            return [] # Return empty list if no cards found

        for card in job_cards:
            try:
                # Updated selectors for elements within each job card.
                # Using lambda to check if the class string contains the target class name.
                title_tag = card.find('h3', class_=lambda x: x and 'base-search-card__title' in x)
                company_tag = card.find('h4', class_=lambda x: x and 'base-search-card__subtitle' in x)
                location_tag = card.find('span', class_=lambda x: x and 'job-search-card__location' in x)

                title = title_tag.text.strip() if title_tag else "N/A"
                company = company_tag.text.strip() if company_tag else "N/A"
                location = location_tag.text.strip() if location_tag else "N/A"

                # Only add if essential information is available
                if title != "N/A" and company != "N/A" and location != "N/A":
                    jobs.append({
                        'title': title,
                        'company': company,
                        'location': location,
                        'source': 'LinkedIn'
                    })
                else:
                    self.logger.debug(f"Skipping job card due to missing essential info: Title='{title}', Company='{company}', Location='{location}'")
            except Exception as e: # Catch any parsing error for a specific card
                self.logger.debug(f"Error parsing individual job card: {e}")
                continue  # skip malformed cards

        self.logger.info(f"Successfully parsed {len(jobs)} jobs from the LinkedIn page.")
        return jobs

    def scrape_all(self) -> List[Dict]:
        """
        Orchestrates the full scraping process across all platforms.

        Returns:
            List[Dict]: Aggregated raw job postings.
        """
        all_jobs = []
        for platform_url in self.platforms:
            self.logger.info(f"Initiating scraping for platform: {platform_url}")
            html = self.fetch_html(platform_url)
            if html:
                if 'linkedin' in platform_url:
                    jobs_from_platform = self.parse_linkedin_jobs(html)
                    all_jobs.extend(jobs_from_platform)
                else:
                    self.logger.warning(f"No specific parser for {platform_url}. Skipping.")
            else:
                self.logger.error(f"Failed to fetch HTML from {platform_url}. No jobs scraped from this source.")

            # Add a dynamic delay to be more robust against simple bot detection
            dynamic_delay = self.delay + (random.uniform(0.5, 2.0)) # Add random fraction
            self.logger.info(f"Pausing for {dynamic_delay:.2f} seconds...")
            time.sleep(dynamic_delay)

        self.logger.info(f"Total jobs scraped across all platforms: {len(all_jobs)}")
        return all_jobs


if __name__ == "__main__":
    # Example use case for testing this agent directly
    # IMPORTANT: LinkedIn URLs change. You might need to visit LinkedIn jobs,
    # perform a search, and copy the URL from your browser's address bar.
    # The filter &f_TPR=r86400 means "Past 24 hours", which often yields zero results.
    # For more results, try removing this filter or setting it to a longer period.
    
    # Example URL without "Past 24 hours" filter:
    test_platforms = ["https://www.linkedin.com/jobs/search/?keywords=machine%20learning&location=MENA"]
    
    # Or, if you want a specific country in MENA, e.g., Egypt:
    # test_platforms = ["https://www.linkedin.com/jobs/search/?keywords=AI%20engineer&location=Egypt"]
    
    # You might also try a very broad search to ensure general parsing works:
    # test_platforms = ["https://www.linkedin.com/jobs/search/?keywords=software%20engineer"]


    # Initialize logging if running directly for testing
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    agent = WebSearchAgent(platforms=test_platforms, delay=3.0) # Increased default delay for testing
    scraped_jobs = agent.scrape_all()

    if scraped_jobs:
        print(f"\n--- Scraped {len(scraped_jobs)} Jobs ---")
        for i, job in enumerate(scraped_jobs[:5]): # Print first 5 for brevity
            print(f"Job {i+1}: Title: {job.get('title')}, Company: {job.get('company')}, Location: {job.get('location')}")
        
        # Save to a temporary file for inspection
        import os
        os.makedirs("data", exist_ok=True)
        with open("data/test_raw_jobs.json", "w", encoding='utf-8') as f:
            json.dump(scraped_jobs, f, indent=2, ensure_ascii=False)
        print("\nRaw jobs saved to data/test_raw_jobs.json")
    else:
        print("\nNo jobs scraped. Please check the LinkedIn URL, your internet connection, or try updating LinkedIn HTML selectors in web_search_agent.py again.")