import unittest

from datetime import datetime, timezone
from unittest.mock import patch

from src.database.models.article import Article
from src.database.models.media import Media
from src.scrapper import ScrapperDateConfig
from src.scrapper.run_scrappers import run_scrappers
from tests.base_test_db import TestBaseCase
from tests.helpers import create_mock_response

SCRAPPER_DATE_CONFIG = {
    'Bihus.Info': ScrapperDateConfig(
        datetime(2022, 5, 4, 15, 15, tzinfo=timezone.utc),
        datetime(2022, 5, 4, 15, 19, tzinfo=timezone.utc)
    )
}

TEST_URL_1 = "https://bihus.info/rosijski-vijskovi-na-sumshhyni-zahopyly-zhytlovyj-budynok-a-potim-rozstrilyaly-jogo-iz-kulemeta/"
TEST_URL_2 = "https://bihus.info/ne-bulo-ni-zvuku-ni-svystu-vidrazu-pidnyalas-velyka-pylyuka-potim-des-za-2-sekundy-posypalys-vikna-na-zhytomyrshhyni-rosijska-krylata-raketa-rozbyla-shkolu/"


class TestRunScrappersCase(TestBaseCase):

    @patch("src.database.service.get_session")
    @patch('src.utils.get_response.requests.get')
    @patch('src.utils.get_response.random.uniform')
    def test_run_scrappers(self, mock_uniform, mock_get, mock_get_session):
        """Checks whether the scraper works correctly:
        Initiates scrappers appropriate to media.
        Searches through sitemaps and scraps all links from time of last
        scrapping to this date. Then takes all this links and parses
        important elements. And then inserts them to database.
        """

        mock_get.side_effect = create_mock_response
        mock_uniform.return_value = 0
        mock_get_session.return_value = self.session

        media = Media(name='Bihus.Info', sitemap_index_url="https://bihus.info/sitemap_index.xml",
            is_active=True)

        self.session.add(media)
        self.session.flush()

        with patch.object(self.session, 'commit') as mock_commit, \
                patch.object(self.session, 'close') as mock_close:

            run_scrappers(False, SCRAPPER_DATE_CONFIG)

            self.session.flush()

            retrieved = self.session.query(Article).all()

            self.assertEqual(len(retrieved), 2)
            self.assertEqual(retrieved[0].link, TEST_URL_1)
            self.assertEqual(retrieved[1].link, TEST_URL_2)

if __name__ == '__main__':
    unittest.main()