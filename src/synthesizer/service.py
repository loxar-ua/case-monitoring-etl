from src.database.models.cluster import Cluster
from src.database.models.article import Article
from src.database.repository import ClusterRepository
from src.synthesizer.llm_service import LLMService
from src.synthesizer.unified_analyzer.pipeline import UnifiedAnalyzerPipeline
from src.synthesizer.featured_image.pipeline import ImagePipeline


class ClusterAnalyzerService:
    def __init__(self, llm_client: LLMService):
        self.unified_pipe = UnifiedAnalyzerPipeline(llm_client)
        self.image_pipe = ImagePipeline()

    def analyze(self, cluster: Cluster, articles: list[Article], repo: ClusterRepository) -> bool:
        analysis_result = self.unified_pipe.analyze_cluster(articles)

        cluster.is_relevant = analysis_result.is_relevant

        if not cluster.is_relevant:
            cluster.is_checked = True
            return False

        cluster.name = analysis_result.name

        cluster.categories.clear()
        for cat_name in analysis_result.categories:
            cluster.categories.append(repo.get_or_create_category(cat_name))

        article_map = {a.id: a for a in articles}
        repo.replace_cluster_events(cluster, analysis_result.events, article_map)

        cluster.featured_image_url = self.image_pipe.get_latest_image_url(articles)

        cluster.is_checked = True
        return True