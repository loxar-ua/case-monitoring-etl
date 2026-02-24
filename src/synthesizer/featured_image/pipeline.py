from src.database.models.article import Article


class ImagePipeline:
    def get_latest_image_url(self, articles: list[Article]) -> str | None:
        valid_articles = [a for a in articles if a.featured_image_url and a.published_at]

        if not valid_articles:
            return None

        latest_article = max(valid_articles, key=lambda a: a.published_at)
        return latest_article.featured_image_url