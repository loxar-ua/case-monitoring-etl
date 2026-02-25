from src.database.session import get_session
from src.database.repository import ClusterRepository
from src.synthesizer.llm_service import LLMService
from src.synthesizer.service import ClusterAnalyzerService
from src.synthesizer.runner import ClusterProcessingJob

def main():
    llm_client = LLMService()

    with get_session() as session:
        repo = ClusterRepository(session)
        analyzer_service = ClusterAnalyzerService(llm_client)

        job = ClusterProcessingJob(
            repo=repo,
            analyzer=analyzer_service,
        )

        job.run()

if __name__ == "__main__":
    main()