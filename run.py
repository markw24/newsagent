# run.py — entry point: fetches RSS feeds, summarizes with OpenAI, builds index.html

from config import TOPICS
from fetch_feeds import fetch_all_topics
from fetch_markets import fetch_markets
from summarize import summarize_all_topics
from build_page import build_html


def main():
    print("=== The Daily Edge ===")

    print("\n[1/4] Fetching RSS feeds...")
    articles_by_topic = fetch_all_topics(TOPICS)

    print("\n[2/4] Fetching market data...")
    market_data = fetch_markets()

    print("\n[3/4] Summarizing with OpenAI...")
    summaries_by_topic = summarize_all_topics(articles_by_topic)

    print("\n[4/4] Building index.html...")
    build_html(summaries_by_topic, articles_by_topic, market_data)

    print("\nDone. Open index.html to view your daily briefing.")


if __name__ == "__main__":
    main()
