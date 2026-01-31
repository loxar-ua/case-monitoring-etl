import json
import logging
import re
from pathlib import Path


from src.database.models.article import Article
from src.synthesizer.name_cluster.schemas import NameResult
from src.utils.build_prompt import build_prompt
#прописати шлях до ллм

path_file=Path(__file__).resolve().parent
file_prompt= "prompt.txt"
logger = logging.getLogger(__name__)

class NamePipeline:
    def __init__(self, llm_client: LLMService):
        self.llm_client = llm_client


    @staticmethod
    def build_articles_block(articles: list[Article]) -> str:
        return "\n".join(
            f"[id]: {a.id}\n"
            f"title: {a.title}\n"
            f"content: {a.content}\n"
            for a in articles
        )

    def name_cluster(self, articles: list[Article]) -> NameResult:
        document = self.build_articles_block(articles)
        prompt = build_prompt(document, file_prompt)

        raw_response = self.llm_client.get_response(prompt)

        match = re.search(r"\{.*\}", raw_response, re.DOTALL)
        if not match:
            raise ValueError(f"LLM did not return JSON: {raw_response}")

        payload = json.loads(match.group(0))

        return NameResult(
            name=str(payload["name"])
        )
