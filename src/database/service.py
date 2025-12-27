from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func

from datetime import datetime, timedelta

from .session import get_session
from .models.media import Media
from .models.article import Article
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


def post_article(article_dicts: list[dict]) -> None:
    """Saves a single article to the database.
    Takes custom tuple with parsed elements of article and inserts
    data to database"""

    if len(article_dicts) == 0:
        logger.error("No article where given to insert")
        return

    session = get_session()
    try:
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
        session.rollback()

    finally:
        session.close()