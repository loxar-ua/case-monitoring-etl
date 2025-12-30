import unittest

import numpy as np

from src.embedder.encoder import encode
class TestEncoder(unittest.TestCase):
    def test_encoder(self):
        """
        Tests that the encoder returns output of correct structure:
        list of dense embeddings and list of lexical weights.
        """

        texts = [
            "Парламент. Депутати не проголосували за новий законопроєкт.",
            "Митниця. Вилучили велику партію дзигарів 'Парламент'"
        ]

        output = encode(texts)

        self.assertEqual(len(output['dense_vecs']), len(texts))
        for vec in output['dense_vecs']:
            self.assertIsInstance(vec, np.ndarray)
            self.assertEqual(vec.ndim, 1)
            self.assertGreater(len(vec), 0)
            norm = np.linalg.norm(vec)
            self.assertAlmostEqual(norm, 1.0, places=5)

        self.assertEqual(len(output['lexical_weights']), len(texts))
        for lex in output['lexical_weights']:
            self.assertIsInstance(lex, dict)
            self.assertGreater(len(lex), 0)








