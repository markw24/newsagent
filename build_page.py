# build_page.py — assembles the final index.html from template, analysis, markets, and signals

from datetime import datetime, timezone
from format_html import (
    format_market_html,
    format_analysis_html,
    format_sources_html,
    format_signal_box_html,
    format_theme_html,
)


def build_html(summaries_by_topic, articles_by_topic, market_data, signal_box="", theme=""):
    """Assemble the final index.html from template, analysis, and market data."""

    today = datetime.now(timezone.utc).strftime("%A, %B %-d, %Y")
    content_parts = []

    # Markets section
    market_html = format_market_html(market_data)
    if market_html:
        content_parts.append(market_html)

    # Signal box + theme appear after markets, before topic sections
    signal_html = format_signal_box_html(signal_box)
    if signal_html:
        content_parts.append(signal_html)

    theme_html = format_theme_html(theme)
    if theme_html:
        content_parts.append(theme_html)

    # Topic sections
    for topic_name, analysis_text in summaries_by_topic.items():
        analysis_html = format_analysis_html(analysis_text)
        sources_html = format_sources_html(articles_by_topic.get(topic_name, []))
        section = (
            f"<section>\n"
            f"  <h2>{topic_name}</h2>\n"
            f"  {analysis_html}\n"
            f"  {sources_html}\n"
            f"</section>"
        )
        content_parts.append(section)

    content = "\n\n".join(content_parts)

    with open("template.html", "r") as f:
        template = f.read()

    html = template.replace("{date}", today).replace("{content}", content)

    with open("index.html", "w") as f:
        f.write(html)

    print(f"Wrote index.html ({len(html):,} bytes)")
