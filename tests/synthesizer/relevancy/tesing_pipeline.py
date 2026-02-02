from collections import defaultdict
import csv
from pathlib import Path
import unittest
from unittest.mock import MagicMock

from tests.synthesizer.relevancy.schemas import Article
from src.synthesizer.relevancy.pipeline import RelevancyPipeline
from src.synthesizer.relevancy.schemas import RelevancyResult

BASE_PATH = Path(__file__).resolve().parent
FIXTURES_PATH = BASE_PATH.parent.parent / "fixtures" / 'relevancy'
CSV_PATH = FIXTURES_PATH / "data_updated.csv"


def load_articles_from_csv(path: str) -> list[Article]:
    articles = []

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            raw_cluster = row.get("predicted_cluster", "").strip()

            if not raw_cluster:
                continue

            articles.append(
                Article(
                    id=int(row["id"]),
                    title=row["title"],
                    content=row["content"],
                    cluster_id=int(float(raw_cluster)),
                )
            )

    return articles



def group_by_cluster(articles: list[Article]) -> dict[int, list[Article]]:
    clusters = defaultdict(list)

    for article in articles:
        clusters[article.cluster_id].append(article)

    return clusters




class TestRelevancyPipeline(unittest.TestCase):
    def setUp(self):
        self.mock_llm = MagicMock()
        self.pipeline = RelevancyPipeline(llm_client=self.mock_llm)

        articles = load_articles_from_csv(CSV_PATH)
        self.clusters = group_by_cluster(articles)

    def test_relevancy_true(self):
        self.mock_llm.get_response.return_value = '{"is_relevant": true}'

        result = self.pipeline.relevancy(self.articles)

        self.assertIsInstance(result, RelevancyResult)
        self.assertTrue(result.is_relevant)
        self.mock_llm.get_response.assert_called_once()

    def test_relevancy_false(self):
        self.mock_llm.get_response.return_value = '{"is_relevant": false}'

        result = self.pipeline.relevancy(self.articles)

        self.assertFalse(result.is_relevant)
