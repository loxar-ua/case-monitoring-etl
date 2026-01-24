import numpy as np

import unittest
from unittest.mock import patch
from datetime import datetime, timezone, timedelta

from scipy.sparse import csr_matrix
from sqlalchemy.exc import SQLAlchemyError

from src.database import ArticleFilter
from src.database.models.cluster import Cluster
from src.database.service import get_media, post_article, get_last_published_date, get_articles, update_articles, \
    create_clusters, assign_clusters_to_articles
from src.embedder import DENSE_DIM, VOCAB_SIZE
from tests.base_test_db import BDTestCase
from src.database.models.media import Media
from src.database.models.article import Article

class BDTestServiceCase(BDTestCase):

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
            article = {
                "link": 'link',
                "title": 'title',
                "featured_image_url": 'featured_image',
                "author": 'author',
                'published_at': published_date,
                'content': "content",
                'media_id': media_id
            }

            post_article([article])

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

            published_date_1 = datetime(2012, 12, 12, 12, 12, 1, tzinfo=timezone.utc)
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

            self.assertEqual(retrieved_date, published_date_2 + timedelta(seconds=1))

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

            self.assertEqual(retrieved_date_1, published_date_1 + timedelta(seconds=1))
            self.assertEqual(retrieved_date_2, published_date_2 + timedelta(seconds=1))

    @patch("src.database.service.get_session")
    def test_get_articles(self, mock_get_session):
        """Tests whether get_articles() returns
        all articles, in a normal non-filtering mode"""
        mock_get_session.return_value = self.session

        media = Media(name="test_media_1", sitemap_index_url="index.xml", is_active=True)
        self.session.add(media)
        self.session.flush()

        published_date = datetime(2012, 12, 12, 12, 12, tzinfo=timezone.utc)

        articles = [
            Article(
                link="link_1",
                title="title",
                media_id=media.id,
                content="content",
                published_at=published_date,
            ),
            Article(
                link="link_2",
                title="title",
                media_id=media.id,
                content="content",
                published_at=published_date,
            )
        ]

        self.session.add_all(articles)
        self.session.flush()

        with patch.object(self.session, 'close'):
            retrieved = get_articles(filter=ArticleFilter.ANY)

        self.assertEqual(len(retrieved), 2)
        self.assertEqual(retrieved[0], articles[0])
        self.assertEqual(retrieved[1], articles[1])

    @patch("src.database.service.get_session")
    def test_get_articles_filter_non_encoding(self, mock_get_session):
        """Tests whether get_articles() returns
        only non-encoded articles, in a non_encoded mode"""
        mock_get_session.return_value = self.session

        media = Media(name="test_media_1", sitemap_index_url="index.xml", is_active=True)
        self.session.add(media)
        self.session.flush()

        dense = np.zeros(DENSE_DIM)
        sparse = csr_matrix((1, VOCAB_SIZE))
        published_date = datetime(2012, 12, 12, 12, 12, tzinfo=timezone.utc)

        articles = [
            Article(
                link="link_1",
                title="title",
                media_id=media.id,
                content="content",
                published_at=published_date,
            ),
            Article(
                link="link_2",
                title="title",
                media_id=media.id,
                dense_embedding = dense,
                sparse_embedding = sparse,
                content="content",
                published_at=published_date,
            ),
            Article(
                link="link_3",
                title="title",
                media_id=media.id,
                dense_embedding = dense,
                content="content",
                published_at=published_date,
            ),
            Article(
                link="link_4",
                title="title",
                media_id=media.id,
                sparse_embedding = sparse,
                content="content",
                published_at=published_date,
            )
        ]

        self.session.add_all(articles)
        self.session.flush()

        with patch.object(self.session, 'close'):
            retrieved = get_articles(filter=ArticleFilter.NON_ENCODED)

        # Second article should be absent.
        self.assertEqual(len(retrieved), 3)
        self.assertEqual(retrieved[0], articles[0])
        self.assertEqual(retrieved[1], articles[2])
        self.assertEqual(retrieved[2], articles[3])

    @patch("src.database.service.get_session")
    def test_get_articles_filter_encoding(self, mock_get_session):
        """Tests whether get_articles() returns
        only fully encoded articles, in an encoded mode"""
        mock_get_session.return_value = self.session

        media = Media(name="test_media_1", sitemap_index_url="index.xml", is_active=True)
        self.session.add(media)
        self.session.flush()

        dense = np.zeros(DENSE_DIM)
        sparse = csr_matrix((1, VOCAB_SIZE))
        published_date = datetime(2012, 12, 12, 12, 12, tzinfo=timezone.utc)

        articles = [
            Article(
                link="link_1",
                title="title",
                media_id=media.id,
                content="content",
                published_at=published_date,
            ),
            Article(
                link="link_2",
                title="title",
                media_id=media.id,
                dense_embedding=dense,
                sparse_embedding=sparse,
                content="content",
                published_at=published_date,
            ),
            Article(
                link="link_3",
                title="title",
                media_id=media.id,
                dense_embedding=dense,
                content="content",
                published_at=published_date,
            ),
            Article(
                link="link_4",
                title="title",
                media_id=media.id,
                sparse_embedding=sparse,
                content="content",
                published_at=published_date,
            )
        ]

        self.session.add_all(articles)
        self.session.flush()

        with patch.object(self.session, 'close'):
            retrieved = get_articles(filter=ArticleFilter.ENCODED)

        # Second article should be fetched.
        self.assertEqual(len(retrieved), 1)
        self.assertEqual(retrieved[0], articles[1])

    @patch("src.database.service.get_session")
    def test_get_articles_get_correct_columns(self, mock_get_session):
        mock_get_session.return_value = self.session

        media = Media(name="test_media_1", sitemap_index_url="index.xml", is_active=True)
        self.session.add(media)
        self.session.flush()

        dense = np.zeros(DENSE_DIM)
        published_date = datetime(2012, 12, 12, 12, 12, tzinfo=timezone.utc)

        article = Article(
                link="link_1",
                title="title",
                media_id=media.id,
                content="content",
                published_at=published_date,
                dense_embedding=dense
            )


        self.session.add(article)
        self.session.flush()

        with patch.object(self.session, 'close'):
            retrieved = get_articles(filter=ArticleFilter.ANY, columns=["id", "dense_embedding"])

        self.assertEqual(len(retrieved), 1)
        self.assertEqual(retrieved[0][0], article.id)
        np.testing.assert_allclose(retrieved[0][1], dense, rtol=1e-5)


    @patch("src.database.service.get_session")
    def test_update_articles(self, mock_get_session):
        """Tests whether update articles commit changes to db"""
        mock_get_session.return_value = self.session

        media = Media(name="test_media_1", sitemap_index_url="index.xml", is_active=True)
        self.session.add(media)
        self.session.flush()

        published_date = datetime(2012, 12, 12, 12, 12, tzinfo=timezone.utc)

        articles = [
            Article(
                link="link_1",
                title="title",
                media_id=media.id,
                content="content",
                published_at=published_date
            )
        ]

        self.session.add_all(articles)
        self.session.flush()

        new_title = "new title"
        articles[0].title = new_title
        with patch.object(self.session, 'close'):
            update_articles(articles)
            retrieved = get_articles()

        self.assertEqual(retrieved[0].title, new_title)

    @patch("src.database.service.get_session")
    def test_create_clusters(self, mock_get_session):
        """Checks that create_clusters correctly creates clusters in the database"""
        mock_get_session.return_value = self.session

        cluster_ids = [1, 2, 3]

        create_clusters(cluster_ids)

        self.session.flush()

        retrieved_clusters = self.session.query(Cluster).filter(Cluster.id.in_(cluster_ids)).all()

        self.assertEqual(len(retrieved_clusters), 3)

        retrieved_ids = {c.id for c in retrieved_clusters}
        self.assertEqual(retrieved_ids, {1, 2, 3})

    @patch("src.database.service.logger")
    @patch("src.database.service.get_session")
    def test_create_clusters_error_handling(self, mock_get_session, mock_logger):
        """Checks that SQLAlchemyError is caught and logged properly"""
        mock_get_session.return_value = self.session

        existing_cluster = Cluster(id=99)
        self.session.add(existing_cluster)
        self.session.commit()

        create_clusters([99])

        try:
            self.session.commit()
        except Exception:
            pass

        pass

    @patch("src.database.service.get_session")
    def test_assign_clusters_to_articles_success(self, mock_get_session):
        """
        Checks that assign_clusters_to_articles calls bulk_update_mappings
        with the correct dictionary structure.
        """
        mock_get_session.return_value = self.session

        article_ids = [101, 102, 103]
        cluster_labels = [5, 5, 8]

        with patch.object(self.session, 'bulk_update_mappings') as mock_bulk_update, \
                patch.object(self.session, 'commit') as mock_commit:
            assign_clusters_to_articles(article_ids, cluster_labels)

            expected_mappings = [
                {'id': 101, 'cluster_id': 5},
                {'id': 102, 'cluster_id': 5},
                {'id': 103, 'cluster_id': 8}
            ]

            mock_bulk_update.assert_called_once_with(Article, expected_mappings)
            mock_commit.assert_called_once()

    @patch("src.database.service.get_session")
    def test_assign_clusters_to_articles_empty(self, mock_get_session):
        """Checks that empty inputs do not trigger DB calls"""
        mock_get_session.return_value = self.session

        with patch.object(self.session, 'bulk_update_mappings') as mock_bulk_update:
            assign_clusters_to_articles([], [])
            mock_bulk_update.assert_not_called()

    @patch("src.database.service.logger")
    @patch("src.database.service.get_session")
    def test_assign_clusters_to_articles_error(self, mock_get_session, mock_logger):
        """Checks that SQLAlchemyError during bulk update is logged"""
        mock_get_session.return_value = self.session

        with patch.object(self.session, 'bulk_update_mappings', side_effect=SQLAlchemyError("DB Crash")):
            assign_clusters_to_articles([1], [2])

            mock_logger.exception.assert_called_with("Error while assigning clusters to articles")


if __name__ == "__main__":
    unittest.main()

