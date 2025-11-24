from datetime import datetime

from src.utils.normalize_text import normalize_text

TYZHDEN_CFG = {
    "title": {
        "tag_name": "meta",
        "tag_attrs": {"property": "og:title"},
        "formatter": str
    },
    "author": {
        "tag_name": "span",
        "tag_attrs": {"class": "a-name"},
        "formatter": lambda tag: tag.get_text(strip=True) if tag else None
        },
    "featured_image_url": {
        "tag_name": "meta",
        "tag_attrs": {"property": "og:image"},
        "formatter": str
    },
    "published_at": {
        "tag_name": "meta",
        "tag_attrs": {"property": "article:published_time"},
        "formatter": datetime.fromisoformat,
    },
    "content": {
        "tag_name": "div",
        "tag_attrs": {"class": "entry-content"},
        "formatter": normalize_text,
    },
}

BIHUS_CFG = {
    "title": {
        "tag_name": "meta",
        "tag_attrs": {"property": "og:title"},
        "formatter": str,
    },
    "author": {
        "tag_name": "meta",
        "tag_attrs": {"name": "author"},
        "formatter": str,
    },
    "featured_image_url": {
        "tag_name": "meta",
        "tag_attrs": {"property": "og:image"},
        "formatter": str,
    },
    "published_at": {
        "tag_name": "meta",
        "tag_attrs": {"property": "article:published_time"},
        "formatter": datetime.fromisoformat,
    },
    "content": {
        "tag_name": "div",
        "tag_attrs": {"class": "bi-single-content"},
        "formatter": normalize_text,
    },
}