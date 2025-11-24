from datetime import datetime

from src.utils.normalize_text import normalize_text
from src.utils.parse_chesno_date import parse_chesno_date
from src.utils.parse_texty_date import parse_texty_date

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

ANTAC_CFG = {
    "title": {
        "tag_name": "meta",
        "tag_attrs": {"property": "og:title"},
        "formatter": str,
    },
    "author": {
        "tag_name": None,
        "tag_attrs": None,
        "formatter": str,
    },
    "featured_image_url": {
        "tag_name": "meta",
        "tag_attrs": {"property": "og:image"},
        "formatter": str,
    },
    "published_at": {
        "tag_name": "meta",
        "tag_attrs": {"property": "article:modified_time"},
        "formatter": datetime.fromisoformat,
    },
    "content": {
        "tag_name": "article",
        "tag_attrs": {"class": "article-content"},
        "formatter": normalize_text,
    },
}

CHESNO_CFG = {
    "title": {
        "tag_name": "meta",
        "tag_attrs": {"property": "og:title"},
        "formatter": str,
    },
    "author": {
        "tag_name": "div",
        "tag_attrs": "author-item",
        "formatter": normalize_text,
    },
    "featured_image_url": {
        "tag_name": "meta",
        "tag_attrs": {"property": "og:image"},
        "formatter": str,
    },
    "published_at": {
        "tag_name": "div",
        "tag_attrs": {"class": "date"},
        "formatter": parse_chesno_date,
    },
    "content": {
        "tag_name": "div",
        "tag_attrs": {"class": "publication-row"},
        "formatter": normalize_text,
    },
}

TEXTY_CFG = {
    "title": {
        "tag_name": "meta",
        "tag_attrs": {"property": "og:title"},
        "formatter": str,
    },
    "author": {
        "tag_name": "a",
        "tag_attrs": {"class": "author"},
        "formatter": normalize_text,
    },
    "featured_image_url": {
        "tag_name": "meta",
        "tag_attrs": {"property": "og:image"},
        "formatter": str,
    },
    "published_at": {
        "tag_name": "time",
        "tag_attrs": {},
        "formatter": parse_texty_date,
    },
    "content": {
        "tag_name": "article",
        "tag_attrs": {},
        "formatter": normalize_text,
    },
}