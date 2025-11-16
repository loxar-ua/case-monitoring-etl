import requests
from bs4 import BeautifulSoup

from datetime import datetime, timezone
from collections import namedtuple
import re

from .base_scrapper import BaseScrapper
from src.utils.get_response import get_response
from src.utils.normalize_text import normalize_text

class BihusInfoScrapper(BaseScrapper):

    def get_links(self, start_date: datetime, end_date: datetime) -> list[str] | None:
        """Takes starting and ending date for scraping articles from sitemap_index.xml.
        Using <lastmod> finds what subsitemaps to check.
        Inside subsitemap, using <lastmod> finds what articles to take.
        Returns a list of links."""

        sitemap_index_response = get_response(self.media_orm.sitemap_index_url)
        if sitemap_index_response is None:
            return None

        sitemap_index_soup = BeautifulSoup(sitemap_index_response.content, "lxml-xml")

        LinkInfo = namedtuple('LinkInfo', ['link', 'datetime'])

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

    def _get_article_soup(self, link: str) -> BeautifulSoup:
        """Takes link of article and returns the content of articles as BeautifulSoup object."""

        article_response = get_response(link)
        article_soup = BeautifulSoup(article_response.content, "html.parser")

        return article_soup

    def _get_featured_image_url(self, article_soup: BeautifulSoup) -> str | None:
        """Takes content of article in form of soup and returns featured image url."""

        featured_image_url = article_soup.find(
            name='meta',
            attrs={'property': 'og:image'}
        )

        if featured_image_url:
            featured_image_url = str(featured_image_url['content'])
        else:
            featured_image_url = None

        return featured_image_url

    def _get_title(self, article_soup: BeautifulSoup) -> str | None:
        """Takes content of article in form of soup and returns title."""

        title = article_soup.find(
            name='meta',
            attrs={'property': 'og:title'}
        )

        if title:
            title = str(title['content'])
        else:
            title = None

        return title

    def _get_author(self, article_soup: BeautifulSoup) -> str | None:
        """Takes content of article in form of soup and returns title."""

        author = article_soup.find(
            name='meta',
            attrs={'name': 'author'}
        )

        if author:
            author = str(author['content'])
        else:
            author = None

        return author

    def _get_published_at(self, article_soup: BeautifulSoup) -> datetime | None:
        """Takes content of article in form of soup and returns published date."""

        published_at = article_soup.find(
            name='meta',
            attrs={'property': 'article:published_time'}
        )

        if published_at:
            published_at = datetime.fromisoformat(published_at['content'])
        else:
            published_at = None

        return published_at


    def _get_content(self, article_soup: BeautifulSoup) -> str | None:
        """Takes content of article in form of soup and returns normalised content."""

        content = article_soup.find('div', attrs={'class': 'bi-single-content'})

        if not content:
            return None

        return normalize_text(content)
