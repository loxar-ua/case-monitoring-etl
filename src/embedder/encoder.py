from . import embedding_model

def encode(texts: list[str]) -> dict:
    """
    Encode articles to get dense and sparse embeddings.
    :param texts:
    :return: dict("dense_vecs", "lexical_weights")
    """
    output = embedding_model.encode(
        texts,
        batch_size=12,
        max_length=1024,
        return_dense=True,
        return_sparse=True
    )

    return output