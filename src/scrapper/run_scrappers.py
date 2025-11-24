from datetime import datetime, timezone

import src.database.service as db_service
from src.scrapper import ScrapperDateConfig, SCRAPPER_MAP

def run_scrappers(operational_mode: bool, scrapper_date_config: dict[str, ScrapperDateConfig] = None) -> None:
    """Initiates scrappers appropriate to media.
    Searches through sitemaps and scraps all links from time of last
    scrapping to this date. Then takes all this links and parses
    important elements. And then inserts them to database."""

    medias = db_service.get_media()

    for media in medias:
        if not media.name in scrapper_date_config:
            continue

        Scrapper_Class = SCRAPPER_MAP.get(media.name)
        scrapper = Scrapper_Class(media)

        if operational_mode: # Operational mode
            START_DATE = db_service.get_last_published_date(media)
            END_DATE = datetime.now(tz=timezone.utc)
        elif scrapper_date_config: # Base load mode
            START_DATE = scrapper_date_config[media.name].start_date
            END_DATE = scrapper_date_config[media.name].end_date
        else: # Baseload mode, but without date config means no articles will be parsed
            return # TODO: log this

        links = scrapper.get_links(start_date=START_DATE, end_date=END_DATE)

        for link in links:
            article_info = scrapper.parse_article(link)
            db_service.post_article(article_info)