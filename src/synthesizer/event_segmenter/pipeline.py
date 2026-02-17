import json
import logging
import re
from pathlib import Path

from src.database.models.article import Article
from src.synthesizer.event_segmenter.schemas import EventResult, EventItem
from src.utils.build_prompt import build_prompt
from src.synthesizer.llm_service import LLMService

path_file = Path(__file__).resolve().parent
file_prompt = path_file / "prompt.txt"

logger = logging.getLogger(__name__)


class EventPipeline:
    def __init__(self, llm_client: LLMService):
        self.llm_client = llm_client

    @staticmethod
    def build_articles_block(case_id: int, articles: list[Article]) -> str:
        articles_list = [
            {"id": a.id, "title": a.title, "content": (a.content or "")[:300]}
            for a in articles
        ]
        return f"Case ID: {case_id}\nСписок статей:\n{json.dumps(articles_list, ensure_ascii=False, indent=2)}"

    def segment_events(self, case_id: int, articles: list[Article]) -> EventResult:
        document = self.build_articles_block(case_id, articles)
        prompt = build_prompt(document, file_prompt)

        raw_response = self.llm_client.get_response(prompt)

        match = re.search(r"\{.*\}", raw_response, re.DOTALL)
        if not match:
            logger.error(f"Failed to find JSON in LLM response: {raw_response}")
            raise ValueError("LLM returned malformed data")

        payload = json.loads(match.group(0))

        events = [
            EventItem(
                event_id=e["event_id"],
                title=e["title"],
                description=e["description"],
                article_ids=e["article_ids"]
            )
            for e in payload.get("events", [])
        ]

        return EventResult(
            case_id=payload.get("case_id", case_id),
            events=events
        )