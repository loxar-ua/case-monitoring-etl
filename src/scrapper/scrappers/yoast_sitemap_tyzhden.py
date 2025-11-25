from bs4 import BeautifulSoup
from datetime import datetime
import re

from src.utils.get_response import get_response
from . import LinkInfo  # твій NamedTuple або dataclass

def get_links_yoast(sitemap_index_url, sub_sitemaps_pattern, start_date, end_date):
    """
    Повертає список LinkInfo для URL, lastmod яких у вказаному діапазоні.
    """
    sitemap_index_response = get_response(sitemap_index_url)
    if sitemap_index_response is None:
        return []

    sitemap_index_soup = BeautifulSoup(sitemap_index_response.content, "lxml-xml")

    # Всі URL під-sitemap
    sub_sitemap_urls = [
        sitemap.find('loc').text
        for sitemap in sitemap_index_soup.find_all("sitemap")
        if sitemap.find('loc') is not None and sitemap.find('loc').text
    ]

    # Фільтрація по regex
    sub_sitemap_urls = [url for url in sub_sitemap_urls if re.fullmatch(sub_sitemaps_pattern, url)]

    links = []

    for sub_sitemap_url in sub_sitemap_urls:
        sub_sitemap_response = get_response(sub_sitemap_url)
        if sub_sitemap_response is None:
            continue

        sub_sitemap_soup = BeautifulSoup(sub_sitemap_response.content, "lxml-xml")
        for url_tag in sub_sitemap_soup.find_all("url"):
            loc_tag = url_tag.find("loc")
            lastmod_tag = url_tag.find("lastmod")

            if loc_tag is None or not loc_tag.text:
                continue

            loc = loc_tag.text

            if lastmod_tag is None or not lastmod_tag.text:
                # Якщо lastmod відсутній, можна пропускати або ставити None
                continue

            # Безпечне перетворення ISO формату з часом і зоною
            try:
                lastmod_dt = datetime.fromisoformat(lastmod_tag.text)
            except ValueError:
                continue

            # Перевірка діапазону
            if start_date and end_date:
                if not (start_date <= lastmod_dt <= end_date):
                    continue

            links.append(LinkInfo(loc, lastmod_dt))

    return links
