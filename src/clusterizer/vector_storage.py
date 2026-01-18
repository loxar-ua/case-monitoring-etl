import faiss
import numpy as np
from scipy.sparse import csr_matrix


def transpose_elements(articles_attrs: list) -> tuple[np.ndarray, np.ndarray, csr_matrix]:
    """
    Extracts IDs and dense embeddings from articles' attributes.
    :param articles_attrs:
    :return: tuple of np.ndarrays (ids, dense_matrix)
    """
    ids_tuple, dense_tuple, sparse_tuple = zip(*articles_attrs)

    ids = np.array(ids_tuple, dtype=np.int64)
    dense_matrix = np.array(dense_tuple, dtype=np.float32)
    sparse_matrix = csr_matrix(csr_matrix, dtype=np.float32)

    return ids, dense_matrix, sparse_matrix

def form_faiss_index(ids: np.ndarray, dense_matrix: np.ndarray, dimensionality: int) -> faiss.IndexIDMap:
    """
    Forms FAISS index from articles' dense embeddings.
    :param articles:
    :return: faiss index
    """

    indexIP = faiss.IndexFlatIP(dimensionality)
    indexID = faiss.IndexIDMap(indexIP)

    indexID.add_with_ids(dense_matrix, ids)

    return indexID