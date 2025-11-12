from bs4 import BeautifulSoup
import re


def normalise_text(text: BeautifulSoup) -> str:
    """This function removes html tags and excessive spaces"""

    clean_text = text.get_text()
    normalised_text = re.sub(r'\s+', ' ', clean_text).strip()

    return normalised_text