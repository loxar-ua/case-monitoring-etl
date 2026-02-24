from src.logger import logger
from src.database.repository import ClusterRepository
from src.synthesizer.service import ClusterAnalyzerService

class ClusterProcessingJob:
    def __init__(self, repo: ClusterRepository, analyzer: ClusterAnalyzerService, batch_commit: int = 10):
        self.repo = repo
        self.analyzer = analyzer
        self.batch_commit = batch_commit

    def run(self):
        clusters = self.repo.get_unprocessed_clusters()
        processed = 0

        for cluster in clusters:
            if len(cluster.articles) <= 2:
                continue

            try:
                self.analyzer.analyze(cluster, cluster.articles, self.repo)
                processed += 1
                logger.info(f"Processed {cluster.id}")

                if processed % self.batch_commit == 0:
                    self.repo.commit()

            except Exception as e:
                logger.error(f"Error while working on cluster {cluster.id}: {e}")
                self.repo.rollback()

        if processed % self.batch_commit != 0:
            self.repo.commit()