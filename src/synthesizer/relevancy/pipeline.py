import json
import logging
import re

from src.database.models.article import Article
from src.synthesizer.relevancy.schemas import RelevancyResult
from src.synthesizer.relevancy.prompt import build_prompt
#прописати шлях до ллм

logger = logging.getLogger(__name__)

class RelevancyPipeline:
    def __init__(self, llm_client: LLMService):
        self.llm_client = LLMService


    @staticmethod
    def build_articles_block(articles: list[Article]) -> str:
        return "\n".join(
            f"[id]: {a.id}\n"
            f"title: {a.title}\n"
            f"content: {a.content}\n"
            for a in articles
        )

    def relevancy(self, articles: list[Article]) -> RelevancyResult:
        document = self.build_articles_block(articles)
        prompt = build_prompt(document)

        raw_response = self.llm_client.get_response(prompt)

        match = re.search(r"\{.*\}", raw_response, re.DOTALL)
        if not match:
            raise ValueError(f"LLM did not return JSON: {raw_response}")

        payload = json.loads(match.group(0))

        return RelevancyResult(
            is_relevant=bool(payload["is_relevant"])
        )
