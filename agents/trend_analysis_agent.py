from typing import List, Dict, Tuple
import pandas as pd
import logging
from collections import Counter

# Configure logging for the TrendAnalysisAgent
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("TrendAnalysisAgent")

class TrendAnalysisAgent:
    """
    Agent responsible for analyzing cleaned job postings to extract key insights:
    - Most in-demand job titles
    - Most frequent skills
    - Geographic distribution of jobs
    - Overall trend observations and summary
    """

    def __init__(self):
        logger.info("TrendAnalysisAgent initialized.")

    def _flatten_skills(self, postings: List[Dict]) -> List[str]:
        """
        Helper function to flatten all skill lists from job postings into a single list.
        Ensures robust handling of missing 'skills' key.

        Args:
            postings (List[Dict]): A list of structured job entries.

        Returns:
            List[str]: A flattened list containing all mentioned skills.
        """
        skills = []
        for post in postings:
            # Safely get skills, defaulting to an empty list if key is missing
            skills.extend(post.get("skills", []))
        return skills

    def analyze(self, postings: List[Dict]) -> Dict[str, any]:
        """
        Analyzes structured job postings to compute job title frequency, skill frequency,
        and location distribution. Generates a comprehensive dictionary of insights.

        Args:
            postings (List[Dict]): A list of structured job entries (output from DataExtractionAgent).

        Returns:
            Dict[str, any]: A dictionary containing various insights and rankings,
                            including top titles, top skills, location distribution, and a summary.
        """
        if not postings:
            logger.warning("No job postings provided for analysis. Returning empty insights.")
            return {
                "top_titles": [],
                "top_skills": [],
                "location_distribution": [],
                "summary": "Insufficient data for trend summary."
            }

        logger.info(f"Starting trend analysis on {len(postings)} job postings...")

        # Convert list of dicts to a pandas DataFrame for efficient analysis
        df = pd.DataFrame(postings)

        # Ensure necessary columns exist, handling potential missing data
        for col in ["title", "location", "skills"]:
            if col not in df.columns:
                logger.warning(f"Column '{col}' not found in DataFrame. Analysis might be incomplete.")
                df[col] = None # Add column with None values if missing

        # Calculate frequencies
        title_freq = Counter(df["title"].dropna()) # Drop NA titles before counting
        skill_freq = Counter(self._flatten_skills(postings))
        location_freq = Counter(df["location"].dropna()) # Drop NA locations before counting

        # Get top N entries for titles and skills
        # Limiting to top 10 as per typical report requirements
        top_titles = title_freq.most_common(10)
        top_skills = skill_freq.most_common(10)
        # For locations, typically all unique locations are relevant, but can be limited if too many
        top_locations = location_freq.most_common() # Get all locations and their counts

        logger.info("Trend analysis completed successfully.")

        return {
            "top_titles": top_titles,
            "top_skills": top_skills,
            "location_distribution": top_locations,
            "summary": self.generate_summary(top_titles, top_skills, top_locations)
        }

    def generate_summary(self, top_titles: List[Tuple[str, int]],
                         top_skills: List[Tuple[str, int]],
                         location_distribution: List[Tuple[str, int]]) -> str:
        """
        Creates a natural language summary of the analysis for reporting purposes.
        Provides a more detailed and dynamic summary based on available data.

        Args:
            top_titles (List[Tuple[str, int]]): Ranked list of top job titles.
            top_skills (List[Tuple[str, int]]): Ranked list of top skill keywords.
            location_distribution (List[Tuple[str, int]]): Distribution of jobs by location.

        Returns:
            str: A human-readable summary of the AI/ML job market trends.
        """
        summary_parts = []

        if top_titles:
            most_common_title = top_titles[0][0]
            summary_parts.append(
                f"As of May 2025, the most in-demand AI/ML job title in the MENA region is \"{most_common_title}\"."
            )
        else:
            summary_parts.append("Job title demand trends could not be determined due to insufficient data.")

        if top_skills:
            most_common_skill = top_skills[0][0]
            summary_parts.append(
                f"The top required skill across job listings is \"{most_common_skill}\"."
            )
            if len(top_skills) > 1:
                summary_parts.append(
                    f"Other highly sought-after skills include: {', '.join([s[0] for s in top_skills[1:5]])}."
                )
        else:
            summary_parts.append("Key skill requirements could not be identified.")

        if location_distribution:
            top_locations = [loc[0] for loc in location_distribution[:3]]
            summary_parts.append(
                f"Geographically, the demand is primarily concentrated in: {', '.join(top_locations)}."
            )
        else:
            summary_parts.append("Geographic distribution of jobs could not be analyzed.")

        summary_parts.append(
            "Overall, the market indicates a strong demand for roles involving advanced machine learning pipelines, "
            "cloud-based deployment, and robust data engineering capabilities."
        )

        return " ".join(summary_parts)


if __name__ == "__main__":
    # Example demonstration of TrendAnalysisAgent functionality
    dummy_structured_jobs = [
        {"title": "ML Engineer", "skills": ["python", "tensorflow", "aws"], "location": "Dubai"},
        {"title": "ML Engineer", "skills": ["pytorch", "aws", "docker"], "location": "Dubai"},
        {"title": "Data Scientist", "skills": ["python", "nlp", "pandas"], "location": "Cairo"},
        {"title": "AI Specialist", "skills": ["computer vision", "tensorflow", "gcp"], "location": "Riyadh"},
        {"title": "Data Engineer", "skills": ["sql", "spark", "aws"], "location": "Dubai"},
        {"title": "ML Engineer", "skills": ["python", "mlops"], "location": "Amman"},
        {"title": "Data Scientist", "skills": ["r", "statistics"], "location": "Cairo"},
        {"title": "AI Researcher", "skills": ["deep learning", "pytorch"], "location": "Doha"},
        {"title": "ML Engineer", "skills": ["kubernetes", "docker"], "location": "Dubai"},
        {"title": "Data Analyst", "skills": ["sql", "excel"], "location": "Beirut"},
        {"title": "ML Engineer", "skills": ["python", "tensorflow"], "location": "Dubai"},
    ]

    agent = TrendAnalysisAgent()
    insights = agent.analyze(dummy_structured_jobs)

    print("\n--- Analysis Insights ---")
    print("Summary:", insights["summary"])
    print("\nTop 10 Job Titles:")
    for title, count in insights["top_titles"]:
        print(f"- {title}: {count}")
    print("\nTop 10 Skills:")
    for skill, count in insights["top_skills"]:
        print(f"- {skill}: {count}")
    print("\nJob Distribution by Location:")
    for location, count in insights["location_distribution"]:
        print(f"- {location}: {count}")

