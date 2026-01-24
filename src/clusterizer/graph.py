import faiss
import numpy as np
from scipy.sparse import csr_matrix, spmatrix
from sknetwork.clustering import Leiden

from src.logger import logger
from src.utils.batcher import batcher

@batcher(1000)
def form_adjancy_relationship(
    size: int,
    ids: np.ndarray,
    dense_chunk: np.ndarray,
    sparse_matrix: spmatrix,
    faiss_index: faiss.IndexIDMap,
    id_to_idx: dict,
    alpha: float = 0.5,
    min_threshold: float = 0.55,
    k_neighbors: int = 50
):
    sim_dense_batch, target_ids_batch = faiss_index.search(dense_chunk, k=k_neighbors + 1)

    sim_dense_batch = sim_dense_batch[:, 1:]
    target_ids_batch = target_ids_batch[:, 1:]

    map_func = np.vectorize(id_to_idx.get)
    target_indices_batch = map_func(target_ids_batch)

    current_chunk_indices = map_func(ids)

    sources_repeated = np.repeat(current_chunk_indices, target_indices_batch.shape[1])
    targets_flat = target_indices_batch.flatten()

    vecs_target = sparse_matrix[targets_flat]
    vecs_source = sparse_matrix[sources_repeated]

    sim_sparse_flat = np.asarray(vecs_source.multiply(vecs_target).sum(axis=1)).ravel()
    sim_dense_flat = sim_dense_batch.ravel()

    weights_flat = (alpha * sim_sparse_flat) + (1 - alpha) * sim_dense_flat

    mask = weights_flat > min_threshold

    return sources_repeated[mask], targets_flat[mask], weights_flat[mask]


def build_graph(
    faiss_index: faiss.IndexIDMap,
    ids: np.ndarray,
    dense_matrix: np.ndarray,
    sparse_matrix: spmatrix,
    alpha: float,
    min_threshold: float,
    k_neighbors: int
) -> spmatrix | None:

    n_articles = len(ids)

    id_to_idx = {id_val: i for i, id_val in enumerate(ids)}

    batch_iterator = form_adjancy_relationship(
        n_articles,
        ids,
        dense_matrix,
        sparse_matrix=sparse_matrix,
        faiss_index=faiss_index,
        id_to_idx=id_to_idx,
        alpha=alpha,
        min_threshold=min_threshold,
        k_neighbors=k_neighbors,
    )

    results = list(batch_iterator)

    if not results:
        return None

    all_sources_tuple, all_targets_tuple, all_weights_tuple = zip(*results)

    all_sources = np.concatenate(all_sources_tuple)
    all_targets = np.concatenate(all_targets_tuple)
    all_weights = np.concatenate(all_weights_tuple)

    graph = csr_matrix(
        (all_weights, (all_sources, all_targets)),
        shape=(n_articles, n_articles)
    )

    return graph

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