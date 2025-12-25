from datetime import datetime, timezone
from math import ceil

import src.database.service as db_service
from src.scrapper import ScrapperDateConfig, SCRAPPER_MAP
from src.logger import logger

def run_scrappers(operational_mode: bool,
                  scrapper_date_config: dict[str, ScrapperDateConfig] = None,
                  batch_size: int = 100) -> None:
    """Initiates scrappers appropriate to media.
    Searches through sitemaps and scraps all links from time of last
    scrapping to this date. Then takes all this links and parses
    important elements. And then inserts them to database."""

    logger.info(
        "Starting scrapping. operational_mode = %s, batch_size = %s",
        operational_mode, batch_size
    )

    medias = db_service.get_media()

    for media in medias:

        Scrapper_Class = SCRAPPER_MAP[media.name]
        scrapper = Scrapper_Class(media)

        if operational_mode: # Operational mode
            START_DATE = db_service.get_last_published_date(media)
            if not START_DATE:
                START_DATE = datetime(2022, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
            END_DATE = datetime.now(tz=timezone.utc)
        else: # Base load mode
            if not media.name in scrapper_date_config:
                logger.error("Media isn't configer in scrapper_date_config")
                continue
            START_DATE = scrapper_date_config[media.name].start_date
            END_DATE = scrapper_date_config[media.name].end_date

        logger.info(
            "Starting scrapping %s. start date = %s, end date = %s",
            media.name, START_DATE, END_DATE
        )
        links = scrapper.get_links(start_date=START_DATE, end_date=END_DATE)
        if not links: continue

        links_size = len(links)
        chunk_number = ceil(links_size / batch_size)

        for i in range(chunk_number):
            chunk_start = i * batch_size
            chunk_end = min((i + 1) * batch_size, links_size)

            article_infos = []
            for link in links[chunk_start:chunk_end]:
                article_info = scrapper.parse_article(link)

                if not article_info:
                    continue
                article_infos.append(article_info)

            db_service.post_article(article_infos)