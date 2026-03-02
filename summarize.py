# summarize.py — sends article text to OpenAI API and returns bullet-point summaries per topic

import os
import openai
from config import OPENAI_MODEL, MAX_ARTICLES_PER_FEED

SYSTEM_PROMPT = (
    "You are a concise news editor writing a daily briefing. "
    "Summarize the key stories in 4-6 bullet points. "
    "Be direct and factual. Start each bullet with •"
)


def build_article_text(article_list):
    """Convert a list of article dicts into a plain text block for the prompt."""
    lines = []
    for i, article in enumerate(article_list[:MAX_ARTICLES_PER_FEED * 2], start=1):
        lines.append(f"{i}. {article['title']}")
        if article.get("summary"):
            short_summary = article["summary"][:300]
            lines.append(f"   {short_summary}")
        lines.append("")
    return "\n".join(lines)


def summarize_topic(client, topic_name, article_list):
    """Make one OpenAI API call for a single topic and return bullet-point text."""
    if not article_list:
        return "• No articles available for this topic today."

    article_text = build_article_text(article_list)
    user_message = f"Here are today's articles about {topic_name}:\n\n{article_text}"

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            max_tokens=512,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as error:
        print(f"Warning: could not summarize '{topic_name}' — {error}")
        return "• Summary unavailable due to an error."


def summarize_all_topics(articles_by_topic):
    """
    Summarize every topic using one OpenAI API call per topic.
    Returns a dict mapping topic name to a bullet-point string.
    Reads OPENAI_API_KEY from the environment.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable is not set.")
        raise SystemExit(1)

    client = openai.OpenAI(api_key=api_key)
    summaries = {}

    for topic_name, article_list in articles_by_topic.items():
        print(f"Summarizing '{topic_name}'...")
        summaries[topic_name] = summarize_topic(client, topic_name, article_list)

    return summaries
