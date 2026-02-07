import sys
from unittest.mock import MagicMock

sys.modules["llama_cpp"] = MagicMock()

import unittest
from unittest.mock import patch
from pathlib import Path
from collections import defaultdict
import csv

from src.synthesizer.cluster_category.pipeline import CategoryPipeline
from src.database.models.article import Article
from src.synthesizer.cluster_category.schemas import CategoryResult

BASE_PATH = Path(__file__).resolve().parent
FIXTURES_PATH = BASE_PATH.parent.parent / "fixtures" / 'relevancy'
CSV_PATH = FIXTURES_PATH / "data_updated.csv"


def load_articles_from_csv(path: str) -> list[Article]:
    articles = []

    if not Path(path).exists():
        return []

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


class TestCategoryPipeline(unittest.TestCase):
    def setUp(self):
        self.mock_llm = MagicMock()
        self.pipeline = CategoryPipeline(llm_client=self.mock_llm)

        self.articles = load_articles_from_csv(CSV_PATH)
        self.clusters = group_by_cluster(self.articles)

    @patch("src.synthesizer.cluster_category.pipeline.build_prompt")
    def test_categorize_cluster_success(self, mock_build_prompt):
        # Якщо CSV немає або він порожній, використовуємо фейкові дані
        if not self.clusters:
            print("WARNING: CSV not found or empty. Using fake data.")
            test_articles = [Article(id=1, title="Test", content="Content", cluster_id=1)]
        else:
            first_cluster_id = list(self.clusters.keys())[0]
            test_articles = self.clusters[first_cluster_id]

        mock_build_prompt.return_value = "Mocked prompt text"

        self.mock_llm.get_response.return_value = '{ "categories": ["Війна", "Корупція"] }'

        result: CategoryResult = self.pipeline.categorize_cluster(test_articles)

        self.assertIsInstance(result, CategoryResult)
        self.assertEqual(result.categories, ["Війна", "Корупція"])

        mock_build_prompt.assert_called_once()
        self.mock_llm.get_response.assert_called_once_with("Mocked prompt text")

    @patch("src.synthesizer.cluster_category.pipeline.build_prompt")
    def test_categorize_cluster_invalid_json(self, mock_build_prompt):
        if not self.clusters:
            test_articles = [Article(id=1, title="Test", content="Content", cluster_id=1)]
        else:
            first_cluster_id = list(self.clusters.keys())[0]
            test_articles = self.clusters[first_cluster_id]

        mock_build_prompt.return_value = "Mocked prompt text"
        self.mock_llm.get_response.return_value = "Invalid response not JSON"

        with self.assertRaises(ValueError):
            self.pipeline.categorize_cluster(test_articles)