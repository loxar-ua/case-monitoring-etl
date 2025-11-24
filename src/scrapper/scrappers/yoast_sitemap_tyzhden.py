from bs4 import BeautifulSoup
from datetime import datetime
import re

from src.utils.get_response import get_response
from . import LinkInfo

def get_links_yoast(sitemap_index_url, sub_sitemaps_pattern, start_date, end_date):
    sitemap_index_response = get_response(sitemap_index_url)
    if sitemap_index_response is None:
        return []

    sitemap_index_soup = BeautifulSoup(sitemap_index_response.content, "lxml-xml")

    sub_sitemap_urls = [
        sitemap.find('loc').text
        for sitemap in sitemap_index_soup.find_all("sitemap")
        if sitemap.find('loc') is not None and sitemap.find('loc').text
    ]

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

            if loc_tag is None or loc_tag.text is None:
                continue

            if lastmod_tag is None or lastmod_tag.text is None:
                continue
            lastmod_dt = datetime.fromisoformat(lastmod_tag.text)

            if start_date <= lastmod_dt <= end_date:
                links.append(loc_tag.text)

    return links
