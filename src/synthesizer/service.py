from src.database.models.cluster import Cluster
from src.database.models.article import Article
from src.database.repository import ClusterRepository
from src.synthesizer.llm_service import LLMService
from src.synthesizer.relevancy.pipeline import RelevancyPipeline
from src.synthesizer.name_cluster.pipeline import NamePipeline
from src.synthesizer.cluster_category.pipeline import CategoryPipeline
from src.synthesizer.event_segmenter.pipeline import EventPipeline

class ClusterAnalyzerService:
    def __init__(self, llm_client: LLMService):
        self.rel_pipe = RelevancyPipeline(llm_client)
        self.name_pipe = NamePipeline(llm_client)
        self.cat_pipe = CategoryPipeline(llm_client)
        self.event_pipe = EventPipeline(llm_client)

    def analyze(self, cluster: Cluster, articles: list[Article], repo: ClusterRepository) -> bool:
        rel_result = self.rel_pipe.relevancy(articles)
        cluster.is_relevant = rel_result.is_relevant

        if not cluster.is_relevant:
            return False

        cluster.name = self.name_pipe.name_cluster(articles).name

        cat_result = self.cat_pipe.categorize_cluster(articles)
        cluster.categories.clear()
        for cat_name in cat_result.categories:
            cluster.categories.append(repo.get_or_create_category(cat_name))

        event_result = self.event_pipe.segment_events(cluster.id, articles)
        article_map = {a.id: a for a in articles}
        repo.replace_cluster_events(cluster, event_result.events, article_map)

        cluster.is_checked = True
        return True