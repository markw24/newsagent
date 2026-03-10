# summarize.py — sends article text to OpenAI API and returns intelligence analysis per topic

import os
import openai
from config import OPENAI_MODEL, MAX_ARTICLES_PER_FEED

SYSTEM_PROMPT = (
    "You are an intelligence analyst producing a morning briefing for a strategic "
    "thinker who tracks technology, startups, geopolitics, and financial markets.\n\n"
    "You will receive articles grouped by topic. Your job is NOT to summarize each "
    "article individually. Instead, SYNTHESIZE across all articles to produce "
    "analytical intelligence.\n\n"
    "Produce the following sections:\n\n"
    "SITUATION ASSESSMENT (3-5 sentences)\n"
    "What is actually happening right now in this space? Synthesize across all the "
    "articles to paint a coherent picture. Connect dots between articles — if one "
    "reports a policy change and another reports a market reaction, link them. "
    "Write in analytical prose, not bullet points.\n\n"
    "SIGNAL VS NOISE (2-3 sentences)\n"
    "Of everything reported today, what actually matters and what is ephemeral? "
    "Be opinionated. If three articles cover the same non-event, say so. If one "
    "buried detail in one article is more significant than all the headlines "
    "combined, call it out.\n\n"
    "IMPLICATIONS & WATCH LIST (2-4 sentences)\n"
    "What are the second-order effects? What should the reader monitor over the "
    "coming days and weeks? Be specific — name the companies, policies, people, "
    "or metrics to watch. Not 'this could affect markets' but 'watch [specific "
    "thing] because [specific reason].'\n\n"
    "CONTRARIAN CHECK (1-2 sentences)\n"
    "What is the consensus view across these articles, and what would need to be "
    "true for that consensus to be wrong?\n\n"
    "RELEVANCE SCORING:\n"
    "Before analyzing, mentally score each article on these dimensions (0-5 each):\n"
    "1. Strategic relevance — Does this affect how power, capital, or technology flows?\n"
    "2. Structural insight — Does this reveal a structural change, not just a daily event?\n"
    "3. Actionability — Could someone make a better decision knowing this?\n"
    "4. Novelty — Is this genuinely new information or a rehash?\n"
    "Only include articles scoring 12/20 or higher in your analysis. "
    "If most articles score below threshold, say so — 'Today's coverage was thin on "
    "substance' is more valuable than manufacturing analysis from noise.\n\n"
    "SOURCE TIERING:\n"
    "Articles are labeled with source tiers. Weight Tier 1 sources most heavily. "
    "When multiple outlets report the same story, use the highest-tier source. "
    "Do not repeat the same story twice.\n\n"
    "RULES:\n"
    "- NEVER produce bullet-point summaries of individual articles.\n"
    "- ALWAYS connect articles to each other, even across topics if relevant.\n"
    "- Be direct and opinionated. Say 'This matters because...' not 'Some analysts believe...'\n"
    "- If the articles are thin or repetitive, say so. Do not manufacture insight from noise.\n"
    "- Keep total output for this topic to 150-250 words. Dense, not long.\n"
    "- Use these exact section headers: SITUATION ASSESSMENT, SIGNAL VS NOISE, "
    "IMPLICATIONS & WATCH LIST, CONTRARIAN CHECK.\n"
    "- Do NOT use bullet points or bullet characters. Write in prose paragraphs."
)


def build_article_text(article_list):
    """Convert a list of article dicts into a plain text block for the prompt.
    Prepends [Tier N — Source Name] to each article title for source tiering.
    """
    lines = []
    for i, article in enumerate(article_list[:MAX_ARTICLES_PER_FEED * 2], start=1):
        tier = article.get("tier", "")
        source_name = article.get("source_name", "")
        tier_label = f"[Tier {tier} — {source_name}] " if tier and source_name else ""
        lines.append(f"{i}. {tier_label}{article['title']}")
        if article.get("summary"):
            short_summary = article["summary"][:300]
            lines.append(f"   {short_summary}")
        lines.append("")
    return "\n".join(lines)


def summarize_topic(client, topic_name, article_list):
    """Make one OpenAI API call for a single topic and return analytical text."""
    if not article_list:
        return "No articles available for this topic today."

    article_text = build_article_text(article_list)
    user_message = f"Here are today's articles about {topic_name}:\n\n{article_text}"

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            max_tokens=800,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as error:
        print(f"Warning: could not summarize '{topic_name}' — {error}")
        return "Analysis unavailable due to an error."


def summarize_all_topics(articles_by_topic):
    """
    Analyze every topic using one OpenAI API call per topic.
    Returns a dict mapping topic name to analytical text.
    Reads OPENAI_API_KEY from the environment.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable is not set.")
        raise SystemExit(1)

    client = openai.OpenAI(api_key=api_key)
    summaries = {}

    for topic_name, article_list in articles_by_topic.items():
        print(f"Analyzing '{topic_name}'...")
        summaries[topic_name] = summarize_topic(client, topic_name, article_list)

    return summaries
