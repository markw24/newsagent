# fetch_feeds.py — downloads RSS feeds and returns a dict of article lists per topic

import feedparser
from config import MAX_ARTICLES_PER_FEED


def fetch_articles_from_feed(feed_config):
    """
    Download one RSS feed and return a list of article dicts.
    feed_config is a dict with keys: url, tier, name.
    """
    article_list = []
    feed_url = feed_config["url"]
    try:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:MAX_ARTICLES_PER_FEED]:
            title = entry.get("title", "").strip()
            summary = entry.get("summary", entry.get("description", "")).strip()
            link = entry.get("link", "")
            if title:
                article_list.append({
                    "title": title,
                    "summary": summary,
                    "link": link,
                    "source_tier": feed_config.get("tier", ""),
                    "source_name": feed_config.get("name", ""),
                })
    except Exception as error:
        print(f"Warning: could not fetch feed {feed_url} — {error}")
    return article_list


def fetch_all_topics(topics_dict):
    """
    Fetch articles for every topic in topics_dict.
    Returns a dict mapping topic name to a list of article dicts.
    Each article includes source_tier and source_name from the feed config.
    """
    articles_by_topic = {}

    for topic_name, feed_configs in topics_dict.items():
        topic_articles = []
        for feed_config in feed_configs:
            fetched = fetch_articles_from_feed(feed_config)
            topic_articles.extend(fetched)

        articles_by_topic[topic_name] = topic_articles
        print(f"Fetched {len(topic_articles)} articles for '{topic_name}'")

    return articles_by_topic
