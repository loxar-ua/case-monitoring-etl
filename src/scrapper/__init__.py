from src.scrapper.scrappers.bihus_info_scrapper import BihusInfoScrapper
from src.scrapper.scrappers.tyzhden_scrapper import TyzhdenScrapper
from src.scrapper.scrappers.nashi_groshi_scrapper import NashiGroshiScrapper
from src.scrapper.scrappers.chesno_scrapper import ChesnoScrapper
from src.scrapper.scrappers.antac_scrapper import AntacScrapper
from src.scrapper.scrappers.slovo_i_dilo_scrapper import SlovoScrapper

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
    "Український тиждень": TyzhdenScrapper,
    "НАШІ ГРОШІ": NashiGroshiScrapper,
    "Центр протидії корупції": AntacScrapper,
    "Рух Чесно": ChesnoScrapper,
    "Слово і Діло": SlovoScrapper,
}

SCRAPPER_DATE_CONFIG = {
    "Слово і Діло": ScrapperDateConfig(
            datetime(2025, 9, 1, 1, 10, tzinfo=timezone.utc),
            datetime.now(timezone.utc),
        )

}

