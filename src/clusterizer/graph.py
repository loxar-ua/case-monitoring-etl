import faiss
import numpy as np
from scipy.sparse import csr_matrix, spmatrix
from sknetwork.clustering import Leiden

from src.utils.batcher import batcher

@batcher(1000)
def form_adjancy_relationship(
    size: int,
    ids: np.ndarray,
    dense_chunk: np.ndarray,
    sparse_matrix: spmatrix = None,
    faiss_index: faiss.IndexIDMap = None,
    alpha: float = 0.5,
    min_threshold: float = 0.55,
    k_neighbors: int = 50
):
    sim_dense_batch, target_nodes_batch = faiss_index.search(dense_chunk, k=k_neighbors + 1)

    sim_dense_batch = sim_dense_batch[:, 1:]
    target_nodes_batch = target_nodes_batch[:, 1:]

    sources_repeated = np.repeat(ids, target_nodes_batch.shape[1])
    targets_flat = target_nodes_batch.flatten()

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

    batch_iterator = form_adjancy_relationship(
        n_articles,
        ids,
        dense_matrix,
        sparse_matrix=sparse_matrix,
        faiss_index=faiss_index,
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
    if graph is None:
        return None

    leiden = Leiden(resolution=resolution)

    labels = leiden.fit_predict(graph)

    return labels.tolist()