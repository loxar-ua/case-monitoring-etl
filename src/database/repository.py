from sqlalchemy.orm import Session, selectinload
from src.database.models.cluster import Cluster
from src.database.models.category import Category
from src.database.models.event import Event

class ClusterRepository:
    def __init__(self, session: Session):
        self.session = session
        self._category_cache = self._load_category_cache()

    def _load_category_cache(self) -> dict:
        return {cat.name: cat for cat in self.session.query(Category).all()}

    def get_unprocessed_clusters(self, batch_limit: int = 50) -> list[Cluster]:
        return (
            self.session.query(Cluster)
            .options(
                selectinload(Cluster.articles),
                selectinload(Cluster.categories),
                selectinload(Cluster.events)
            )
            .filter(Cluster.is_checked.is_(False))
            .order_by(Cluster.id.desc())
            .limit(batch_limit)
            .all()
        )

    def get_or_create_category(self, name: str) -> Category:
        if name not in self._category_cache:
            new_cat = Category(name=name)
            self.session.add(new_cat)
            self._category_cache[name] = new_cat
        return self._category_cache[name]

    def replace_cluster_events(self, cluster: Cluster, event_results, article_map: dict):
        for old_event in cluster.events:
            self.session.delete(old_event)

        for event_data in event_results:
            event_articles = [
                article_map[art_id] for art_id in event_data.article_ids
                if art_id in article_map and getattr(article_map[art_id], 'published_at', None)
            ]

            event_date = min((a.published_at for a in event_articles), default=None)

            new_event = Event(
                title=event_data.title,
                description=event_data.description,
                cluster_id=cluster.id,
                date=event_date
            )
            self.session.add(new_event)
            self.session.flush()

            for art in event_articles:
                art.event_id = new_event.id

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()