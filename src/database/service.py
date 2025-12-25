from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func

from datetime import datetime, timedelta
from typing import List

from .session import get_session
from .models.media import Media
from .models.article import Article
from src.scrapper.scrappers.base_scrapper import ArticleInfo
from ..logger import logger


def get_media() -> list[Media]:
    """Gets all media sites marked as 'is_active'.
    Used for taking sitemaps and associating articles
    to their separate media"""

    session = get_session()

    try:
        medias = session.query(Media).filter(Media.is_active == True).order_by(Media.id).all()
        return medias

    except SQLAlchemyError:
        logger.exception("Error while getting media")
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

    except SQLAlchemyError:
        logger.exception("Error while getting last published date of articles from %s", media.name)
        return None

    finally:
        session.close()


def post_article(article_tuples: List[ArticleInfo]) -> None:
    """Saves a single article to the database.
    Takes custom tuple with parsed elements of article and inserts
    data to database"""

    if len(article_tuples) == 0:
        logger.info("No article where given to insert")
        return

    articles = []
    for article_tuple in article_tuples:
        article = Article(
            link = article_tuple.link,
            title = article_tuple.title,
            featured_image_url= article_tuple.featured_image_url,
            author = article_tuple.author,
            published_at = article_tuple.published_at,
            content = article_tuple.content,
            media_id = article_tuple.media_id,
        )
        articles.append(article)
    session = get_session()


    try:
        session.add_all(articles)
        session.commit()

        logger.info("Inserted %s articles to db", len(articles))

    except SQLAlchemyError:
        logger.exception("Error while inserting articles")
        session.rollback()

    finally:
        session.close()