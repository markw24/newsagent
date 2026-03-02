# config.py — single source of truth for topics, feed URLs, and app settings

MAX_ARTICLES_PER_FEED = 5
OPENAI_MODEL = "gpt-4o-mini"

TOPICS = {
    "VC & Startups": [
        "https://techcrunch.com/feed/",
        "https://feeds.feedburner.com/venturebeat/SZYF",
    ],
    "Geopolitics": [
        "https://feeds.bbci.co.uk/news/world/rss.xml",
        "https://feeds.skynews.com/feeds/rss/world.xml",
    ],
    "World News": [
        "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
        "https://feeds.reuters.com/reuters/worldNews",
    ],
    "Financial News": [
        "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
    ],
}
