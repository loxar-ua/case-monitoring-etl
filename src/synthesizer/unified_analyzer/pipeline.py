import json
import logging
import re
from pathlib import Path

from src.database.models.article import Article
from src.synthesizer.unified_analyzer.schemas import AnalysisResult, EventItem
from src.utils.build_prompt import build_prompt
from src.synthesizer.llm_service import LLMService

path_file = Path(__file__).resolve().parent
file_prompt = path_file / "prompt.txt"

logger = logging.getLogger(__name__)

class UnifiedAnalyzerPipeline:
    def __init__(self, llm_client: LLMService):
        self.llm_client = llm_client

    @staticmethod
    def build_articles_block(articles: list[Article]) -> str:
        articles_list = [
            {"id": a.id, "title": a.title, "content": (a.content or "")[:300]}
            for a in articles
        ]
        return f"Список статей:\n{json.dumps(articles_list, ensure_ascii=False, indent=2)}"

    def analyze_cluster(self, articles: list[Article]) -> AnalysisResult:
        document = self.build_articles_block(articles)
        prompt = build_prompt(document, file_prompt)

        raw_response = self.llm_client.get_response(prompt)
        if not raw_response:
             raise ValueError("LLM returned None")

        # Handle case where llm_service already returns parsed JSON dictionary
        if isinstance(raw_response, dict):
            payload = raw_response
        else:
            match = re.search(r"\{.*\}", raw_response, re.DOTALL)
            if not match:
                raise ValueError(f"LLM did not return JSON: {raw_response}")
            payload = json.loads(match.group(0))

        events = [
            EventItem(
                event_id=e["event_id"],
                title=e["title"],
                description=e["description"],
                article_ids=e.get("article_ids", [])
            )
            for e in payload.get("events", [])
        ]

        return AnalysisResult(
            is_relevant=bool(payload.get("is_relevant", False)),
            name=str(payload.get("name", "")),
            categories=payload.get("categories", []),
            events=events
        )