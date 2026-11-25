"""Fetch RSS news for the categories displayed by ``app.py``."""

from urllib.parse import urljoin, urlparse

import feedparser
import streamlit as st


FEEDS = {
    "fed": {
        "title": "🏛️ آخر أخبار الاحتياطي الفيدرالي",
        "sources": [
            "https://www.federalreserve.gov/feeds/press_all.xml",
            "https://www.federalreserve.gov/feeds/press_monetary.xml",
        ],
        "fallback": [],
    },
    "gold": {
        "title": "🥇 تقارير مجلس الذهب العالمي",
        "sources": [
            "https://www.gold.org/goldhub/rss/news",
            "https://www.gold.org/rss/press-releases",
        ],
        "fallback": [],
    },
    "analysts": {
        "title": "📊 آراء المحللين الاقتصاديين",
        "sources": [
            "https://feeds.content.dowjones.io/public/rss/mw_topstories",
        ],
        "fallback": [],
    },
    "markets": {
        "title": "📈 آخر أخبار الأسواق",
        "sources": [
            "https://www.cnbc.com/id/100003114/device/rss/rss.html",
            "https://feeds.content.dowjones.io/public/rss/mw_marketpulse",
        ],
        "fallback": [],
    },
}


def _clean_external_link(raw_link, feed_url, category):
    """Normalize an RSS link and reject unusable values such as '#' or fragments."""
    if not isinstance(raw_link, str):
        return None

    link = raw_link.strip()
    if not link or link == "#":
        return None

    link = urljoin(feed_url, link)
    parsed = urlparse(link)

    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return None

    if category == "gold" and parsed.hostname not in ("gold.org", "www.gold.org"):
        return None

    return link


def _entry_link(entry, feed_url, category):
    """Extract the real article URL from common RSS fields."""
    candidates = [
        entry.get("link"),
        entry.get("guid"),
        entry.get("id"),
    ]

    for link_candidate in candidates:
        cleaned = _clean_external_link(link_candidate, feed_url, category)
        if cleaned:
            return cleaned

    for link_data in entry.get("links", []) or []:
        if isinstance(link_data, dict):
            if link_data.get("rel") not in (None, "alternate", "self"):
                continue
            cleaned = _clean_external_link(link_data.get("href"), feed_url, category)
            if cleaned:
                return cleaned

    return "https://www.gold.org/goldhub/research" if category == "gold" else None


@st.cache_data(ttl=1800, show_spinner=False)
def _fetch_rss(url, category=""):
    """Return up to six normalized entries, or an empty list if unavailable."""
    try:
        feed = feedparser.parse(url)
        if getattr(feed, "bozo", False) and not getattr(feed, "entries", None):
            return []

        items = []
        for entry in feed.entries[:6]:
            link = _entry_link(entry, url, category)

            items.append(
                {
                    "title": entry.get("title", "بدون عنوان").strip(),
                    "summary": entry.get("summary", entry.get("description", ""))[:300],
                    "link": link or "#",
                    "date": entry.get("published", entry.get("updated", "")),
                }
            )
        return items
    except Exception:
        return []


@st.cache_data(ttl=1800, show_spinner=False)
def get_news(category):
    """Fetch news for a category, returning its fallback list if feeds fail."""
    info = FEEDS.get(category)
    if not info:
        return []

    for url in info["sources"]:
        items = _fetch_rss(url, category)
        if items:
            return items
    return info.get("fallback", [])


@st.cache_data(ttl=1800, show_spinner=False)
def is_live(category):
    """Return whether any configured feed currently has entries."""
    info = FEEDS.get(category)
    if not info:
        return False
    return any(bool(_fetch_rss(url, category)) for url in info["sources"])
