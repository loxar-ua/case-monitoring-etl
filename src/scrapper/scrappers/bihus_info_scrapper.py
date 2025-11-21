from bs4 import BeautifulSoup

from datetime import datetime
import re

from .base_scrapper import BaseScrapper
from src.utils.get_response import get_response
from . import LinkInfo
from ...database.models.media import Media
from .configs import BIHUS_CFG

class BihusInfoScrapper(BaseScrapper):

    def __init__(self, media_orm: Media, **kwargs):
        super().__init__(media_orm, **kwargs)

        self.elements_cfg = BIHUS_CFG

    def get_links(self, start_date: datetime, end_date: datetime) -> list[str] | None:
        """Takes starting and ending date for scraping articles from sitemap_index.xml.
        Using <lastmod> finds what subsitemaps to check.
        Inside subsitemap, using <lastmod> finds what articles to take.
        Returns a list of links."""

        sitemap_index_response = get_response(self.media_orm.sitemap_index_url)
        if sitemap_index_response is None:
            return None

        sitemap_index_soup = BeautifulSoup(sitemap_index_response.content, "lxml-xml")


        sub_sitemap_urls = [LinkInfo(sitemap.find('loc').text,
                                    datetime.fromisoformat(sitemap.find('lastmod').text))
                        for sitemap in sitemap_index_soup.find_all("sitemap")]

        # Filter all unimportant sitemaps, that don't contain articles
        sub_sitemap_urls = list(filter(
            lambda x: re.fullmatch(r"https://bihus.info/post-sitemap\d+\.xml", x.link),
            sub_sitemap_urls
        ))

        combined_sub_sitemap = BeautifulSoup("<urlset></urlset>", "lxml-xml")
        for sub_sitemap_url in sub_sitemap_urls:

            sub_sitemap_response = get_response(sub_sitemap_url.link)

            if sub_sitemap_response is None:
                continue

            sub_sitemap_soup = BeautifulSoup(sub_sitemap_response.content, "lxml-xml")

            for url_tag in sub_sitemap_soup.urlset.find_all(recursive=False):
                combined_sub_sitemap.urlset.append(url_tag)

        article_urls = [LinkInfo(url.find("loc").text,
                                 datetime.fromisoformat(url.find("lastmod").text))
                        for url in combined_sub_sitemap.urlset]

        article_urls = list(filter(
            lambda x: start_date <= x.datetime <= end_date,
            article_urls
        ))

        links = [article_url.link for article_url in article_urls]

        return links