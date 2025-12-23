from typing import Callable, Type, List, Optional
from datetime import datetime

from src.database.models.media import Media
from src.scrapper.scrappers.base_scrapper import BaseScrapper
from src.scrapper.scrappers.sitemap_search import get_links_from_sitemap

FilterFunc = Callable[[List[str]], List[str]]

class GenericScrapper(BaseScrapper):
    SITEMAP_PATTERN: str = None
    ELEMENTS_CFG: dict = None

    LINK_FILTER_FUNC: Optional[FilterFunc] = None

    def __init__(self, media_orm: Media, **kwargs):
        super().__init__(media_orm, **kwargs)
        self.elements_cfg = self.ELEMENTS_CFG

    def get_links(self, start_date: datetime, end_date: datetime) -> list[str] | None:
        links = get_links_from_sitemap(
            sitemap_index_url=self.media_orm.sitemap_index_url,
            sub_sitemaps_pattern=self.SITEMAP_PATTERN,
            start_date=start_date,
            end_date=end_date,
        )

        if not links:
            return None

        if self.LINK_FILTER_FUNC:
            return self.LINK_FILTER_FUNC(links)

        return links

def create_scrapper_class(
        name: str,
        elements_cfg: dict,
        sitemap_pattern: str,
        link_filter_func: Optional[FilterFunc] = None
                            ) -> Type[GenericScrapper]:

    attrs = {
        'ELEMENTS_CFG': elements_cfg,
        'SITEMAP_PATTERN': sitemap_pattern,
        'LINK_FILTER_FUNC': link_filter_func,
    }

    NewScrapperClass = type(name, (GenericScrapper,), attrs)
    return NewScrapperClass