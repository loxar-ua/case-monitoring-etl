from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from testcontainers.postgres import PostgresContainer

import unittest

from src.database.models.base import Base
from src.database.session import get_connection

class TestBaseCase(unittest.TestCase):
    postgres: PostgresContainer = None
    engine = None
    Session = None

    @classmethod
    def setUpClass(cls):
        """Starts Docker container with Postgres instance, and starts new Session"""
        cls.postgres = PostgresContainer('pgvector/pgvector:pg16')
        cls.postgres.start()

        psql_url = cls.postgres.get_connection_url()
        cls.engine = get_connection(psql_url)

        with cls.engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
            conn.commit()

        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    @classmethod
    def tearDownClass(cls):
        """Deletes all tables, stops engine and stops Docker
        container with Postgres instance"""
        Base.metadata.drop_all(cls.engine)

        if cls.engine:
            cls.engine.dispose()

        if cls.postgres:
            cls.postgres.stop()

    def setUp(self):
        """Starts new session and creates transaction,
        for future rollback of all changes in test function"""
        self.session = self.Session()
        self.transaction = self.session.begin_nested()

    def tearDown(self):
        """Rollbacks transaction and closes session after work of each test"""
        self.transaction.rollback()
        self.session.close()