import faiss
import numpy as np
from scipy.sparse import csr_matrix, spmatrix, vstack

from src.embedder import VOCAB_SIZE

def db_sparse_scipy(sparse_tuple: tuple) -> spmatrix:
    processed_sparse = []
    for s in sparse_tuple:
        if s is None:
            processed_sparse.append(csr_matrix((1, VOCAB_SIZE)))
        elif isinstance(s, dict):
            indices = list(s.keys())
            data = list(s.values())
            indptr = [0, len(indices)]
            processed_sparse.append(csr_matrix((data, indices, indptr), shape=(1, VOCAB_SIZE)))
        else:
            processed_sparse.append(csr_matrix(s, shape=(1, VOCAB_SIZE)))

    sparse_matrix = vstack(processed_sparse, dtype=np.float32)

    return sparse_matrix


def transpose_elements(articles_attrs: list) -> tuple[list, np.ndarray, spmatrix]:
    """
    Extracts IDs and dense embeddings from articles' attributes.
    :param articles_attrs:
    :return: tuple of np.ndarrays (ids, dense_matrix)
    """
    if not articles_attrs:
        return [], np.array([]), csr_matrix((0, VOCAB_SIZE))

    ids_tuple, dense_tuple, sparse_tuple = zip(*articles_attrs)

    ids = list(ids_tuple)
    dense_matrix = np.array(dense_tuple, dtype=np.float32)

    sparse_matrix = db_sparse_scipy(sparse_tuple)

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