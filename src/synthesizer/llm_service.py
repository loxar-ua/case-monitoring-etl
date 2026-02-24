import json
import os
from google import genai
from google.genai import types

from src.logger import logger


class LLMService():
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing")

        self.client = genai.Client(api_key=api_key)

    def get_response(self, query: str) -> dict | None:
        try:
            logger.info(f"Passing query to llm: {query}")
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=query,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                )
            )

            content_str = response.text
            json_content = json.loads(content_str)

            logger.info(f"Getting response from llm: {json_content}")
            return json_content

        except json.JSONDecodeError:
            logger.warning('LLM returned wrong json format')
            return None
        except Exception as e:
            logger.error(f"API request failed: {e}")
            return None