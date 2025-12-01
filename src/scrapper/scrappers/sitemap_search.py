from bs4 import BeautifulSoup

from datetime import datetime, timezone
import re

from src.utils.get_response import get_response
from . import LinkInfo

def get_links_from_sitemap(sitemap_index_url, sub_sitemaps_pattern, start_date, end_date, ):
    """Using <lastmod> finds what subsitemaps to check.
    Inside subsitemap, using <lastmod> finds what articles to take.
    Returns a list of links."""

    sitemap_index_response = get_response(sitemap_index_url)
    if not sitemap_index_response:
        return None

    sitemap_index_soup = BeautifulSoup(sitemap_index_response.content, "lxml-xml")

    sub_sitemap_urls = [sitemap.find('loc').text
                        for sitemap in sitemap_index_soup.find_all("sitemap")]

    # Filter all unimportant sitemaps, that don't contain articles
    sub_sitemap_urls = list(filter(
        lambda x: re.fullmatch(sub_sitemaps_pattern, x),
        sub_sitemap_urls
    ))

    combined_sub_sitemap = BeautifulSoup("<urlset></urlset>", "lxml-xml")
    for sub_sitemap_url in sub_sitemap_urls:

        sub_sitemap_response = get_response(sub_sitemap_url)
        if not sub_sitemap_response:
            continue

        sub_sitemap_soup = BeautifulSoup(sub_sitemap_response.content, "lxml-xml")

        urlset_tag = sub_sitemap_soup.find("urlset")
        if urlset_tag:
            for url_tag in urlset_tag.find_all(recursive=False):
                combined_sub_sitemap.urlset.append(url_tag)

    article_urls = [LinkInfo(url.find("loc").text.strip(),
                             datetime.fromisoformat(url.find("lastmod").text)
                             .replace(tzinfo=timezone.utc))
                    for url in combined_sub_sitemap.urlset]

    # Get articles that only fall within a specified time interval
    article_urls = list(filter(
        lambda x: start_date <= x.datetime <= end_date,
        article_urls
    ))

    # Sort articles from oldest to newest
    article_urls = list(sorted(
        article_urls,
        key=lambda x: x.datetime
    ))

    links = [article_url.link for article_url in article_urls]

    return links