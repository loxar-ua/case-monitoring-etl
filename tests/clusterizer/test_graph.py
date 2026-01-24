import unittest
import numpy as np
from unittest.mock import MagicMock, patch
from scipy.sparse import csr_matrix

from src.clusterizer.graph import form_adjancy_relationship, build_graph, get_cluster_labels
from src.embedder import DENSE_DIM


class TestGraphClustering(unittest.TestCase):

    def setUp(self):
        self.n_articles = 10
        self.ids = np.arange(self.n_articles)
        self.dense_matrix = np.random.rand(self.n_articles, 128).astype(np.float32)

        self.sparse_matrix = csr_matrix(np.eye(self.n_articles), dtype=np.float32)

        self.mock_faiss = MagicMock()

    def test_form_adjancy_relationship_math(self):
        """
        Verifies the math logic:
        Weight = (alpha * sparse) + ((1-alpha) * dense)
        Checks if filtering by min_threshold works.
        """
        chunk_size = 1
        ids_chunk = np.array([0])
        dense_chunk = self.dense_matrix[0:1]

        k_neighbors = 2

        mock_dists = np.array([[1.0, 0.8, 0.2]], dtype=np.float32)
        mock_inds = np.array([[0, 1, 2]], dtype=np.int64)

        self.mock_faiss.search.return_value = (mock_dists, mock_inds)

        rows = np.array([0, 1, 2])
        cols = np.array([0, 0, 0])
        data = np.array([1.0, 0.4, 0.9])

        custom_sparse = csr_matrix((data, (rows, cols)), shape=(3, 1))

        results = form_adjancy_relationship(
            1,
            ids_chunk,
            dense_chunk,
            sparse_matrix=custom_sparse,
            faiss_index=self.mock_faiss,
            alpha=0.5,
            min_threshold=0.5,
            k_neighbors=2
        )

        self.assertTrue(len(results) > 0)
        sources, targets, weights = results[0]

        self.assertEqual(len(weights), 2)

        self.assertIn(1, targets)
        self.assertIn(2, targets)

        expected_w1 = 0.6
        expected_w2 = 0.55

        idx_1 = np.where(targets == 1)[0][0]
        self.assertAlmostEqual(weights[idx_1], expected_w1, places=5)

    @patch("src.clusterizer.graph.form_adjancy_relationship")
    def test_build_graph_aggregation(self, mock_worker):
        """
        Tests that build_graph correctly aggregates chunks from the worker
        and builds a CSR matrix.
        """
        batch_1 = (np.array([0]), np.array([1]), np.array([0.9]))
        batch_2 = (np.array([2]), np.array([3]), np.array([0.8]))

        mock_worker.return_value = [batch_1, batch_2]

        graph = build_graph(
            ids=np.arange(4),
            dense_matrix=np.zeros((4, 10)),
            sparse_matrix=None,
            faiss_index=None,
            alpha=0.5,
            min_threshold=0.5,
            k_neighbors=10
        )

        self.assertIsInstance(graph, csr_matrix)
        self.assertEqual(graph.shape, (4, 4))

        self.assertEqual(graph[0, 1], 0.9)
        self.assertEqual(graph[2, 3], 0.8)
        self.assertEqual(graph[0, 3], 0.0)

    @patch("src.clusterizer.graph.form_adjancy_relationship")
    def test_build_graph_empty_result(self, mock_worker):
        """Tests that build_graph returns None if no relationships found"""
        mock_worker.return_value = []

        graph = build_graph(
            ids=np.arange(5),
            dense_matrix=np.zeros((5, 10)),
            sparse_matrix=None,
            faiss_index=None,
            alpha=0.5,
            min_threshold=0.5,
            k_neighbors=10
        )

        self.assertIsNone(graph)

    @patch("src.clusterizer.graph.Leiden")
    def test_get_cluster_labels(self, mock_leiden_class):
        """Tests the wrapper around sknetwork Leiden"""
        mock_instance = MagicMock()
        mock_leiden_class.return_value = mock_instance
        mock_instance.fit_predict.return_value = np.array([0, 0, 1, 2])

        graph = csr_matrix((4, 4))

        labels = get_cluster_labels(graph, resolution=1.0)

        mock_instance.fit_predict.assert_called_once_with(graph)
        self.assertIsInstance(labels, list)
        self.assertEqual(labels, [0, 0, 1, 2])

    def test_get_cluster_labels_none_input(self):
        """Should return None if graph is None"""
        res = get_cluster_labels(None, resolution=1.0)
        self.assertIsNone(res)


if __name__ == '__main__':
    unittest.main()