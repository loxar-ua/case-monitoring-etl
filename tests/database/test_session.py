from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

import os
import unittest
from unittest import mock

from src.database.session import get_connection, get_session
from tests.base_test import BaseTestCase


@mock.patch.dict(os.environ, {
        "DATABASE_NAME": "test_db",
        "DATABASE_USER": "test_user",
        "DATABASE_PASSWORD": "test_password",
        "DATABASE_HOST": "test_host",
        "DATABASE_PORT": "5432",
        "DATABASE_SSLMODE": "require"})
class TestSessionCase(BaseTestCase):

    def test_get_connection_returns_connection(self):
        """Checks that get_connection returns correct Engine with correct URL"""
        engine = get_connection()
        self.assertIsInstance(engine, Engine)
        self.assertEqual(engine.url.database, "test_db")
        self.assertEqual(engine.url.username, "test_user")
        self.assertEqual(engine.url.password, "test_password")
        self.assertEqual(engine.url.host, "test_host")
        self.assertEqual(engine.url.port, 5432)

    @mock.patch.dict(os.environ, {"DATABASE_NAME": "",})
    def test_get_connection_returns_connection_error(self):
        """Checks that get_connection raises AsssertionError, when there's one of parameters is absent"""
        self.assertRaisesRegex(AssertionError, "One of the parameters is absent", get_connection)

    def test_get_session_returns_session(self):
        """Checks that get_session returns correct session"""
        session = get_session()
        self.assertIsInstance(session, Session)
        self.assertEqual(session.bind.url.database, "test_db")

    def test_get_session_returns_default_url(self):
        """Checks that get_session uses determined url"""
        session = get_session("postgresql://user:pass@localhost/predetermined_db")
        self.assertEqual(session.bind.url.database,  "predetermined_db")


if __name__ == "__main__":
    unittest.main()