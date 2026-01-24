import unittest
import numpy as np
from unittest.mock import MagicMock, patch
from scipy.sparse import csr_matrix, issparse
# Ensure VOCAB_SIZE is imported or defined for the test
from src.clusterizer.vector_storage import transpose_elements, form_faiss_index, VOCAB_SIZE, db_sparse_scipy

class TestDbSparseScipy(unittest.TestCase):

    def test_valid_list_input(self):
        """Tests standard list of floats (common DB return)."""
        data = [[0.1, 0.0, 0.5] + [0.0] * (VOCAB_SIZE - 3)]
        result = db_sparse_scipy(data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].dtype, np.float32)
        self.assertEqual(result[0].shape, (1, VOCAB_SIZE))

    def test_dictionary_format(self):
        """Tests pgvector SPARSEVEC dict format {index: value}."""
        sparse_dict = {5: 1.2, 10: 0.5}
        result = db_sparse_scipy([sparse_dict])
        self.assertEqual(result[0][0, 5], 1.2)
        self.assertEqual(result[0][0, 10], 0.5)
        self.assertEqual(result[0].shape, (1, VOCAB_SIZE))

    def test_none_handling(self):
        """Tests if None values are converted to zero-rows instead of crashing."""
        result = db_sparse_scipy([None])
        self.assertEqual(result[0].nnz, 0) # Number of non-zeros should be 0
        self.assertEqual(result[0].shape, (1, VOCAB_SIZE))

    def test_mixed_types_and_strings(self):
        """
        Tests the 'dtype object' fix.
        DBs sometimes return numbers as strings or mixed ints/floats.
        """
        # A list containing a string number and an int
        dirty_data = [["0.5", 1, 0] + [0] * (VOCAB_SIZE - 3)]
        result = db_sparse_scipy(dirty_data)
        self.assertEqual(result[0].dtype, np.float32)
        self.assertAlmostEqual(result[0][0, 0], 0.5)

    def test_incompatible_garbage_data(self):
        """Tests if completely invalid data (like a string) defaults to a zero row."""
        result = db_sparse_scipy(["not_a_vector"])
        self.assertEqual(result[0].shape, (1, VOCAB_SIZE))
        self.assertEqual(result[0].nnz, 0)

    def test_empty_input(self):
        """Tests empty list input."""
        result = db_sparse_scipy([])
        self.assertEqual(result, [])

class TestVectorStorage(unittest.TestCase):

    def setUp(self):
        self.dim = 128
        self.vocab = VOCAB_SIZE

        self.id_1 = 101
        self.dense_1 = np.random.rand(self.dim).astype(np.float32).tolist()  # Simulating DB list

        self.sparse_1 = [float(0)] * self.vocab
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

        self.assertIsInstance(ids, np.ndarray)
        self.assertEqual(ids.dtype, np.int64)
        np.testing.assert_array_equal(ids, [101, 102])

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

if __name__ == "__main__":
    unittest.main()