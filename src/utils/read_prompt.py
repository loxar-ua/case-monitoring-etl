def read_prompt(document:str):
    with open(document, "r", encoding="utf-8") as f:
        return f.read()