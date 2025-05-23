import re
from typing import List


def extract_emails(text: str) -> List[str]:
    """
    Extracts all email addresses from a block of text.

    Args:
        text (str): Input text that may contain email addresses.

    Returns:
        List[str]: List of matched email strings.
    """
    email_pattern = r"[\w\.-]+@[\w\.-]+\.\w+"
    return re.findall(email_pattern, text)


def normalize_location(location: str) -> str:
    """
    Normalizes a location string (e.g., trimming whitespace, standard casing).

    Args:
        location (str): Raw location text.

    Returns:
        str: Cleaned location.
    """
    if not location:
        return "Unknown"
    return location.strip().title()


def keyword_in_text(keywords: List[str], text: str) -> List[str]:
    """
    Returns a list of keywords that are found in the text.

    Args:
        keywords (List[str]): List of keywords to match.
        text (str): Text to search within.

    Returns:
        List[str]: Matched keywords.
    """
    matches = []
    for word in keywords:
        if re.search(rf"\\b{re.escape(word)}\\b", text, flags=re.IGNORECASE):
            matches.append(word)
    return matches


if __name__ == "__main__":
    demo_text = "We're hiring a Python developer in Cairo. Contact us at hr@techfirm.com."
    print("Emails:", extract_emails(demo_text))
    print("Location:", normalize_location("  cairo "))
    print("Keywords:", keyword_in_text(["python", "java"], demo_text))
