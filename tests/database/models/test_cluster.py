from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

import unittest
from datetime import datetime

from src.database.models.article import Article
from src.database.models.base import Base
from src.database.models.cluster import Cluster
from src.database.session import get_connection


class TestClusterCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = get_connection("postgresql+psycopg2://postgres:pass@localhost:5432/test_db")
        with cls.engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
            conn.commit()

        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(cls.engine)
        cls.engine.dispose()

    def setUp(self):
        self.session = self.Session()
        self.transaction = self.session.begin_nested()

    def tearDown(self):
        self.transaction.rollback()
        self.session.close()

    def test_cluster_creation(self):
        """Check that the cluster record is created correctly."""
        cluster = Cluster(name = "cluster")
        self.session.add(cluster)

        retrieved = self.session.query(Cluster).first()

        self.assertEqual(retrieved.name, "cluster")
        self.assertEqual(repr(retrieved), "<Cluster 'cluster'>")

    def test_cluster_relationship(self):
        """Check that the cluster relationship is created correctly."""
        cluster = Cluster(name = "cluster" )

        self.session.add(cluster)
        self.session.flush()

        article = Article(
            title="title",
            link="link",
            featured_image_url="image_url",
            author="author",
            content="content",
            published_at=datetime.now(),
            cluster_id=cluster.id,
        )

        self.session.add(article)

        retrieved = self.session.query(Cluster).first()

        self.assertIsNotNone(retrieved.articles[0])
        self.assertEqual(retrieved.articles[0].title, "title")


if __name__ == "__main__":
    unittest.main()