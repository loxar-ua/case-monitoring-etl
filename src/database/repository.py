from sqlalchemy.orm import Session, joinedload
from src.database.models.cluster import Cluster
from src.database.models.category import Category
from src.database.models.event import Event

class ClusterRepository:
    def __init__(self, session: Session):
        self.session = session
        self._category_cache = self._load_category_cache()

    def _load_category_cache(self) -> dict:
        return {cat.name: cat for cat in self.session.query(Category).all()}

    def get_unprocessed_clusters(self) -> list[Cluster]:
        return (
            self.session.query(Cluster)
            .options(
                joinedload(Cluster.articles),
                joinedload(Cluster.categories),
                joinedload(Cluster.events)
            )
            .filter(Cluster.is_checked.is_(False))
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
            new_event = Event(
                title=event_data.title,
                description=event_data.description,
                cluster_id=cluster.id
            )
            self.session.add(new_event)
            self.session.flush()

            for art_id in event_data.article_ids:
                if art_id in article_map:
                    article_map[art_id].event_id = new_event.id

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()