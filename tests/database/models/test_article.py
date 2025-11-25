import unittest
from datetime import datetime

from src.database.models.article import Article
from src.database.models.media import Media
from src.database.models.cluster import Cluster
from tests.base_test_db import TestBaseCase

class TestArticleCase(TestBaseCase):

    def test_article_creation(self):
        """Check that the article record is created correctly."""
        article = Article(
            title="title",
            link="link",
            featured_image_url="image_url",
            author="author",
            content="content",
            published_at=datetime.now()
        )
        self.session.add(article)

        retrieved = self.session.query(Article).first()

        self.assertEqual(retrieved.title, "title")
        self.assertEqual(retrieved.link, "link")
        self.assertEqual(repr(retrieved), "<Article 'title', 'link'>")

    def test_article_minimum_creation(self):
        """Check that the article record is created using only the minimum required fields."""
        article = Article(title="title", link="link", content="content", published_at=datetime.now())
        self.session.add(article)

        retrieved = self.session.query(Article).first()

        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.title, "title")
        self.assertEqual(retrieved.author, None)


    def test_article_relationship(self):
        """Check that the article relationship with media and cluster works correctly."""
        cluster = Cluster(
            name="cluster"
        )

        media = Media(
            name="media",
            sitemap_index_url="index_url"
        )

        self.session.add_all([cluster, media])
        self.session.flush()

        article = Article(
            title="title",
            link="link",
            featured_image_url="image_url",
            author="author",
            content="content",
            published_at=datetime.now(),
            media_id=media.id,
            cluster_id=cluster.id
        )

        self.session.add(article)

        retrieved = self.session.query(Article).first()

        self.assertIsNotNone(retrieved.media)
        self.assertEqual(retrieved.media.name, "media")

        self.assertIsNotNone(retrieved.cluster)
        self.assertEqual(retrieved.cluster.name, "cluster")


if __name__ == "__main__":
    unittest.main()