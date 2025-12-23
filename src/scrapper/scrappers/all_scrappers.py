from src.scrapper.scrappers.generic_scrapper import create_scrapper_class
from src.scrapper.configs import *

#pravda
@staticmethod
def pravda_link_filter(links: list[str], *args, **kwargs) -> list[str]:
    return [
        link for link in links
        if "/news/" in link and "/rus/" not in link and "/eng/" not in link
    ]
PravdaScrapper = create_scrapper_class(
    name="PravdaScrapper",
    elements_cfg=PRAVDA_CFG,
    sitemap_pattern=r"https://www\.pravda\.com\.ua/sitemap/sitemap-(202[5-9]|20[3-9]\d)-\d{2}\.xml\.gz",
    link_filter_func=pravda_link_filter
)

#antac
AntacScrapper = create_scrapper_class(
    name="AntacScrapper",
    elements_cfg=ANTAC_CFG,
    sitemap_pattern=r"https://antac.org.ua/news-sitemap\d+\.xml",
)

#babel
BabelScrapper = create_scrapper_class(
    name="BabelScrapper",
    elements_cfg=BABEL_CFG,
    sitemap_pattern=r"https://babel\.ua/ukrainian/default/2025/(0[1-9]|1[0-1])-(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])\.xml",
)

# bihus
BihusScrapper = create_scrapper_class(
    name="BihusScrapper",
    elements_cfg=BIHUS_CFG,
    sitemap_pattern=r"https://bihus.info/post-sitemap\d+\.xml",
)

ChesnoScrapper = create_scrapper_class(
    name="ChesnoScrapper",
    elements_cfg=CHESNO_CFG,
    sitemap_pattern=r"https://www.chesno.org/sitemap-posts.xml"
)

#hromadske
@staticmethod
def hromadske_link_filter(links: list[str], *args, **kwargs) -> list[str]:
    return [link for link in links
            if  "/ru/" not in link and "/en/" not in link
            ]

HromadskeScrapper = create_scrapper_class(
    name="HromadskeScrapper",
    elements_cfg= HROMADSKE_CFG,
    sitemap_pattern=r"https://hromadske\.ua/sitemaps/posts/(202[5-9]|20[3-9]\d)/(0?[1-9]|1[0-2])\.xml",
    link_filter_func=hromadske_link_filter
)

#nashigroshi
NashiGroshiScrapper = create_scrapper_class(
    name="NashiGroshiScrapper",
    elements_cfg= GROSHI_CFG,
    sitemap_pattern=r"https://nashigroshi\.org/sitemap-pt-post-(202[5-9]|20[3-9]\d)-\d{2}\.xml"
)
#texty

TextyScrapper = create_scrapper_class(
    name="TextyScrapper",
    elements_cfg= TEXTY_CFG,
    sitemap_pattern=r"https://texty.org.ua/sitemap-articles.xml",
)

#tyzhden
TyzhdenScrapper = create_scrapper_class(
    name="TyzhdenScrapper",
    elements_cfg= TYZHDEN_CFG,
    sitemap_pattern=r"https://tyzhden.ua/wp-sitemap-posts-post-(12[4-9]|1[3-9]\d+|[2-9]\d+)\.xml",
)
#Espreso

EspresoScrapper = create_scrapper_class(
    name="EspresoScrapper",
    elements_cfg= ESPRESDO_CFG,
    sitemap_pattern=r"https://espreso.tv/sitemap_news_1.xml",

)

#Radio Svoboda

RadioSvobodaScrapper = create_scrapper_class(
    name="RadioSvobodaScrapper",
    elements_cfg= SVOBODA_CFG,
    sitemap_pattern=r"https://www.radiosvoboda.org/sitemap_9_latest.xml.gz",
)

#Suspilne

SuspilneScrapper = create_scrapper_class(
    name="SuspilneScrapper",
    elements_cfg= SUSPILNE_CFG,
    sitemap_pattern=r"https://suspilne.media/suspilne/sitemap/post-sitemap\d+\.xml",
)