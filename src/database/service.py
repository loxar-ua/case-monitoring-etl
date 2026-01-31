from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, or_, and_

from datetime import datetime, timedelta

from src.database import ArticleFilter
from .session import get_session
from .models.media import Media
from ..logger import logger
from sqlalchemy.orm import Session
from src.database.models.article import Article
from src.database.models.cluster import Cluster
from src.synthesizer.relevancy.pipeline import RelevancyPipeline
from src.synthesizer.name_cluster.pipeline import NamePipeline


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


def get_articles(filter: ArticleFilter = ArticleFilter.ANY) -> list[Article]:
    """
    Fetches all articles from db. If filter_not_encoded set to True
    fetches only articles without dense and sparse encoddings.
    :param filter:
    if ENCODED gives only encoded articles,
    if NON-ENCODED gives only articles without full encodings (no sparse or dense embedding),
    if ANY gives both encoded and non-encoded articles
    :return: list of articles
    """

    try:
        with get_session() as session:
            query = session.query(Article)
            if filter == ArticleFilter.ENCODED:
                query = query.filter(
                    and_(
                        Article.dense_embedding.is_not(None),
                        Article.sparse_embedding.is_not(None)
                    )
                )
            elif filter == ArticleFilter.NON_ENCODED:
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
            for article in articles:
                session.merge(article)
            session.commit()
            logger.info("Updated %s articles", len(articles))

    except SQLAlchemyError:
        logger.exception("Error while updating articles")





def relevancy_pipeline(session: Session, llm_client, batch_commit: int = 10):
    pipeline = RelevancyPipeline(llm_client)

    clusters = session.query(Cluster).all()

    processed = 0
    for cluster in clusters:
        articles = session.query(Article).filter_by(cluster_id=cluster.id).all()

        if len(articles) <= 2:
            continue

        result = pipeline.relevancy(articles)
        cluster.is_relevant = result.is_relevant

        processed += 1

        if processed % batch_commit == 0:
            session.commit()

    session.commit()

def name_cluster_pipeline(session: Session, llm_client, batch_commit: int = 10):
    pipeline = NamePipeline(llm_client)

    clusters = session.query(Cluster).filter_by(Cluster.is_relevant.is_(True)).all()

    processed = 0
    for cluster in clusters:
        articles = session.query(Article).filter_by(cluster_id=cluster.id).all()


        result = pipeline.name_cluster(articles)
        cluster.name = result.name

        processed += 1

        if processed % batch_commit == 0:
            session.commit()

    session.commit()

