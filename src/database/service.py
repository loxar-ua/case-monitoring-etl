from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, or_, and_, select

from datetime import datetime, timedelta

from src.database.models.article import Article
from src.database import ArticleFilter
from .models.cluster import Cluster
from .session import get_session
from .models.media import Media
from .models.article import Article
from ..logger import logger
from sqlalchemy.orm import Session
from src.database.models.article import Article
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


def get_articles(filter: ArticleFilter = ArticleFilter.ANY, columns: list | None = None) -> list:
    """
    Fetches all articles from db. If filter_not_encoded set to True
    fetches only articles without dense and sparse encoddings.
    :param filter:
    if ENCODED gives only encoded articles,
    if NON-ENCODED gives only articles without full encodings (no sparse or dense embedding),
    if ANY gives both encoded and non-encoded articles
    :return: list of articles
    """

    if columns is None:
        columns = [Article]
    else:
        columns = [getattr(Article, col) for col in columns]

    try:
        with get_session() as session:
            query = session.query(*columns)

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

            articles = query.all()

            logger.info("Fetched %s articles", len(articles))
            return articles

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

def create_clusters(ids: list):
    """
    Create empty clusters with such ids.
    :param ids:
    :return:
    """

    if not ids: return

    clean_ids = [int(i) for i in ids]

    BATCH_SIZE = 1000

    try:
        with get_session() as session:
            for i in range(0, len(clean_ids), BATCH_SIZE):
                chunk = clean_ids[i: i + BATCH_SIZE]

                stmt = insert(Cluster).values([{'id': x} for x in chunk])
                stmt = stmt.on_conflict_do_nothing(index_elements=['id'])

                session.execute(stmt)

            session.commit()
            logger.info(f"Ensured {len(clean_ids)} clusters exist (in batches).")

    except SQLAlchemyError as e:
        logger.exception("Error creating clusters")
        raise e



from psycopg2.extras import execute_values
import math

def assign_clusters_to_articles(ids: list, labels: list) -> None:
    """
    Updates cluster_id using Postgres 'UPDATE FROM VALUES'.
    Batches COMMITS to avoid locking the table for too long.
    """
    if not ids or not labels:
        return

    data = list(zip([int(x) for x in ids], [int(y) for y in labels]))
    total = len(data)

    BATCH_SIZE = 5000

    sql = """
          UPDATE article AS a
          SET cluster_id = v.new_cluster_id
              FROM \
              (VALUES %s) \
              AS v(art_id, new_cluster_id)
        WHERE a.id = v.art_id \
          """

    try:
        with get_session() as session:
            conn = session.connection().connection

            with conn.cursor() as cursor:
                for i in range(0, total, BATCH_SIZE):
                    chunk = data[i: i + BATCH_SIZE]

                    execute_values(
                        cursor,
                        sql,
                        chunk,
                        template="(%s, %s)",
                        page_size=1000
                    )
                    conn.commit()

                    logger.info(f"Fast-update progress: {min(i + BATCH_SIZE, total)} / {total}")

            logger.info(f"Finished assigning clusters to {total} articles.")

    except Exception:
        logger.exception("Error while assigning clusters to articles")






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

