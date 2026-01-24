import unittest
from unittest.mock import patch, MagicMock
import numpy as np

from src.clusterizer.run_clusterizer import run_clusterizer, ALPHA, MIN_THRESHOLD, K_NEIGHBORS, RESOLUTION
from src.database import ArticleFilter
from src.embedder import DENSE_DIM


class TestRunClusterizer(unittest.TestCase):

    def setUp(self):
        # 1. Start Patches and store mocks in self
        self.mock_get_articles = patch("src.clusterizer.run_clusterizer.get_articles").start()
        self.mock_transpose = patch("src.clusterizer.run_clusterizer.transpose_elements").start()
        self.mock_form_index = patch("src.clusterizer.run_clusterizer.form_faiss_index").start()
        self.mock_build_graph = patch("src.clusterizer.run_clusterizer.build_graph").start()
        self.mock_get_labels = patch("src.clusterizer.run_clusterizer.get_cluster_labels").start()
        self.mock_create_clusters = patch("src.clusterizer.run_clusterizer.create_clusters").start()
        self.mock_assign_clusters = patch("src.clusterizer.run_clusterizer.assign_clusters_to_articles").start()

        # 2. Ensure patches are stopped after every test
        self.addCleanup(patch.stopall)

        # 3. Setup default mock behaviors (Happy Path)
        self.mock_get_articles.return_value = ["dummy_article_data"]

        self.ids = [1, 2]
        self.dense = MagicMock()
        self.sparse = MagicMock()
        self.mock_transpose.return_value = (self.ids, self.dense, self.sparse)

        self.index = MagicMock()
        self.mock_form_index.return_value = self.index

        self.graph = MagicMock()
        self.mock_build_graph.return_value = self.graph

        self.labels = [0, 0]
        self.mock_get_labels.return_value = self.labels

    def test_run_clusterizer_success(self):
        """
        Verifies the full successful execution flow.
        """
        run_clusterizer()

        # Assertions
        self.mock_get_articles.assert_called_once_with(columns=['id', 'dense_embedding', 'sparse_embedding'], filter=ArticleFilter.ENCODED)

        self.mock_transpose.assert_called_once_with(["dummy_article_data"])

        self.mock_form_index.assert_called_once_with(self.ids, self.dense, dimensionality=DENSE_DIM)

        self.mock_build_graph.assert_called_once_with(
            ids=self.ids,
            faiss_index=self.index,
            alpha=ALPHA,
            min_threshold=MIN_THRESHOLD,
            k_neighbors=K_NEIGHBORS,
            dense_matrix=self.dense,
            sparse_matrix=self.sparse,
        )

        self.mock_get_labels.assert_called_once_with(self.graph, resolution=RESOLUTION)

        self.mock_create_clusters.assert_called_once_with(self.labels)
        self.mock_assign_clusters.assert_called_once_with(self.ids, self.labels)

    def test_run_clusterizer_no_articles(self):
        """
        Verifies execution stops early if get_articles returns empty.
        """
        # Override setup behavior
        self.mock_get_articles.return_value = []
        # Update transpose to handle empty input if needed, or assume it won't be called
        self.mock_transpose.return_value = ([], np.array([]), None)

        run_clusterizer()

        self.mock_get_articles.assert_called_once()
        # Verify subsequent steps are NOT called (assuming code handles empty list)
        # If your code calls transpose on empty list, this assertion might need adjustment
        self.mock_form_index.assert_not_called()

    def test_run_clusterizer_graph_failure(self):
        """
        Verifies execution stops if build_graph returns None (no edges).
        """
        self.mock_build_graph.return_value = None

        run_clusterizer()

        self.mock_build_graph.assert_called_once()

        # Should not proceed to clustering or database updates
        # (Assuming you added 'if graph is None: return' in your code)
        self.mock_create_clusters.assert_not_called()
        self.mock_assign_clusters.assert_not_called()


if __name__ == '__main__':
    unittest.main()