from collections import defaultdict
import csv

from tests.synthesizer.relevancy.schemas import Article


def load_articles_from_csv(path: str) -> list[Article]:
    articles = []

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            raw_cluster = row.get("predicted_cluster", "").strip()

            if not raw_cluster:
                continue  # ⬅️ просто пропускаємо

            articles.append(
                Article(
                    id=int(row["id"]),
                    title=row["title"],
                    content=row["content"],
                    cluster_id=int(float(raw_cluster)),
                )
            )

    return articles



def group_by_cluster(articles: list[Article]) -> dict[int, list[Article]]:
    clusters = defaultdict(list)

    for article in articles:
        clusters[article.cluster_id].append(article)

    return clusters

class MockLLMClient:
    def classify(self, prompt: str) -> str:
        return '{"is_relevant": true}'

from src.synthesizer.relevancy.pipeline import RelevancyPipeline

articles = load_articles_from_csv(
    "/src/synthesizer/relevancy/fixtures/data_updated.csv"
)

clusters = group_by_cluster(articles)

pipeline = RelevancyPipeline(MockLLMClient())

results = []

for cluster_id, cluster_articles in clusters.items():
    if not cluster_articles:
        continue

    result = pipeline.relevancy(cluster_articles)

    results.append({
        "cluster_id": cluster_id,
        "articles_count": len(cluster_articles),
        "is_relevant": result.is_relevant,
    })

    print(
        f"Cluster {cluster_id}: "
        f"{len(cluster_articles)} articles → "
        f"is_relevant={result.is_relevant}"
    )
