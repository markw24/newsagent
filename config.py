# config.py — single source of truth for topics, feed URLs, and app settings

MAX_ARTICLES_PER_FEED = 5
OPENAI_MODEL = "gpt-4o-mini"

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
        {"url": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml", "tier": 1, "name": "NYT World"},
        {"url": "https://feeds.skynews.com/feeds/rss/world.xml", "tier": 2, "name": "Sky News"},
    ],
    "World News": [
        {"url": "https://news.google.com/rss/search?q=when:24h+allinurl:reuters.com&ceid=US:en&hl=en-US&gl=US", "tier": 1, "name": "Reuters via Google"},
        {"url": "https://feeds.bbci.co.uk/news/rss.xml", "tier": 1, "name": "BBC Top"},
        {"url": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml", "tier": 1, "name": "NYT Home"},
    ],
    "Financial News": [
        {"url": "https://feeds.content.dowjones.io/public/rss/mw_realtimeheadlines", "tier": 1, "name": "MarketWatch"},
        {"url": "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml", "tier": 1, "name": "NYT Business"},
        {"url": "https://seekingalpha.com/market_currents.xml", "tier": 2, "name": "Seeking Alpha"},
        {"url": "https://feeds.finance.yahoo.com/rss/2.0/headline?s=^GSPC&region=US&lang=en-US", "tier": 2, "name": "Yahoo Finance"},
        {"url": "https://www.investing.com/rss/news.rss", "tier": 3, "name": "Investing.com"},
    ],
}
