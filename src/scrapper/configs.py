from datetime import datetime, timezone, timedelta
from src.utils.normalize_text import normalize_text
import re

from src.utils.parse_chesno_date import parse_chesno_date
from src.utils.parse_texty_date import parse_texty_date
from src.utils.get_publish_at_pravda import parse_uk_date

HROMADSKE_CFG = {
    "title": {
        "tag_name": "meta",
        "tag_attrs": {"property": "og:title"},
        "formatter": str,
        "use_content_attr": True,
    },
    "author": {
    "tag_name": "a",
    "tag_attrs": {"class": "c-post-author__name"},
    "formatter": lambda tag: tag.get_text(strip=True) if tag else None
    },
    "featured_image_url": {
        "tag_name": "meta",
        "tag_attrs": {"property": "og:image"},
        "formatter": str
    },

    "published_at": {
    "tag_name": "time",
    "tag_attrs": {"class": "c-post-header__date"},
    "formatter": lambda tag: (
        datetime.fromisoformat(tag["datetime"])
        if tag and tag.has_attr("datetime")
        else None
    )
    },
    "content": {
        "tag_name": "div",
        "tag_attrs": {"class": "s-content"},
        "formatter": normalize_text,
        "use_content_attr": True,
    },
}

PRAVDA_CFG = {
    "title": {
        "tag_name": "meta",
        "tag_attrs": {"property": "og:title"},
        "formatter": str,
        "use_content_attr": True,
    },
    "author": {
    "tag_name": "div",
    "tag_attrs": {"class": "post_news_date"},
    "formatter": lambda tag: (
        tag.find("span", class_="post_news_author").get_text(strip=True)
        if tag and tag.find("span", class_="post_news_author")
        else None
    ),
    },
    "featured_image_url": {
        "tag_name": "meta",
        "tag_attrs": {"property": "og:image"},
        "formatter": str
    },

    "published_at": {
    "tag_name": "div",
    "tag_attrs": {"class": "post_news_date"},
    "formatter": lambda tag: parse_uk_date(
        tag.get_text(strip=True).split("—")[-1].strip()
    )
    },
    "content": {
        "tag_name": "div",
        "tag_attrs": {"class": "post_news_text"},
        "formatter": normalize_text,
        "use_content_attr": True,
    },
}

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