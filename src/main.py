from src.scrapper.run_scrappers import run_scrappers
from src.scrapper import SCRAPPER_DATE_CONFIG
from logger import logger

def main():

    run_scrappers(
        operational_mode=True,
        scrapper_date_config=SCRAPPER_DATE_CONFIG
    )



if __name__ == '__main__':
    main()
