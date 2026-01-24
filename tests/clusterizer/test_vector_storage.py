import unittest
import numpy as np
from unittest.mock import MagicMock, patch
from scipy.sparse import csr_matrix, issparse
# Ensure VOCAB_SIZE is imported or defined for the test
from src.clusterizer.vector_storage import transpose_elements, form_faiss_index, VOCAB_SIZE


class TestVectorStorage(unittest.TestCase):

    def setUp(self):
        self.dim = 128
        self.vocab = VOCAB_SIZE

        self.id_1 = 101
        self.dense_1 = np.random.rand(self.dim).astype(np.float32).tolist()  # Simulating DB list

        self.sparse_1 = [0.0] * self.vocab
        self.sparse_1[5] = 1.0

        self.id_2 = 102
        self.dense_2 = np.random.rand(self.dim).astype(np.float32).tolist()
        self.sparse_2 = [0.0] * self.vocab
        self.sparse_2[10] = 0.5

        self.articles_attrs = [
            (self.id_1, self.dense_1, self.sparse_1),
            (self.id_2, self.dense_2, self.sparse_2)
        ]

    def test_transpose_elements(self):
        """Checks if lists from DB are correctly converted to matrices."""
        ids, dense_matrix, sparse_matrix = transpose_elements(self.articles_attrs)

        self.assertEqual(ids, [101, 102])

        self.assertIsInstance(dense_matrix, np.ndarray)
        self.assertEqual(dense_matrix.shape, (2, self.dim))
        np.testing.assert_array_almost_equal(dense_matrix[0], np.array(self.dense_1, dtype=np.float32))

        self.assertTrue(issparse(sparse_matrix), "Should be a SciPy sparse matrix")
        self.assertEqual(sparse_matrix.shape, (2, self.vocab))
        self.assertEqual(sparse_matrix[0, 5], 1.0)
        self.assertEqual(sparse_matrix[1, 10], 0.5)

    def test_transpose_elements_empty(self):
        """Checks handling of empty input list and correct default shape."""
        ids, dense, sparse = transpose_elements([])
        self.assertEqual(ids, [])
        self.assertEqual(dense.size, 0)
        self.assertEqual(sparse.shape, (0, self.vocab))

    @patch("src.clusterizer.vector_storage.faiss")
    def test_form_faiss_index(self, mock_faiss):
        ids = np.array([101, 102])
        dense_matrix = np.random.rand(2, 128).astype(np.float32)
        dim = 128

        mock_index_ip = MagicMock()
        mock_index_id = MagicMock()
        mock_faiss.IndexFlatIP.return_value = mock_index_ip
        mock_faiss.IndexIDMap.return_value = mock_index_id

        result = form_faiss_index(ids, dense_matrix, dim)

        mock_faiss.IndexFlatIP.assert_called_once_with(dim)
        mock_index_id.add_with_ids.assert_called_once()
        self.assertEqual(result, mock_index_id)