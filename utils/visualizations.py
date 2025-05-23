import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from typing import List, Tuple
import logging
import os
import numpy as np # For potential future complex calculations

# Configure logging for the Visualizations module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Visualizations")

def generate_bar_chart(data: List[Tuple[str, int]], title: str, filename: str,
                       x_label: str = "Frequency", y_label: str = "Category",
                       top_n: int = 10, bar_color_map: str = 'viridis',
                       font_name: str = 'Arial'):
    """
    Generates a professional and highly customizable horizontal bar chart and saves it as an image.
    This function incorporates advanced aesthetic and readability enhancements.

    Args:
        data (List[Tuple[str, int]]): A list of (label, value) tuples, e.g., [("Python", 50), ("TensorFlow", 40)].
        title (str): The main title of the chart.
        filename (str): The full path for the output image file (e.g., "output/chart.png").
        x_label (str): Label for the x-axis (horizontal axis).
        y_label (str): Label for the y-axis (vertical axis).
        top_n (int): The number of top elements to display in the chart.
        bar_color_map (str): Matplotlib colormap name for bar colors (e.g., 'viridis', 'plasma', 'cividis').
        font_name (str): Font family to use for all text in the chart.
    """
    if not data:
        logger.warning(f"No data provided for generating the chart for: '{title}'. Skipping chart generation.")
        return

    # Sort data in descending order by value and select the top N elements
    sorted_data = sorted(data, key=lambda item: item[1], reverse=True)[:top_n]
    if not sorted_data: # Check again after slicing
        logger.warning(f"No valid data points after sorting/slicing for: '{title}'. Skipping chart generation.")
        return

    labels = [item[0] for item in sorted_data]
    values = [item[1] for item in sorted_data]

    # Apply a professional Matplotlib style for better aesthetics
    plt.style.use('seaborn-v0_8-darkgrid') # Provides a dark grid background for better contrast

    # Create the figure and axes with a larger, more appropriate size
    fig, ax = plt.subplots(figsize=(12, 8)) # Width, Height in inches

    # Generate colors from the specified colormap
    colors = plt.cm.get_cmap(bar_color_map, len(labels))
    bar_colors = [colors(i) for i in np.linspace(0, 1, len(labels))]

    # Create horizontal bars with specified height and colors
    bars = ax.barh(labels, values, color=bar_colors, height=0.7, edgecolor='black', linewidth=0.5)
    ax.invert_yaxis() # Display the highest value at the top

    # Add data labels on the bars for precise values
    for bar in bars:
        width = bar.get_width()
        ax.annotate(f'{width}',
                    xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0),  # Offset text slightly to the right
                    textcoords="offset points",
                    ha='left', va='center',
                    fontsize=10, color='black',
                    fontweight='bold')

    # Customize axes labels and title with specified font
    ax.set_xlabel(x_label, fontsize=14, labelpad=15, fontname=font_name, fontweight='bold')
    ax.set_ylabel(y_label, fontsize=14, labelpad=15, fontname=font_name, fontweight='bold')
    ax.set_title(title, fontsize=18, pad=25, fontname=font_name, fontweight='bold')

    # Enhance x-axis ticks to be integers and improve readability
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    ax.tick_params(axis='x', labelsize=12, colors='gray')
    ax.tick_params(axis='y', labelsize=12, colors='black')

    # Add a subtle grid
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    ax.grid(axis='y', linestyle=':', alpha=0.5)

    # Remove top and right spines for a cleaner look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(0.5)
    ax.spines['bottom'].set_linewidth(0.5)

    plt.tight_layout() # Adjust layout to prevent labels from overlapping

    # Ensure the output directory exists
    output_dir = os.path.dirname(filename)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save the chart with high resolution and tight bounding box
    try:
        plt.savefig(filename, dpi=300, bbox_inches='tight', transparent=False, facecolor='white')
        logger.info(f"Chart saved successfully: {filename}")
    except Exception as e:
        logger.error(f"Failed to save chart '{filename}': {e}", exc_info=True)
    finally:
        plt.close(fig) # Close the figure to free up memory


if __name__ == "__main__":
    # Example usage for demonstration of the professional visualization module
    # Ensure 'reports' directory exists for saving output
    output_directory = "reports"
    os.makedirs(output_directory, exist_ok=True)

    # Dummy data for job titles and skills
    dummy_titles_data = [
        ("Machine Learning Engineer", 22), ("Data Scientist", 18), ("AI Engineer", 15),
        ("Computer Vision Specialist", 12), ("NLP Engineer", 10), ("Data Analyst", 8),
        ("Data Engineer", 7), ("AI Researcher", 6), ("MLOps Engineer", 5), ("Python Developer (AI)", 4),
        ("AI Consultant", 3), ("AI Product Manager", 2)
    ]

    dummy_skills_data = [
        ("Python", 60), ("TensorFlow", 45), ("PyTorch", 38),
        ("Deep Learning", 35), ("Natural Language Processing", 30),
        ("Computer Vision", 25), ("AWS", 20), ("Kubernetes", 15),
        ("SQL", 12), ("Spark", 10), ("Docker", 8), ("Azure", 7)
    ]

    # Generate charts using the professional function
    generate_bar_chart(
        dummy_titles_data,
        "Top 10 AI/ML Job Titles in MENA (Demo)",
        os.path.join(output_directory, "top_titles_professional_demo.png"),
        top_n=10,
        bar_color_map='plasma' # Using a different colormap for variety
    )

    generate_bar_chart(
        dummy_skills_data,
        "Top 10 AI/ML Skills in MENA (Demo)",
        os.path.join(output_directory, "top_skills_professional_demo.png"),
        top_n=10,
        bar_color_map='cividis' # Another colormap
    )

    logger.info(f"Professional demo charts generated in '{output_directory}/'.")
