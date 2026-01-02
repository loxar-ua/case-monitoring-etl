import numpy as np
from scipy.sparse import csr_matrix
from sklearn.preprocessing import normalize

from src.database.models.article import Article
from src.database.service import get_articles, update_articles
from src.embedder import VOCAB_SIZE
from src.embedder.encoder import encode
from src.utils.batcher import batcher
from src.logger import logger


def get_text(article: Article) -> str:
    return article.title + ". " + article.content

def dict_to_csr(sparse_dict: dict) -> csr_matrix:
    length = len(sparse_dict)
    data = list(sparse_dict.values())
    cols = list(sparse_dict.keys())
    rows = np.zeros(length)

    return csr_matrix((data, (rows, cols)), shape=(1, VOCAB_SIZE), dtype=float)

@batcher(2000)
def encode_and_update(size: int, elements: list[Article]) -> None:

    texts = list(map(get_text, elements))
    output = encode(texts)

    dense_embeddings = output["dense_vecs"]
    sparse_embeddings = list(
        map(lambda x: normalize(x, norm='l2'),
            map(dict_to_csr, output["lexical_weights"])
            )
    )

    for i in range(size):
        article = elements[i]
        article.dense_embedding = dense_embeddings[i]
        article.sparse_embedding = sparse_embeddings[i]

    update_articles(elements)


def run_encoder():
    """
    Fetches articles from db that don't have embeddings.
    Creates and normalizes embeddings for each article.
    Updates articles in db with new embeddings.
    """
    logger.info("Starting encoder")
    articles = get_articles(True)
    size = len(articles)

    encode_and_update(size, articles)

    logger.info("End of encoding")