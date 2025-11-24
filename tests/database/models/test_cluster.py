import unittest
from datetime import datetime

from src.database.models.article import Article
from src.database.models.cluster import Cluster
from tests.base_test_db import TestBaseCase

class TestArticleCase(TestBaseCase):

    def test_cluster_creation(self):
        """Check that the cluster record is created correctly."""
        cluster = Cluster(name="cluster")
        self.session.add(cluster)

        retrieved = self.session.query(Cluster).first()

        self.assertEqual(retrieved.name, "cluster")
        self.assertEqual(repr(retrieved), "<Cluster 'cluster'>")

    def test_cluster_relationship(self):
        """Check that the cluster relationship is created correctly."""
        cluster = Cluster(name="cluster")

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