import faiss
import numpy as np
from scipy.sparse import csr_matrix, spmatrix, vstack

from src.embedder import VOCAB_SIZE


def db_sparse_scipy(sparse_tuple):
    processed_sparse = []
    for s in sparse_tuple:
        if s is None:
            processed_sparse.append(csr_matrix((1, VOCAB_SIZE), dtype=np.float32))
        else:
            try:
                row = csr_matrix(np.array(s, dtype=np.float32), shape=(1, VOCAB_SIZE))
                processed_sparse.append(row)
            except (ValueError, TypeError):
                if isinstance(s, dict):
                    indices = list(s.keys())
                    data = np.array(list(s.values()), dtype=np.float32)
                    indptr = np.array([0, len(indices)])
                    processed_sparse.append(csr_matrix((data, indices, indptr), shape=(1, VOCAB_SIZE)))
                else:
                    processed_sparse.append(csr_matrix((1, VOCAB_SIZE), dtype=np.float32))

    return processed_sparse


def transpose_elements(articles_attrs: list) -> tuple[np.ndarray, np.ndarray, spmatrix]:
    """
    Extracts IDs and dense embeddings from articles' attributes.
    :param articles_attrs:
    :return: tuple of np.ndarrays (ids, dense_matrix)
    """
    if not articles_attrs:
        return [], np.array([]), csr_matrix((0, VOCAB_SIZE))

    ids_tuple, dense_tuple, sparse_tuple = zip(*articles_attrs)

    ids = np.array(ids_tuple, dtype=np.int64)
    dense_matrix = np.array(dense_tuple, dtype=np.float32)

    processed_sparse_list = db_sparse_scipy(sparse_tuple)

    sparse_matrix = vstack(processed_sparse_list, dtype=np.float32)

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