import faiss
import numpy as np
from scipy.sparse import csr_matrix, spmatrix
from sknetwork.clustering import Leiden
from src.logger import logger
from src.utils.batcher import batcher


@batcher(1000)
def form_adjancy_relationship(
        size: int,
        local_indices_chunk: np.ndarray,
        dense_chunk: np.ndarray,
        sparse_matrix: spmatrix,
        faiss_index: faiss.Index,
        alpha: float = 0.5,
        min_threshold: float = 0.55,
        k_neighbors: int = 50
):
    sim_dense_batch, target_indices_batch = faiss_index.search(dense_chunk, k=k_neighbors + 1)

    sim_dense_batch = sim_dense_batch[:, 1:]
    target_indices_batch = target_indices_batch[:, 1:]

    sources_repeated = np.repeat(local_indices_chunk, target_indices_batch.shape[1])
    targets_flat = target_indices_batch.flatten()

    vecs_target = sparse_matrix[targets_flat]
    vecs_source = sparse_matrix[sources_repeated]

    sim_sparse_flat = np.asarray(vecs_source.multiply(vecs_target).sum(axis=1)).ravel()
    sim_dense_flat = sim_dense_batch.ravel()

    weights_flat = (alpha * sim_sparse_flat) + (1 - alpha) * sim_dense_flat
    mask = weights_flat > min_threshold

    logger.info(f"Sample similarity: {weights_flat[:20]}")

    return sources_repeated[mask], targets_flat[mask], weights_flat[mask]


def build_graph(
        faiss_index: faiss.Index,
        dense_matrix: np.ndarray,
        sparse_matrix: spmatrix,
        alpha: float,
        min_threshold: float,
        k_neighbors: int
) -> spmatrix | None:
    n_articles = dense_matrix.shape[0]

    local_indices = np.arange(n_articles)

    batch_iterator = form_adjancy_relationship(
        n_articles,
        local_indices,
        dense_matrix,
        sparse_matrix=sparse_matrix,
        faiss_index=faiss_index,
        alpha=alpha,
        min_threshold=min_threshold,
        k_neighbors=k_neighbors,
    )

    results = list(batch_iterator) if batch_iterator else []
    if not results:
        return None

    all_sources, all_targets, all_weights = map(np.concatenate, zip(*results))

    return csr_matrix((all_weights, (all_sources, all_targets)), shape=(n_articles, n_articles))

def get_cluster_labels(graph: spmatrix, resolution: float) -> list | None:
    if graph is None or graph.nnz == 0:
        logger.info("Graph is empty or has no edges. Every article will be its own cluster.")
        return None

    try:
        leiden = Leiden(resolution=resolution)
        labels = leiden.fit_predict(graph)
        return labels.tolist()
    except ValueError as e:
        logger.error(f"Clustering failed: {e}")
        return None