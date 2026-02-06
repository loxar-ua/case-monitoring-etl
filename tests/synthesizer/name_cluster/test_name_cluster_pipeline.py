import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
from collections import defaultdict
import csv

from src.synthesizer.name_cluster.pipeline import NamePipeline
from src.database.models.article import Article
from src.synthesizer.name_cluster.schemas import NameResult

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

class TestNamePipeline(unittest.TestCase):
    def setUp(self):
        self.mock_llm = MagicMock()
        self.pipeline = NamePipeline(llm_client=self.mock_llm)

        self.articles = load_articles_from_csv(CSV_PATH)
        self.clusters = group_by_cluster(self.articles)

    @patch("src.synthesizer.name_cluster.pipeline.build_prompt")
    def test_name_cluster_success(self, mock_build_prompt):
        mock_build_prompt.return_value = "Mocked prompt text"

        self.mock_llm.get_response.return_value = '{"name": "Cluster named"}'

        result: NameResult = self.pipeline.name_cluster(self.articles)

        self.assertIsInstance(result, NameResult)
        self.assertEqual(result.name, "Cluster named")

        mock_build_prompt.assert_called_once()
        self.mock_llm.get_response.assert_called_once_with("Mocked prompt text")

    @patch("src.synthesizer.name_cluster.pipeline.build_prompt")
    def test_name_cluster_invalid_json(self, mock_build_prompt):
        mock_build_prompt.return_value = "Mocked prompt text"
        self.mock_llm.get_response.return_value = "Invalid response"

        with self.assertRaises(ValueError):
            self.pipeline.name_cluster(self.articles)

