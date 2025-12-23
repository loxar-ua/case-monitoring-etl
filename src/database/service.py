from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, select, update

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

def form_clusters(clusters_info: list):
    """Saves a single cluster to the database.
    Takes dict with cluster info, creates cluster with
    title and summary, connects articles."""

    session = get_session()

    all_categories = session.scalars(select(Category)).all()
    category_map = {c.id: c for c in all_categories}

    new_clusters = []
    article_updates = []

    for cluster_info in clusters_info:
        cluster_id = cluster_info['cluster_id']
        article_ids = set(cluster_info['articles_ids'])

        if cluster_info['is_relevant']:
            categories = [
                category_map[cat_id]
                for cat_id in cluster_info['categories']
                if cat_id in category_map
            ]

            statement = select(Article.featured_image_url).where(Article.id.in_(article_ids))
            with session.no_autoflush:
                images = session.scalars(statement).all()
            image = next((x for x in images if x), None)

            cluster = Cluster(
                id = cluster_id,
                name = cluster_info['title'],
                summary = cluster_info['summary'],
                categories = categories,
                is_relevant = True,
                featured_image_url = image
            )
        else:
            cluster = Cluster(
                id = cluster_id,
                is_relevant = False
            )

        new_clusters.append(cluster)
        print(cluster_id)
        for art_id in article_ids:
            article_updates.append({'id': art_id, 'cluster_id': cluster_id})

    try:
        session.add_all(new_clusters)
        session.execute(update(Article), article_updates)
        session.commit()

    except SQLAlchemyError as error:
        print(error) #TODO: log this
        session.rollback()

    finally:
        session.close()
