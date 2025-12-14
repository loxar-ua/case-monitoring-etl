from src.scrapper.scrappers.all_scrappers import *
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
    "Bihus.Info": BihusScrapper,
    "Український тиждень": TyzhdenScrapper,
    "НАШІ ГРОШІ": NashiGroshiScrapper,
    "Тексти": TextyScrapper,
    "Центр протидії корупції": AntacScrapper,
    "Рух Чесно": ChesnoScrapper,
    "Українська Правда": PravdaScrapper,
    "Громадське": HromadskeScrapper,
    "Бабель": BabelScrapper,

}

SCRAPPER_DATE_CONFIG = {
    "Бабель": ScrapperDateConfig(
            datetime(2025, 9, 10, 7, 50, tzinfo=timezone.utc),
            datetime.now(timezone.utc),
        )
}
