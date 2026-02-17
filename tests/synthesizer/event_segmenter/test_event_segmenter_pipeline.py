import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
from collections import defaultdict
import json
import csv

from src.synthesizer.event_segmenter.pipeline import EventPipeline
from src.database.models.article import Article
from src.synthesizer.event_segmenter.schemas import EventResult

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
            articles.append(
                Article(
                    id=int(row["id"]),
                    title=row["title"],
                    content=row["content"]
                )
            )
    return articles


class TestEventPipeline(unittest.TestCase):
    def setUp(self):
        self.mock_llm = MagicMock()
        self.pipeline = EventPipeline(llm_client=self.mock_llm)

        self.articles = load_articles_from_csv(CSV_PATH)

    @patch("src.synthesizer.event_segmenter.pipeline.build_prompt")
    def test_segment_events_success(self, mock_build_prompt):
        mock_build_prompt.return_value = "Mocked prompt text for events"

        fake_payload = {
            "case_id": 123,
            "events": [
                {
                    "event_id": 1,
                    "title": "Початок подій",
                    "description": "Перша подія у справі.",
                    "article_ids": [1, 2]
                },
                {
                    "event_id": 2,
                    "title": "Затримання",
                    "description": "Друга подія у справі.",
                    "article_ids": [3]
                }
            ]
        }
        self.mock_llm.get_response.return_value = json.dumps(fake_payload)

        test_articles = self.articles[:3] if self.articles else [Article(id=1, title="T", content="C")]

        result = self.pipeline.segment_events(case_id=123, articles=test_articles)

        self.assertIsInstance(result, EventResult)
        self.assertEqual(len(result.events), 2)
        self.assertEqual(result.events[0].title, "Початок подій")
        self.assertEqual(result.events[1].article_ids, [3])

        mock_build_prompt.assert_called_once()
        self.mock_llm.get_response.assert_called_once_with("Mocked prompt text for events")

    @patch("src.synthesizer.event_segmenter.pipeline.build_prompt")
    def test_segment_events_invalid_json(self, mock_build_prompt):
        mock_build_prompt.return_value = "Mocked prompt text"
        self.mock_llm.get_response.return_value = "Error: I cannot process this request."

        test_articles = [Article(id=1, title="Test", content="Content")]

        with self.assertRaises(ValueError):
            self.pipeline.segment_events(case_id=1, articles=test_articles)

    def test_build_articles_block(self):
        test_articles = [
            Article(id=10, title="Заголовок", content="Дуже довгий текст статті...")
        ]
        block = self.pipeline.build_articles_block(case_id=99, articles=test_articles)

        self.assertIn("Case ID: 99", block)
        self.assertIn('"id": 10', block)
        self.assertIn("Заголовок", block)


if __name__ == "__main__":
    unittest.main()