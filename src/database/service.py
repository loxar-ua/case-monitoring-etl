from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, select

from datetime import datetime, timedelta

from .models.category import Category
from .models.cluster import Cluster
from .session import get_session
from .models.media import Media
from .models.article import Article
from src.scrapper.scrappers.base_scrapper import ArticleInfo

def get_media() -> list[Media]:
    """Gets all media sites marked as 'is_active'.
    Used for taking sitemaps and associating articles
    to their separate media"""

    session = get_session()

    try:
        medias = session.query(Media).filter(Media.is_active == True).all()
        return medias

    except SQLAlchemyError as error:
        print(error) # TODO: log this
        return []

    finally:
        session.close()

def get_last_published_date(media: Media) -> datetime | None:
    """Finds last published date of article of media.
    Used for finding from what point to start new scraping"""

    session = get_session()

    try:
        last_published_date = (
            session.query(func.max(Article.published_at))
            .filter(Article.media_id == media.id)
            .scalar()
        )

        if last_published_date:
            last_published_date = last_published_date + timedelta(seconds=1)
            return last_published_date

        return None

    except SQLAlchemyError as error:
        print(error)  # TODO: log this
        return None

    finally:
        session.close()


def post_article(article_tuple: ArticleInfo) -> None:
    """Saves a single article to the database.
    Takes custom tuple with parsed elements of article and inserts
    data to database"""

    article = Article(
        link = article_tuple.link,
        title = article_tuple.title,
        featured_image_url= article_tuple.featured_image_url,
        author = article_tuple.author,
        published_at = article_tuple.published_at,
        content = article_tuple.content,
        media_id = article_tuple.media_id,
    )
    session = get_session()

    try:

        session.add(article)
        session.commit()

    except SQLAlchemyError as error:
        print(error) #TODO: log this
        session.rollback()

    finally:
        session.close()

def form_cluster(cluster_info: dict):
    """Saves a single cluster to the database.
    Takes dict with cluster info, creates cluster with
    title and summary, connects articles."""

    session = get_session()

    statement = select(Category).where(Category.id.in_(set(cluster_info['categories'])))
    categories = session.scalars(statement).all()

    statement = select(Article).where(Article.id.in_(set(cluster_info['articles_ids'])))
    articles = session.scalars(statement).all()

    cluster = Cluster(
        id = cluster_info['cluster_id'],
        name = cluster_info['title'],
        summary = cluster_info['summary'],
        categories = categories,
        is_relevant = cluster_info['is_relevant']
    )

    try:
        for article in articles:
            article.cluster_id = cluster_info['cluster_id']

        session.add(cluster)
        session.commit()

    except SQLAlchemyError as error:
        print(error) #TODO: log this
        session.rollback()

    finally:
        session.close()
