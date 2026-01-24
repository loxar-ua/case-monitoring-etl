import faiss
import numpy as np
from scipy.sparse import csr_matrix, spmatrix, vstack
from sklearn.preprocessing import normalize
from src.embedder import VOCAB_SIZE

# file: src/clusterizer/vector_storage.py
import numpy as np
from scipy.sparse import csr_matrix, spmatrix
from sklearn.preprocessing import normalize
from src.embedder import VOCAB_SIZE
from src.logger import logger


def parse_pgvector_string(sparse_str: str) -> dict:
    """
    Parses Postgres sparsevec string: "{50:0.037, 62:0.08}/250002"
    Returns: dict {int: float}
    """
    try:
        if not sparse_str:
            return {}

        # 1. Remove the trailing dimensionality if present (e.g., "/250002")
        if '/' in sparse_str:
            sparse_str = sparse_str.split('/')[0]

        # 2. Strip the curly braces
        sparse_str = sparse_str.strip('{}')

        if not sparse_str:
            return {}

        # 3. Split by comma to get "index:value" pairs
        pairs = sparse_str.split(',')

        result = {}
        for pair in pairs:
            # 4. Split each pair by colon
            idx_str, val_str = pair.split(':')
            result[int(idx_str)] = float(val_str)

        return result

    except Exception as e:
        logger.error(f"Failed to parse sparsevec string: {sparse_str[:20]}... Error: {e}")
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

        # --- PARSING LOGIC START ---
        # Handle the raw string from Postgres
        if isinstance(sparse, str):
            sparse = parse_pgvector_string(sparse)
        # --- PARSING LOGIC END ---

        if sparse and isinstance(sparse, dict):
            for col, val in sparse.items():
                all_rows.append(local_idx)  # Correct local index
                all_cols.append(col)  # Already int from our parser
                all_data.append(val)

    ids = np.array(ids_list, dtype=np.int64)
    # Ensure dense is float32 for FAISS
    dense_matrix = np.array(dense_list, dtype=np.float32)

    sparse_matrix = csr_matrix(
        (all_data, (all_rows, all_cols)),
        shape=(len(ids), VOCAB_SIZE),
        dtype=np.float32
    )

    sparse_matrix = normalize(sparse_matrix, norm='l2', axis=1)
    dense_matrix = normalize(dense_matrix, norm='l2', axis=1)

    return ids, dense_matrix, sparse_matrix

def form_faiss_index(dense_matrix: np.ndarray, dimensionality: int) -> faiss.IndexFlatIP:
    """
    Forms FAISS index from articles' dense embeddings.
    :param articles:
    :return: faiss index
    """

    index = faiss.IndexFlatIP(dimensionality)
    index.add(dense_matrix)

    return index