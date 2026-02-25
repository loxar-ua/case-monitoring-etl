from src.logger import logger
from src.database.repository import ClusterRepository
from src.synthesizer.service import ClusterAnalyzerService


class ClusterProcessingJob:
    def __init__(self, repo: ClusterRepository, analyzer: ClusterAnalyzerService, batch_size: int = 50):
        self.repo = repo
        self.analyzer = analyzer
        self.batch_size = batch_size

    def run(self):
        total_processed = 0

        while True:
            clusters = self.repo.get_unprocessed_clusters(batch_limit=self.batch_size)

            if not clusters:
                logger.info("No more unprocessed clusters found. Finishing job.")
                break

            logger.info(f"Fetched batch of {len(clusters)} clusters.")

            for cluster in clusters:
                if len(cluster.articles) <= 2:
                    cluster.is_checked = True
                    continue

                try:
                    self.analyzer.analyze(cluster, cluster.articles, self.repo)
                    logger.info(f"Processed cluster {cluster.id}")

                except Exception as e:
                    logger.error(f"Error while working on cluster {cluster.id}: {e}")
                    self.repo.rollback()
                    continue

            try:
                self.repo.commit()
                total_processed += len(clusters)
                logger.info(f"Committed batch. Total processed: {total_processed}")
            except Exception as e:
                logger.error(f"Error committing batch: {e}")
                self.repo.rollback()