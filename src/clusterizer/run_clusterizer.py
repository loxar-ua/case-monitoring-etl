import numpy as np

from src.clusterizer.graph import build_graph, get_cluster_labels
from src.clusterizer.vector_storage import transpose_elements, form_faiss_index
from src.database import ArticleFilter
from src.database.service import get_articles, create_clusters, assign_clusters_to_articles
from src.embedder import DENSE_DIM
from src.logger import logger
import os
from joblib import Memory
from src.database.service import get_articles

cache_dir = './.cache_data'
memory = Memory(cache_dir, verbose=1)

@memory.cache
def get_articles_cached(columns, filter):
    return get_articles(columns=columns, filter=filter)

ALPHA = 0.5
MIN_THRESHOLD = 0.55
K_NEIGHBORS = 50
RESOLUTION = 30

def run_clusterizer():
    articles_attrs = get_articles_cached(
        columns=['id', 'dense_embedding', 'sparse_embedding'],
        filter=ArticleFilter.ENCODED
    )

    if not articles_attrs:
        logger.info("No articles found.")
        return

    ids, dense_matrix, sparse_matrix = transpose_elements(articles_attrs)

    logger.info(f"Dense Matrix Shape: {dense_matrix.shape}")
    logger.info(f"Sparse Matrix NNZ: {sparse_matrix.nnz}")

    faiss_index = form_faiss_index(dense_matrix, dimensionality=DENSE_DIM)

    graph = build_graph(
        faiss_index=faiss_index,
        dense_matrix=dense_matrix,
        sparse_matrix=sparse_matrix,
        alpha=ALPHA,
        min_threshold=MIN_THRESHOLD,
        k_neighbors=K_NEIGHBORS,
    )

    if graph is None:
        logger.info("Graph is empty. Stopping.")
        return

    labels = get_cluster_labels(graph, resolution=RESOLUTION)

    if labels is None:
        return

    unique_cluster_ids = [int(c) for c in set(labels)]
    create_clusters(unique_cluster_ids)

    assign_clusters_to_articles(ids.tolist(), labels)
