"""Fetch RSS news for the categories displayed by ``app.py``."""

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


@st.cache_data(ttl=1800, show_spinner=False)
def _fetch_rss(url):
    """Return up to six normalized entries, or an empty list if unavailable."""
    try:
        feed = feedparser.parse(url)
        items = []
        for entry in feed.entries[:6]:
            items.append(
                {
                    "title": entry.get("title", "بدون عنوان"),
                    "summary": entry.get("summary", entry.get("description", ""))[:300],
                    "link": entry.get("link", "#"),
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
        items = _fetch_rss(url)
        if items:
            return items
    return info.get("fallback", [])


@st.cache_data(ttl=1800, show_spinner=False)
def is_live(category):
    """Return whether any configured feed currently has entries."""
    info = FEEDS.get(category)
    if not info:
        return False
    return any(bool(_fetch_rss(url)) for url in info["sources"])
