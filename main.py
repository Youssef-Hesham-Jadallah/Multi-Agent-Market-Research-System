import logging
import os
import json
import sys

# Ensure project root is in path for imports
# This is crucial if you run the script from a different directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from agents.web_search_agent import WebSearchAgent
from agents.data_extraction_agent import DataExtractionAgent
from agents.trend_analysis_agent import TrendAnalysisAgent
from agents.report_writer_agent import ReportWriterAgent

# Configure logging for the main orchestrator
# This ensures that all agents and the main script log to the console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("MainOrchestrator")


def main():
    logger.info("Launching Multi-Agent AI/ML Market Intelligence System for MENA...")

    # Create directories if they don't exist
    os.makedirs("data", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    # Step 1: Web Search Agent — collect raw job data
    logger.info("Step 1: Initializing Web Search Agent for data collection.")
    
    # IMPORTANT: Use a LinkedIn URL that you have tested manually in a browser
    # and confirmed has job listings.
    # If you are facing "Too many requests" or 0 jobs, try these steps:
    # 1. WAIT: Give LinkedIn a few hours (or 24h) to lift any temporary IP ban.
    # 2. TEST A SIMPLER URL: Temporarily use a very broad or simple search query.
    #    e.g., "https://www.linkedin.com/jobs/search/?keywords=software"
    #    or "https://www.linkedin.com/jobs/search/?keywords=engineer"
    # 3. VERIFY HTML SELECTORS: If still no jobs after lifting the ban, you MUST
    #    manually inspect LinkedIn's HTML (using browser developer tools) and
    #    update the selectors in 'web_search_agent.py' accordingly.
    
    platforms = [
        "https://www.linkedin.com/jobs/search/?keywords=machine%20learning&location=MENA"
        # Example for a simpler test:
        # "https://www.linkedin.com/jobs/search/?keywords=software"
        # You can add more LinkedIn URLs or other platforms if you implement their parsing logic.
    ]
    
    # Adjust the delay based on your observations and LinkedIn's response.
    # Higher delay reduces the chance of being blocked but makes scraping slower.
    search_agent = WebSearchAgent(platforms=platforms, delay=2.5) # Slight increase for robustness
    
    raw_data = search_agent.scrape_all()

    if not raw_data:
        logger.warning("Web Search Agent returned no raw data. Subsequent steps might be affected.")
        # Optionally, you can exit here if no data is crucial for the report.
        # sys.exit("No raw data collected. Exiting.")
    else:
        # Optional: persist raw data if collected
        with open("data/raw_jobs_data.json", "w", encoding='utf-8') as f:
            json.dump(raw_data, f, indent=2, ensure_ascii=False)
        logger.info("Raw job data saved to data/raw_jobs_data.json")

    # Step 2: Data Extraction Agent — clean and extract features
    logger.info("Step 2: Initializing Data Extraction Agent for data processing.")
    extraction_agent = DataExtractionAgent()
    
    structured_data = []
    if raw_data: # Only process if there's raw data
        structured_data = extraction_agent.process_batch(raw_data)
        with open("data/processed_jobs_data.json", "w", encoding='utf-8') as f:
            json.dump(structured_data, f, indent=2, ensure_ascii=False)
        logger.info("Processed job data saved to data/processed_jobs_data.json")
    else:
        logger.info("Skipping data extraction as no raw data was collected.")


    # Step 3: Trend Analysis Agent — analyze trends
    logger.info("Step 3: Initializing Trend Analysis Agent for insights generation.")
    analysis_agent = TrendAnalysisAgent()
    
    insights = {}
    if structured_data: # Only analyze if there's structured data
        insights = analysis_agent.analyze(structured_data)
    else:
        logger.info("Skipping trend analysis as no structured data was available.")

    # Step 4: Report Writer Agent — generate PDF report
    logger.info("Step 4: Initializing Report Writer Agent for PDF report generation.")
    report_agent = ReportWriterAgent()

    # Check if essential insights are available before trying to generate report
    if insights and insights.get("summary") and insights.get("top_titles") and insights.get("top_skills") and insights.get("location_distribution"):
        try:
            report_agent.generate_report(insights)
            logger.info("Report generation complete. Check the 'reports' folder.")
        except Exception as e:
            logger.error(f"Error during report generation: {e}")
            logger.error("Report generation skipped due to errors or missing FPDF/Matplotlib setup.")
    else:
        logger.error("Cannot generate report due to missing or insufficient insights from trend analysis.")
        logger.error("Report generation skipped. Ensure data was collected and processed successfully.")


if __name__ == "__main__":
    main()