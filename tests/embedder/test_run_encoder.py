import unittest
from datetime import datetime, timezone
from unittest.mock import patch

from src.database.models.article import Article
from src.embedder import DENSE_DIM, VOCAB_SIZE
from src.embedder.run_encoder import run_encoder
from tests.base_test_db import BDTestCase

date = datetime(2022, 5, 4, 15, 19, tzinfo=timezone.utc)

class TestRunEncoder(BDTestCase):
    @patch("src.database.service.get_session")
    def test_run_encoder(self, mock_get_session):
        """
        Checks whether run_encoder correctly executes all steps:
        Fetches articles from db that don't have embeddings.
        Creates and normalizes embeddings for each article.
        Updates articles in db with new embeddings.
        """

        mock_get_session.return_value = self.session

        articles = [
            Article(
                link="link1",
                title="Парламент",
                content="Депутати не проголосували за новий законопроєкт.",
                published_at=date
            ),
            Article(
                link="link2",
                title="Митниця",
                content="Вилучили велику партію дзигарів \"Парламент\"",
                published_at=date
            )
        ]

        self.session.add_all(articles)
        self.session.flush()

        with patch.object(self.session, 'close'):
            run_encoder()
        self.session.flush()

        retrieved_articles = self.session.query(Article)

        for article in retrieved_articles:
            dense, sparse = article.dense_embedding, article.sparse_embedding
            self.assertIsNotNone(dense)
            self.assertIsNotNone(sparse)
            self.assertEqual(len(dense), DENSE_DIM)
            self.assertEqual(sparse.dimensions(), VOCAB_SIZE)

if __name__ == '__main__':
    unittest.main()

