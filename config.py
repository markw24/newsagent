# config.py — single source of truth for topics, feed URLs, and app settings

MAX_ARTICLES_PER_FEED = 5
OPENAI_MODEL = "gpt-4o-mini"

# Each feed is a dict with url, tier (1=deepest analysis, 3=broadest), and name.
TOPICS = {
    "VC & Startups": [
        {"url": "https://www.ycombinator.com/blog/rss/", "tier": 1, "name": "YC Blog"},
        {"url": "https://a16z.com/feed/", "tier": 1, "name": "a16z"},
        {"url": "https://news.crunchbase.com/feed/", "tier": 2, "name": "Crunchbase"},
        {"url": "https://techcrunch.com/feed/", "tier": 2, "name": "TechCrunch"},
        {"url": "https://feeds.feedburner.com/venturebeat/SZYF", "tier": 3, "name": "VentureBeat"},
    ],
    "Geopolitics": [
        {"url": "https://feeds.bbci.co.uk/news/world/rss.xml", "tier": 1, "name": "BBC World"},
        {"url": "https://feeds.skynews.com/feeds/rss/world.xml", "tier": 2, "name": "Sky News"},
    ],
    "World News": [
        {"url": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml", "tier": 1, "name": "NYT World"},
        {"url": "https://feeds.reuters.com/reuters/worldNews", "tier": 1, "name": "Reuters"},
    ],
    "Financial News": [
        {"url": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml", "tier": 1, "name": "WSJ Markets"},
        {"url": "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml", "tier": 2, "name": "NYT Business"},
    ],
}
