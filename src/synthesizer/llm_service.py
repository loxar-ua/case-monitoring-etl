import json

from llama_cpp import Llama

from src.logger import logger

class LLMService():
    def __init__(self):
        self.llm = Llama(
            model_path="./models/lapa-v0.1.2-instruct-Q4_K_M.gguf",
            n_gpu_layers=28,
            n_ctx=8192 # Make it higher if you would need.
        )

    def get_response(self, query) -> dict | None:
        response = self.llm.create_chat_completion(
            messages=[{"role": "user", "content": query}],
            response_format={
                "type": "json_object",
            }
        )

        content_str = response["choices"][0]["message"]["content"]

        try:
            return json.loads(content_str)
        except json.JSONDecodeError:
            logger.warning('LLM returned wrong json format')
            return None