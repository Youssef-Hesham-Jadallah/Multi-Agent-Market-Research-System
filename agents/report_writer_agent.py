from fpdf import FPDF
import matplotlib.pyplot as plt # Keep this import, fpdf uses it for image dimensions
from typing import List, Tuple, Dict
import os
import logging

# Import the visualization function from utils.visualizations
from utils.visualizations import generate_bar_chart


class ReportWriterAgent:
    """
    Agent responsible for compiling final report using extracted analysis.
    Generates a professional PDF report with charts and insights.
    """

    def __init__(self, report_path: str = "reports/top_ai_ml_jobs_mena_may_2025.pdf"):
        self.report_path = report_path
        self.logger = logging.getLogger("ReportWriterAgent")
        # Ensure logging is configured only once or correctly
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.pdf = FPDF()

    # We no longer need _generate_bar_chart here, as we're importing it from utils.visualizations

    def _add_title_page(self):
        self.pdf.add_page()
        self.pdf.set_font("Arial", 'B', 20)
        self.pdf.cell(200, 20, txt="Top AI/ML Jobs in MENA – May 2025", ln=True, align='C')
        self.pdf.ln(10)
        self.pdf.set_font("Arial", '', 12)
        self.pdf.multi_cell(0, 10, txt="This report provides an overview of the most in-demand AI/ML job roles, key required skills, and job distribution trends across the MENA region.")
        self.pdf.ln(10)
        self.pdf.set_font("Arial", 'I', 10)
        self.pdf.cell(0, 10, txt=f"Date of Report: {os.getenv('REPORT_DATE', 'May 2025')}", ln=True, align='R')


    def _add_section(self, title: str, content: str):
        self.pdf.add_page() # Add a new page for each major section for better layout
        self.pdf.set_font("Arial", 'B', 16)
        self.pdf.ln(10)
        self.pdf.cell(0, 10, title, ln=True, align='L')
        self.pdf.ln(5) # Add some space after title
        self.pdf.set_font("Arial", '', 12)
        # Use write() for simple text and multi_cell for longer, wrapped text
        if content:
            self.pdf.multi_cell(0, 8, content) # Reduced line height for density
        else:
            self.pdf.write(8, "") # Placeholder for empty content section

    def _add_image(self, image_path: str, w: int = 180):
        """
        Adds an image to the PDF, centering it.
        """
        if not os.path.exists(image_path):
            self.logger.warning(f"Image not found: {image_path}. Skipping.")
            return

        # Calculate x position to center the image
        page_width = self.pdf.w
        image_x = (page_width - w) / 2

        self.pdf.ln(5)
        self.pdf.image(image_path, x=image_x, w=w)
        self.pdf.ln(5) # Space after image


    def generate_report(self, insights: Dict[str, any]):
        """
        Assembles the final PDF report from insights.

        Args:
            insights (Dict[str, any]): Analysis results from TrendAnalysisAgent.
        """
        self.logger.info("Starting report generation...")
        
        # Ensure the reports directory exists
        output_dir = os.path.dirname(self.report_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Define image paths for charts
        top_titles_chart_path = os.path.join(output_dir, "top_titles.png")
        top_skills_chart_path = os.path.join(output_dir, "top_skills.png")

        # Generate charts using the imported function from utils.visualizations
        # Pass the full output path to the visualization function
        generate_bar_chart(
            insights.get("top_titles", []), # Provide default empty list if key missing
            "Top AI/ML Job Titles",
            top_titles_chart_path,
            y_label="Job Title", # Specific label for clarity
            x_label="Number of Listings" # Specific label for clarity
        )
        generate_bar_chart(
            insights.get("top_skills", []),
            "Top AI/ML Skills",
            top_skills_chart_path,
            y_label="Skill", # Specific label for clarity
            x_label="Frequency" # Specific label for clarity
        )

        # Build PDF structure
        self.pdf.add_page() # Start with a fresh page for the title
        self._add_title_page()

        self._add_section("Summary of Key Insights", insights.get("summary", "No summary available."))
        
        self._add_section("Top 10 AI/ML Job Titles", "The following chart illustrates the most frequently appearing job titles.")
        self._add_image(top_titles_chart_path)

        self._add_section("Top 10 AI/ML Skills", "Below are the essential skills most demanded by employers in the AI/ML sector.")
        self._add_image(top_skills_chart_path)

        locations_text = "\n".join([f"• {loc}: {count} listings" for loc, count in insights.get("location_distribution", [])])
        if not locations_text:
            locations_text = "No location distribution data available."
        self._add_section("Geographical Distribution of Opportunities", locations_text)

        # Output the PDF
        self.pdf.output(self.report_path)
        self.logger.info(f"Report written successfully to {self.report_path}")


if __name__ == "__main__":
    # Dummy insights example for testing
    dummy_insights = {
        "top_titles": [("Machine Learning Engineer", 22), ("Data Scientist", 18), ("AI Specialist", 15),
                       ("Computer Vision Eng.", 12), ("NLP Scientist", 10), ("Data Analyst", 8),
                       ("Deep Learning Researcher", 7), ("MLOps Engineer", 6), ("Robotics Engineer", 5), ("AI Consultant", 4)],
        "top_skills": [("Python", 60), ("TensorFlow", 45), ("PyTorch", 38), ("Deep Learning", 35),
                       ("NLP", 30), ("Computer Vision", 25), ("AWS", 20), ("SQL", 15),
                       ("Kubernetes", 12), ("Spark", 10)],
        "location_distribution": [("Dubai, UAE", 35), ("Cairo, Egypt", 25), ("Riyadh, KSA", 20), ("Amman, Jordan", 10)],
        "summary": (
            "The MENA AI/ML job market shows robust demand for Machine Learning Engineers, "
            "with Python and TensorFlow being the most sought-after skills. "
            "Major hubs include Dubai, Cairo, and Riyadh, indicating strong regional growth in AI adoption."
        )
    }

    report_agent = ReportWriterAgent()
    report_agent.generate_report(dummy_insights)
    print("Demo report generated.")