from typing import List, Dict
import re
import logging

# Configure logging for the DataExtractionAgent
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("DataExtractionAgent")

class DataExtractionAgent:
    """
    Agent responsible for parsing raw job postings and extracting structured fields:
    - Job Title
    - Required Skills
    - Company Name
    - Location
    - Source
    - Description (full text)
    """

    def __init__(self):
        # Define a comprehensive and categorized list of AI/ML skill keywords
        # Categorization helps in potentially more nuanced analysis later
        self.skill_keywords = {
            "programming_languages": ["python", "r", "java", "scala", "c++", "julia"],
            "ml_frameworks": ["tensorflow", "pytorch", "scikit-learn", "keras", "xgboost", "lightgbm"],
            "data_processing": ["pandas", "numpy", "spark", "hadoop", "sql", "nosql", "kafka", "dask"],
            "cloud_platforms": ["aws", "azure", "gcp", "databricks"],
            "mlops_devops": ["mlops", "docker", "kubernetes", "airflow", "ci/cd", "git", "jenkins"],
            "ml_concepts": ["machine learning", "deep learning", "neural networks", "computer vision",
                            "natural language processing", "nlp", "reinforcement learning", "generative ai",
                            "time series", "predictive modeling"],
            "databases_warehousing": ["postgresql", "mysql", "mongodb", "redshift", "snowflake", "bigquery"],
            "visualization": ["tableau", "power bi", "matplotlib", "seaborn", "plotly"],
            "big_data": ["big data", "data warehousing", "data lakes"],
            "statistics_math": ["statistics", "linear algebra", "calculus", "optimization"]
        }
        # Flatten the categorized skills into a single list for regex matching
        self.all_skills = [skill for category_list in self.skill_keywords.values() for skill in category_list]
        logger.info(f"Initialized DataExtractionAgent with {len(self.all_skills)} skill keywords.")


    def extract_skills(self, description: str) -> List[str]:
        """
        Extracts AI/ML-related skills from the job description using robust regex pattern matching.
        The matching is case-insensitive and looks for whole words.

        Args:
            description (str): Raw job description text.

        Returns:
            List[str]: A sorted list of unique matched skill keywords.
        """
        if not description:
            return []

        found_skills = set()
        # Create a single regex pattern for all skills for efficiency
        # Using '\b' for word boundaries and re.escape for special characters in keywords
        # Using '|' to combine all keywords into one pattern
        pattern = r'\b(?:' + '|'.join(re.escape(s) for s in self.all_skills) + r')\b'
        
        # Find all matches and add them to the set
        matches = re.findall(pattern, description, re.IGNORECASE)
        for match in matches:
            found_skills.add(match.lower()) # Convert to lowercase for consistency

        return sorted(list(found_skills))

    def clean_posting(self, raw_posting: Dict) -> Dict:
        """
        Processes and standardizes a raw job posting dictionary, extracting skills and ensuring data quality.

        Args:
            raw_posting (Dict): Dictionary with keys like 'title', 'location', 'company', 'source', and 'description'.

        Returns:
            Dict: Cleaned and enriched posting with extracted skills, or an empty dict if critical data is missing.
        """
        cleaned_post = {}
        try:
            # Basic validation for essential fields
            if not all(key in raw_posting and raw_posting[key] for key in ['title', 'company', 'location', 'description']):
                logger.warning(f"Skipping malformed raw posting due to missing essential keys: {raw_posting.keys()}")
                return {}

            description = raw_posting.get("description", "")
            
            cleaned_post = {
                "title": raw_posting.get("title", "Unknown").strip(),
                "company": raw_posting.get("company", "Unknown").strip(),
                "location": raw_posting.get("location", "Unknown").strip(),
                "source": raw_posting.get("source", "Unknown").strip(),
                "description": description.strip(), # Keep full description for potential future use
                "skills": self.extract_skills(description),
            }
            return cleaned_post
        except Exception as e:
            logger.error(f"Error cleaning posting: {raw_posting.get('title', 'N/A')} - {e}", exc_info=True)
            return {}

    def process_batch(self, raw_postings: List[Dict]) -> List[Dict]:
        """
        Processes a batch of raw job postings and returns a list of cleaned, structured entries.
        Includes logging for progress and validation.

        Args:
            raw_postings (List[Dict]): List of raw job postings.

        Returns:
            List[Dict]: A list of cleaned and structured job entries.
        """
        if not raw_postings:
            logger.info("No raw postings provided for processing.")
            return []

        logger.info(f"Processing {len(raw_postings)} raw job postings...")
        
        cleaned_entries = []
        for i, post in enumerate(raw_postings):
            if post: # Ensure the post itself is not empty
                cleaned_post = self.clean_posting(post)
                if cleaned_post: # Only add if cleaning was successful and returned a valid dict
                    cleaned_entries.append(cleaned_post)
                else:
                    logger.warning(f"Failed to clean posting at index {i}. It was skipped.")
            else:
                logger.warning(f"Empty or None posting found at index {i}. Skipping.")

        logger.info(f"Data extraction complete. Valid entries extracted: {len(cleaned_entries)} out of {len(raw_postings)}.")
        return cleaned_entries


if __name__ == "__main__":
    # Example demonstration of DataExtractionAgent functionality
    dummy_data = [
        {
            "title": "Senior Machine Learning Engineer",
            "company": "Innovate AI Solutions",
            "location": "Dubai, UAE",
            "description": "We are seeking a Python developer with extensive experience in deep learning frameworks like PyTorch and TensorFlow. Knowledge of MLOps practices, AWS cloud services, and Kubernetes is a must. Familiarity with data analysis using Pandas and SQL is a plus.",
            "source": "LinkedIn"
        },
        {
            "title": "Data Scientist",
            "company": "Analytics Hub",
            "location": "Cairo, Egypt",
            "description": "Looking for a Data Scientist skilled in R and Python for statistical modeling and predictive analytics. Experience with big data technologies such as Spark and Hadoop, and visualization tools like Tableau is preferred. NLP experience is a bonus.",
            "source": "Bayt"
        },
        { # Malformed entry example
            "title": "AI Researcher",
            "company": "Future Tech",
            "location": "Riyadh",
            # Missing description intentionally
            "source": "Glassdoor"
        },
        {} # Empty entry example
    ]

    agent = DataExtractionAgent()
    structured_data = agent.process_batch(dummy_data)

    print("\n--- Structured Job Data ---")
    for entry in structured_data:
        print(f"Title: {entry.get('title')}")
        print(f"Company: {entry.get('company')}")
        print(f"Location: {entry.get('location')}")
        print(f"Skills: {', '.join(entry.get('skills', []))}")
        print(f"Source: {entry.get('source')}")
        print(f"Description snippet: {entry.get('description', '')[:100]}...")
        print("-" * 30)

