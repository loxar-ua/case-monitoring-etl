# src/utils/get_text_pravda.py
from bs4 import BeautifulSoup

def article_text(html_content: str) -> str:
    """
    Витягує текст статті з контейнера <div class="post_news_text">,
    збирає всі <p> та <li> всередині і повертає один текст.
    """
    soup = BeautifulSoup(html_content, "lxml")

    # Знаходимо контейнер статті
    container = soup.find("div", {"data-io-article-url": True, "class": "post_news_text"})
    if not container:
        return ""

    texts = []

    # Збираємо всі абзаци <p> та елементи списків <li>
    for tag in container.find_all(["p", "li"], recursive=True):
        text = tag.get_text(strip=True)
        if text:
            texts.append(text)

    # Об'єднуємо в один текст із абзацами
    return "\n\n".join(texts)
