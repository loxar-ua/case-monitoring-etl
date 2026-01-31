from src.clusterizer.run_clusterizer import run_clusterizer
from src.scrapper.run_scrappers import run_scrappers
from src.scrapper import SCRAPPER_DATE_CONFIG
from src.embedder.run_encoder import run_encoder


def main():

    run_clusterizer()

if __name__ == '__main__':
    main()
