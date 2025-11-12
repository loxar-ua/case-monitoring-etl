from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from testcontainers.postgres import PostgresContainer

import unittest
from datetime import datetime

from src.database.models.article import Article
from src.database.models.base import Base
from src.database.models.media import Media
from src.database.session import get_connection



class TestMediaCase(unittest.TestCase):
    postgres: PostgresContainer = None
    engine = None
    Session = None

    @classmethod
    def setUpClass(cls):
        cls.postgres = PostgresContainer('postgres:16')
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
        Base.metadata.drop_all(cls.engine)

        if cls.engine:
            cls.engine.dispose()

        if cls.postgres:
            cls.postgres.stop()

    def setUp(self):
        self.session = self.Session()
        self.transaction = self.session.begin_nested()

    def tearDown(self):
        self.transaction.rollback()
        self.session.close()

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