import unittest
import numpy as np
from unittest.mock import MagicMock, patch
from scipy.sparse import csr_matrix, vstack

from src.clusterizer.vector_storage import transpose_elements, form_faiss_index


class TestVectorStorage(unittest.TestCase):

    def setUp(self):
        self.dim = 128
        self.vocab = 100

        self.id_1 = 101
        self.dense_1 = np.random.rand(self.dim).astype(np.float32)
        self.sparse_1 = csr_matrix(([1.0], ([0], [5])), shape=(1, self.vocab))

        self.id_2 = 102
        self.dense_2 = np.random.rand(self.dim).astype(np.float32)
        self.sparse_2 = csr_matrix(([0.5], ([0], [10])), shape=(1, self.vocab))

        self.articles_attrs = [
            (self.id_1, self.dense_1, self.sparse_1),
            (self.id_2, self.dense_2, self.sparse_2)
        ]

    def test_transpose_elements(self):
        """
        Checks if the function correctly unpacks the list of tuples
        into separate structures (list, dense array, stacked sparse matrix).
        """
        ids, dense_matrix, sparse_matrix = transpose_elements(self.articles_attrs)

        self.assertIsInstance(ids, list)
        self.assertEqual(ids, [101, 102])

        self.assertIsInstance(dense_matrix, np.ndarray)
        self.assertEqual(dense_matrix.shape, (2, self.dim))
        np.testing.assert_array_equal(dense_matrix[0], self.dense_1)

        self.assertEqual(sparse_matrix.shape, (2, self.vocab))
        self.assertEqual(sparse_matrix[0, 5], 1.0)
        self.assertEqual(sparse_matrix[1, 10], 0.5)

    def test_transpose_elements_empty(self):
        """Checks handling of empty input list"""
        ids, dense, sparse = transpose_elements([])
        self.assertEqual(ids, [])
        self.assertEqual(dense.size, 0)
        self.assertEqual(sparse.shape, (0, 0))

    @patch("src.clusterizer.vector_storage.faiss")
    def test_form_faiss_index(self, mock_faiss):
        """
        Checks if FAISS index is initialized and populated correctly.
        """
        ids = np.array([101, 102])
        dense_matrix = np.random.rand(2, 128).astype(np.float32)
        dim = 128

        mock_index_ip = MagicMock()
        mock_index_id = MagicMock()

        mock_faiss.IndexFlatIP.return_value = mock_index_ip
        mock_faiss.IndexIDMap.return_value = mock_index_id

        result = form_faiss_index(ids, dense_matrix, dim)

        mock_faiss.IndexFlatIP.assert_called_once_with(dim)
        mock_faiss.IndexIDMap.assert_called_once_with(mock_index_ip)

        args, _ = mock_index_id.add_with_ids.call_args
        passed_matrix, passed_ids = args

        np.testing.assert_array_equal(passed_matrix, dense_matrix)
        np.testing.assert_array_equal(passed_ids, ids)
        self.assertEqual(passed_ids.dtype, np.int64)

        self.assertEqual(result, mock_index_id)


if __name__ == '__main__':
    unittest.main()