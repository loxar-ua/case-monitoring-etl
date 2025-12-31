from datetime import datetime, timezone
from math import ceil

import src.database.service as db_service
from src.scrapper import ScrapperDateConfig, SCRAPPER_MAP
from src.logger import logger
from src.scrapper.scrappers.base_scrapper import BaseScrapper
from src.utils.batcher import batcher


@batcher(batch_size=100)
def scrap_and_post(size: int, elements: list[str], scrapper: BaseScrapper) -> None:
    article_infos = []
    for link in elements:
        article_info = scrapper.parse_article(link)

        if not article_info:
            continue
        article_infos.append(article_info)

    if article_infos:
        db_service.post_article(article_infos)

def run_scrappers(operational_mode: bool,
                  scrapper_date_config: dict[str, ScrapperDateConfig] = None) -> None:
    """Initiates scrappers appropriate to media.
    Searches through sitemaps and scraps all links from time of last
    scrapping to this date. Then takes all this links and parses
    important elements. And then inserts them to database."""

    logger.info(
        "Starting scrapping. operational_mode = %s",
        operational_mode
    )

    medias = db_service.get_media()

    for media in medias:

        Scrapper_Class = SCRAPPER_MAP[media.name]
        scrapper = Scrapper_Class(media)

        if operational_mode: # Operational mode
            START_DATE = db_service.get_last_published_date(media)
            if not START_DATE:
                START_DATE = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
            END_DATE = datetime.now(tz=timezone.utc)
        else: # Base load mode
            if not media.name in scrapper_date_config:
                logger.error("Media isn't configured in scrapper_date_config")
                continue
            START_DATE = scrapper_date_config[media.name].start_date
            END_DATE = scrapper_date_config[media.name].end_date

        logger.info(
            "Starting scrapping %s. start date = %s, end date = %s",
            media.name, START_DATE, END_DATE
        )
        links = scrapper.get_links(start_date=START_DATE, end_date=END_DATE)
        if not links: continue
        logger.info("Were found %s articles in this time period from this media", len(links))

        links_size = len(links)
        scrap_and_post(links_size, links, scrapper)

    logger.info("End of scrapping")