import unittest
from datetime import datetime

from src.database.models.article import Article
from src.database.models.media import Media
from tests.base_test_db import BDTestCase

class BDTestArticleCase(BDTestCase):
    def test_media_creation(self):
        """Check that the media record is created correctly."""
        media = Media(
            name = "media",
            sitemap_index_url= "index.xml"
        )
        self.session.add(media)

        self.session.flush()

        retrieved = self.session.query(Media).first()

        self.assertEqual(retrieved.name, "media")
        self.assertEqual(retrieved.sitemap_index_url, "index.xml")
        self.assertEqual(repr(retrieved), "<Media 'media'>")

    def test_media_relationship(self):
        """Check that the media relationship is created correctly."""
        media = Media(name = "media", sitemap_index_url = "index.xml" )

        self.session.add(media)

        self.session.flush()

        article = Article(
            title="title",
            link="link",
            featured_image_url="image_url",
            author="author",
            content="content",
            published_at=datetime.now(),
            media_id=media.id,
        )

        self.session.add(article)

        self.session.flush()

        retrieved = self.session.query(Media).first()

        self.assertIsNotNone(retrieved.articles[0])
        self.assertEqual(len(retrieved.articles), 1)
        self.assertEqual(retrieved.articles[0].title, "title")


if __name__ == "__main__":
    unittest.main()