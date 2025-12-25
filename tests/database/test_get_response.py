import unittest
from unittest.mock import patch, MagicMock
import requests

from tests.base_test import BaseTestCase
from tests.helpers import create_mock_response
from src.database.get_response import get_response, HEADERS, TIMEOUT

TEST_URL = "https://example.com"

class TestGetResponseCase(BaseTestCase):

    @patch('src.database.get_response.requests.get')
    @patch('src.database.get_response.random.uniform')
    def test_get_response_with_success(self, mock_uniform, mock_get):
        """This test checks whether get_response function
        will handle successful request correctly"""

        mock_uniform.return_value = 0

        mock_response = MagicMock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.text = "<html>This is the page content</html>"

        mock_get.return_value = mock_response

        response = get_response(TEST_URL)

        mock_get.assert_called_once_with(url=TEST_URL, headers=HEADERS, timeout=TIMEOUT)
        self.assertEqual(response.text, mock_response.text)

    @patch('src.database.get_response.requests.get')
    @patch('src.database.get_response.random.uniform')
    def test_get_response_block(self, mock_uniform, mock_get):
        """This test checks whether get_response function
         will handle block correctly"""

        mock_uniform.return_value = 0
        mock_get.side_effect = create_mock_response

        response = get_response("https://bihus.info/afdsfsdf")

        self.assertEqual(response, None)

    @patch('src.database.get_response.requests.get')
    @patch('src.database.get_response.random.uniform')
    def test_get_response_error(self, mock_uniform, mock_get):
        """This test checks whether get_response function
        will handle different error types correctly"""

        mock_uniform.return_value = 0

        exceptions_to_test = [
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.RequestException
        ]

        for exception_to_raise in exceptions_to_test:

            mock_get.reset_mock()
            mock_get.side_effect = exception_to_raise

            response = get_response(TEST_URL)

            mock_get.assert_called_once_with(url=TEST_URL, headers=HEADERS, timeout=TIMEOUT)
            self.assertEqual(response, None)


if __name__ == '__main__':
    unittest.main()