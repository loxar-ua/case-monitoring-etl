from src.database.models.category import Category
from src.database.models.article import Article
from src.database.models.cluster import Cluster
from tests.base_test_db import TestBaseCase


class TestCategoryCase(TestBaseCase):

    def test_category_relationship(self):
        """Check that the category relationship is created correctly."""
        category = Category(name="Корупція")

        self.session.add(category)
        self.session.flush()

        cluster = Cluster(name="cluster", categories=[category])
        self.session.add(cluster)
        self.session.flush()

        retrieved_cluster = self.session.query(Cluster).first()
        retrieved_category = self.session.query(Category).first()

        self.assertEqual(retrieved_cluster.categories[0].name, category.name)
        self.assertEqual(retrieved_category.clusters[0].name, cluster.name)






