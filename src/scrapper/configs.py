from datetime import datetime, timezone
from src.utils.normalize_text import normalize_text
import re

GROSHI_CFG = {
    "title": {
        "tag_name": "meta",
        "tag_attrs": {"property": "og:title"},
        "formatter": str,
        "use_content_attr": True,
    },
    "author": {
    "tag_name": "div",
    "tag_attrs": {"class": "column-two-third single article"},
    "formatter": lambda tag: tag.find_all("p")[-1].get_text(strip=True) if tag else None
},
    "featured_image_url": {
        "tag_name": "meta",
        "tag_attrs": {"name": "twitter:image"},
        "formatter": str
    },

    "published_at": {
    "tag_name": "span",
    "tag_attrs": {"class": "meta"},
    "formatter": lambda tag: datetime.strptime(
        re.search(r"\d{2}\.\d{2}\.\d{4}", tag.get_text(strip=True)).group(),
        "%d.%m.%Y"
    ).replace(tzinfo=timezone.utc) if tag else None
},
    "content": {
    "tag_name": "div",
    "tag_attrs": {"class": "column-two-third single article"},
    "formatter": lambda tag: "\n".join(
        p.get_text(strip=True)
        for p in tag.find_all("p")[:-1]
    ) if tag else None
    },
}

TYZHDEN_CFG = {
    "title": {
        "tag_name": "meta",
        "tag_attrs": {"property": "og:title"},
        "formatter": str,
        "use_content_attr": True,

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
        "use_content_attr": True,
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
        "use_content_attr": True,
    },
    "author": {
        "tag_name": "meta",
        "tag_attrs": {"name": "author"},
        "formatter": str,
        "use_content_attr": True,
    },
    "featured_image_url": {
        "tag_name": "meta",
        "tag_attrs": {"property": "og:image"},
        "formatter": str,
        "use_content_attr": True,
    },
    "published_at": {
        "tag_name": "meta",
        "tag_attrs": {"property": "article:published_time"},
        "formatter": datetime.fromisoformat,
        "use_content_attr": True,
    },
    "content": {
        "tag_name": "div",
        "tag_attrs": {"class": "bi-single-content"},
        "formatter": normalize_text,
        "use_content_attr": True,
    },
}