from src.clusterizer.graph import build_graph, get_cluster_labels
from src.clusterizer.vector_storage import transpose_elements, form_faiss_index
from src.database import ArticleFilter
from src.database.service import get_articles, create_clusters, assign_clusters_to_articles
from src.embedder import DENSE_DIM
from src.logger import logger

ALPHA = 0.5
MIN_THRESHOLD = 0.55
K_NEIGHBORS = 50
RESOLUTION = 30

def run_clusterizer():

    articles_attrs = get_articles(columns=['id', 'dense_embedding', 'sparse_embedding'], filter=ArticleFilter.ENCODED)

    if not articles_attrs:
        logger.info("No articles found.")
        return

    ids, dense_matrix, sparse_matrix = transpose_elements(articles_attrs)

    faiss_index = form_faiss_index(ids, dense_matrix, dimensionality=DENSE_DIM)

    graph = build_graph(
        ids=ids,
        faiss_index=faiss_index,
        alpha=ALPHA,
        min_threshold=MIN_THRESHOLD,
        k_neighbors=K_NEIGHBORS,
        dense_matrix=dense_matrix,
        sparse_matrix=sparse_matrix,
    )

    if graph is None:
        logger.info("Graph is empty (no sufficient similarities found). Stopping.")
        return

    labels = get_cluster_labels(graph, resolution=RESOLUTION)

    if not labels:
        logger.info("Clustering produced no labels. Stopping.")
        return

    create_clusters(labels)

    assign_clusters_to_articles(ids.tolist(), labels)

