import unittest
from unittest.mock import patch
from datetime import datetime, timezone

from src.database.service import get_media, post_article, get_last_published_date
from tests.base_test import TestBaseCase
from src.database.models.media import Media
from src.database.models.article import Article
from src.scrapper.scrappers import ArticleInfo

class TestServiceCase(TestBaseCase):

    @patch("src.database.service.get_session")
    def test_get_media(self, mock_get_session):
        """Checks that get_media returns only active media"""
        mock_get_session.return_value = self.session

        with patch.object(self.session, 'close') as mock_close:
            medias = [
                Media(name="active_media", sitemap_index_url="index.xml", is_active=True),
                Media(name="inactive_media", sitemap_index_url="index.xml", is_active=False),
            ]

            self.session.add_all(medias)

            self.session.flush()

            retrieved = get_media()

            mock_close.assert_called_once()

            self.assertEqual(len(retrieved), 1)

            self.assertIsInstance(retrieved[0], Media)
            self.assertEqual("active_media", retrieved[0].name)

    @patch("src.database.service.get_session")
    def test_post_article(self, mock_get_session):
        """Checks that post_article correctly posts articles into database"""
        mock_get_session.return_value = self.session

        with patch.object(self.session, 'commit') as mock_commit, \
                patch.object(self.session, 'close') as mock_close:

            media = Media(name="test_media", sitemap_index_url="index.xml", is_active=True)
            self.session.add(media)
            self.session.flush()

            published_date = datetime.now(tz=timezone.utc)
            media_id = media.id
            article = ArticleInfo(
                "link",
                "title",
                "featured_image",
                "author",
                published_date,
                "content",
                media_id
            )

            post_article(article)

            mock_commit.assert_called_once()
            mock_close.assert_called_once()

            self.session.flush()

            retrieved = self.session.query(Article).first()

            self.assertEqual(retrieved.link, "link")
            self.assertEqual(retrieved.title, "title")
            self.assertEqual(retrieved.featured_image_url, "featured_image")
            self.assertEqual(retrieved.published_at, published_date)
            self.assertEqual(retrieved.author, "author")
            self.assertEqual(retrieved.content, "content")
            self.assertEqual(retrieved.media_id, media_id)

    @patch("src.database.service.get_session")
    def test_last_published_date_one_media(self, mock_get_session):
        """Tests whether get_last_published_date() returns
        correct last published date"""
        mock_get_session.return_value = self.session

        with patch.object(self.session, 'close') as mock_close:
            media = Media(name="test_media", sitemap_index_url="index.xml", is_active=True)
            self.session.add(media)
            self.session.flush()

            published_date_1 = datetime(2012, 12, 12, 12, 12, tzinfo=timezone.utc)
            published_date_2 = datetime(2015, 12, 13, 13, 13, tzinfo=timezone.utc)
            media_id = media.id
            articles = [
                Article(
                    link="link_1",
                    title="title",
                    featured_image_url="featured_image",
                    author="author",
                    published_at=published_date_1,
                    content="content",
                    media_id=media.id
                ),
                Article(
                    link="link_2",
                    title="title",
                    featured_image_url="featured_image",
                    author="author",
                    published_at=published_date_2,
                    content="content",
                    media_id=media.id
                )
            ]

            self.session.add_all(articles)
            self.session.flush()

            retrieved_date = get_last_published_date(media)

            self.assertEqual(retrieved_date, published_date_2)

    @patch("src.database.service.get_session")
    def test_last_published_date_different_media(self, mock_get_session):
        """Tests whether get_last_published_date() returns
        correct date of only media we specify
        and not the last published date of all articles"""
        mock_get_session.return_value = self.session

        with patch.object(self.session, 'close') as mock_close:
            medias = [
                Media(name="test_media_1", sitemap_index_url="index.xml", is_active=True),
                Media(name="test_media_2", sitemap_index_url="index.xml", is_active=False),
            ]
            self.session.add_all(medias)
            self.session.flush()

            published_date_1 = datetime(2012, 12, 12, 12, 12, tzinfo=timezone.utc)
            published_date_2 = datetime(2015, 12, 13, 13, 13, tzinfo=timezone.utc)

            articles = [
                Article(
                    link="link_1",
                    title="title",
                    featured_image_url="featured_image",
                    author="author",
                    published_at=published_date_1,
                    content="content",
                    media_id=medias[0].id
                ),
                Article(
                    link="link_2",
                    title="title",
                    featured_image_url="featured_image",
                    author="author",
                    published_at=published_date_2,
                    content="content",
                    media_id=medias[1].id
                )
            ]

            self.session.add_all(articles)
            self.session.flush()

            retrieved_date_1 = get_last_published_date(medias[0])
            retrieved_date_2 = get_last_published_date(medias[1])

            self.assertEqual(retrieved_date_1, published_date_1)
            self.assertEqual(retrieved_date_2, published_date_2)

if __name__ == "__main__":
    unittest.main()

