from collections import namedtuple

ArticleInfo = namedtuple(
    "ArticleInfo",
    ["link", "title", "featured_image_url", "author", "published_at", "content", "media_id"]
)