from src.utils.read_prompt import read_prompt

def build_prompt(document: str, prompt: str):
    file= read_prompt(prompt)
    return file.replace("{{articles}}", document)