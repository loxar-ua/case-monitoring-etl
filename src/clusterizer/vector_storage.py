import numpy as np
import re
from scipy.sparse import csr_matrix, spmatrix
from sklearn.preprocessing import normalize
from src.embedder import VOCAB_SIZE
from src.logger import logger


def parse_pgvector_sparse(sparse_data) -> dict:
    """
    Robustly parses any Postgres sparsevec string format using Regex.
    Matches "int:float" patterns directly, ignoring all wrappers/braces.
    """
    if sparse_data is None:
        return {}

    if isinstance(sparse_data, dict):
        return sparse_data

    if isinstance(sparse_data, bytes):
        sparse_data = sparse_data.decode('utf-8')

    if not isinstance(sparse_data, str):
        sparse_data = str(sparse_data)

    try:
        pattern = re.compile(r'(\d+)\s*:\s*([\d\.eE+-]+)')

        matches = pattern.findall(sparse_data)

        if not matches:
            return {}

        return {int(k): float(v) for k, v in matches}

    except Exception as e:
        logger.warning(f"Regex parse failed: {sparse_data[:50]}... Error: {e}")
        return {}


def transpose_elements(articles_attrs: list) -> tuple[np.ndarray, np.ndarray, spmatrix]:
    if not articles_attrs:
        return np.array([], dtype=np.int64), np.array([]), csr_matrix((0, VOCAB_SIZE))

    ids_list = []
    dense_list = []

    all_rows = []
    all_cols = []
    all_data = []

    for local_idx, (art_id, dense, sparse) in enumerate(articles_attrs):
        ids_list.append(art_id)
        dense_list.append(dense)

        # Use Regex parser
        sparse_dict = parse_pgvector_sparse(sparse)

        if sparse_dict:
            for col, val in sparse_dict.items():
                all_rows.append(local_idx)
                all_cols.append(col)
                all_data.append(val)

    ids = np.array(ids_list, dtype=np.int64)
    dense_matrix = np.array(dense_list, dtype=np.float32)

    if not all_data:
        logger.warning("CRITICAL: No sparse data extracted from any article. Check regex logs.")

    sparse_matrix = csr_matrix(
        (all_data, (all_rows, all_cols)),
        shape=(len(ids), VOCAB_SIZE),
        dtype=np.float32
    )

    sparse_matrix = normalize(sparse_matrix, norm='l2', axis=1)
    dense_matrix = normalize(dense_matrix, norm='l2', axis=1)

    return ids, dense_matrix, sparse_matrix


def form_faiss_index(dense_matrix: np.ndarray, dimensionality: int):
    import faiss
    index = faiss.IndexFlatIP(dimensionality)
    index.add(dense_matrix)
    return index
