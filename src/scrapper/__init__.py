from src.scrapper.scrappers.bihus_info_scrapper import BihusInfoScrapper
from src.scrapper.scrappers.antac_scrapper import AntacScrapper
from collections import namedtuple
from datetime import datetime, timezone

# Is used to connect scrapper class with appropriate media and to keep begin and end dates of articles publishing.
# It's passed to each different scrapper, allowing to scrap different dates.
# Dates aren't used in operational mode.
ScrapperDateConfig = namedtuple(
    "ScrapperDateConfig",
    ['start_date', 'end_date']
)

SCRAPPER_MAP = {
    "Bihus.Info": BihusInfoScrapper,
    "Центр протидії корупції": AntacScrapper,

}

SCRAPPER_DATE_CONFIG = {
    'Центр протидії корупції': ScrapperDateConfig(
        datetime(2022, 10, 28, 23, 23, tzinfo=timezone.utc),
        datetime.now(timezone.utc),
    )
}
