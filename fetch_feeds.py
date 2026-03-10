# fetch_feeds.py — downloads RSS feeds and returns a dict of article lists per topic

import feedparser
from config import MAX_ARTICLES_PER_FEED


def fetch_articles_from_feed(feed_entry):
    """Download one RSS feed and return a list of article dicts.
    feed_entry is a dict with 'url', 'tier', and 'name' keys.
    """
    article_list = []
    feed_url = feed_entry["url"]
    tier = feed_entry["tier"]
    source_name = feed_entry["name"]
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
                    "tier": tier,
                    "source_name": source_name,
                })
    except Exception as error:
        print(f"Warning: could not fetch feed {feed_url} — {error}")
    return article_list


def fetch_all_topics(topics_dict):
    """
    Fetch articles for every topic in topics_dict.
    Returns a dict mapping topic name to a list of article dicts.
    Each article dict includes 'title', 'summary', 'link', 'tier', 'source_name'.
    """
    articles_by_topic = {}

    for topic_name, feed_entries in topics_dict.items():
        topic_articles = []
        for feed_entry in feed_entries:
            fetched = fetch_articles_from_feed(feed_entry)
            topic_articles.extend(fetched)

        articles_by_topic[topic_name] = topic_articles
        print(f"Fetched {len(topic_articles)} articles for '{topic_name}'")

    return articles_by_topic
