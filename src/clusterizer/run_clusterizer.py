from src.clusterizer.graph import build_graph, get_cluster_labels
from src.clusterizer.vector_storage import transpose_elements, form_faiss_index
from src.database import ArticleFilter
from src.database.service import get_articles, create_clusters, assign_clusters_to_articles
from src.embedder import DENSE_DIM

ALPHA = 0.5
MIN_THRESHOLD = 0.55
K_NEIGHBORS = 50
RESOLUTION = 30

def run_clusterizer():

    artices_attrs = get_articles(columns=['id', 'dense_embedding', 'sparse_embedding'])

    ids, dense_matrix, sparse_matrix = transpose_elements(artices_attrs)

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

    labels = get_cluster_labels(graph, resolution=RESOLUTION)

    create_clusters(labels)

    assign_clusters_to_articles(ids, labels)

