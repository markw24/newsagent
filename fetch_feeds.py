# fetch_feeds.py — downloads RSS feeds and returns a dict of article lists per topic

import feedparser
from config import MAX_ARTICLES_PER_FEED


def fetch_articles_from_feed(feed_url):
    """Download one RSS feed and return a list of article dicts."""
    article_list = []
    try:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:MAX_ARTICLES_PER_FEED]:
            title = entry.get("title", "").strip()
            summary = entry.get("summary", entry.get("description", "")).strip()
            if title:
                article_list.append({"title": title, "summary": summary})
    except Exception as error:
        print(f"Warning: could not fetch feed {feed_url} — {error}")
    return article_list


def fetch_all_topics(topics_dict):
    """
    Fetch articles for every topic in topics_dict.
    Returns a dict mapping topic name to a list of article dicts.
    Example: {"VC & Startups": [{"title": ..., "summary": ...}, ...], ...}
    """
    articles_by_topic = {}

    for topic_name, feed_urls in topics_dict.items():
        topic_articles = []
        for feed_url in feed_urls:
            fetched = fetch_articles_from_feed(feed_url)
            topic_articles.extend(fetched)
            if len(topic_articles) >= MAX_ARTICLES_PER_FEED * len(feed_urls):
                break

        articles_by_topic[topic_name] = topic_articles
        print(f"Fetched {len(topic_articles)} articles for '{topic_name}'")

    return articles_by_topic
