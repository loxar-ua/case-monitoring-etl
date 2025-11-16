from bs4 import BeautifulSoup
import re


def normalize_text(text: BeautifulSoup) -> str:
    """This function removes html tags and excessive spaces"""

    clean_text = text.get_text()
    normalized_text = re.sub(r'\s+', ' ', clean_text).strip()

    return normalized_text