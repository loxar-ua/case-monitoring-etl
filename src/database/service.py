from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, or_

from datetime import datetime, timedelta

from sqlalchemy.orm import Query

from src.database.models.article import Article
from .session import get_session
from .models.media import Media
from .models.article import Article
from ..logger import logger


def get_media() -> list[Media]:
    """
    Gets all media sites marked as 'is_active'.
    Used for taking sitemaps and associating articles
    to their separate media
    :return:
    """

    try:
        with get_session() as session:
            medias = session.query(Media).filter(Media.is_active == True).order_by(Media.id).all()
            return medias

    except SQLAlchemyError:
        logger.exception("Error while getting media")
        return []

def get_last_published_date(media: Media) -> datetime | None:
    """
    Returns the last published date of articles for the given media.
    Returns None if no articles exist or an error occurs.
    :param media:
    :return: datetime of last published article from this media
    """

    try:
        with get_session() as session:
            last_published_date = (
                session.query(func.max(Article.published_at))
                .filter(Article.media_id == media.id)
                .scalar()
            )

            if last_published_date:
                last_published_date = last_published_date + timedelta(seconds=1)
                return last_published_date

            return None

    except SQLAlchemyError:
        logger.exception(
            "Error while getting last published date of articles from %s", media.name
        )
        return None


def post_article(article_dicts: list[dict]) -> None:
    """
    Inserts multiple articles into the database.
    Skips duplicates based on unique 'link' field.
    :param article_dicts:
    :return: None
    """

    if len(article_dicts) == 0:
        logger.warning("No articles to insert")
        return

    try:
        with get_session() as session:
            stmt = (
                insert(Article)
                .values(article_dicts)
                .on_conflict_do_nothing(index_elements=['link'])  # Use 'link' if that's your unique key
            )
            result = session.execute(stmt)
            session.commit()

            logger.info("Inserted %s articles to db", result.rowcount)

    except SQLAlchemyError:
        logger.exception("Error while inserting articles")


def get_articles(filter_not_encoded: bool = False) -> list[Article]:
    """
    Fetches all articles from db. If filter_not_encoded set to True
    fetches only articles without dense and sparse encoddings.
    :param filter_not_encoded: will this filter work
    :return: list of articles
    """

    try:
        with get_session() as session:
            query = session.query(Article)
            if filter_not_encoded:
                query = query.filter(
                    or_(
                        Article.dense_embedding.is_(None),
                        Article.sparse_embedding.is_(None)
                    )
                )

            logger.info("Fetched %s articles", query.count())
            return query.all()

    except SQLAlchemyError:
        logger.exception("Error while fetching articles")
        return []


def update_articles(articles: list[Article]):
    """
    Commits changes in articles. The main update of models is performed in outer functions.
    :param articles:
    """

    try:
        with get_session() as session:
            session.commit()
            logger.info("Updated %s articles", len(articles))

    except SQLAlchemyError:
        logger.exception("Error while updating articles")
