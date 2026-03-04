# build_page.py — takes analysis text and market data, writes index.html from template

import re
from datetime import datetime, timezone


def format_market_html(market_data):
    """Build the market data grid HTML."""
    if not market_data:
        return ""

    cards = []
    for item in market_data:
        direction = "up" if item["change"] >= 0 else "down"
        sign = "+" if item["change"] >= 0 else ""

        # Format price based on size
        price = item["price"]
        if price >= 1000:
            price_str = f"{price:,.0f}"
        elif price >= 100:
            price_str = f"{price:.1f}"
        else:
            price_str = f"{price:.2f}"

        change_str = f"{sign}{item['pct']:.2f}%"
        label_html = ""
        if item.get("label"):
            label_html = f'<div class="vix-label">{item["label"]}</div>'

        cards.append(
            f'<div class="market-card {direction}">'
            f'<div class="market-name">{item["name"]}</div>'
            f'<div class="market-price">{price_str}</div>'
            f'<div class="market-change">{change_str}</div>'
            f'{label_html}'
            f'</div>'
        )

    return (
        '<section><h2>Markets</h2>'
        '<div class="market-grid">' + "".join(cards) + '</div>'
        '</section>'
    )


def format_analysis_html(analysis_text):
    """
    Convert the AI analysis text into styled HTML.
    Wraps section headers (like SITUATION ASSESSMENT) in <h3> tags
    and regular text in <p> tags inside a div.analysis wrapper.
    """
    if not analysis_text:
        return '<div class="analysis"><p>No analysis available.</p></div>'

    # Known section headers from the prompt
    headers = [
        "SITUATION ASSESSMENT",
        "SIGNAL VS NOISE",
        "IMPLICATIONS & WATCH LIST",
        "IMPLICATIONS &amp; WATCH LIST",
        "CONTRARIAN CHECK",
    ]

    lines = analysis_text.split("\n")
    html_parts = []
    current_paragraph = []

    def flush_paragraph():
        text = " ".join(current_paragraph).strip()
        if text:
            html_parts.append(f"<p>{text}</p>")
        current_paragraph.clear()

    for line in lines:
        stripped = line.strip()

        # Skip empty lines — they break paragraphs
        if not stripped:
            flush_paragraph()
            continue

        # Check if this line is a section header
        # Match patterns like "SITUATION ASSESSMENT", "**SITUATION ASSESSMENT**",
        # "### SITUATION ASSESSMENT", "SITUATION ASSESSMENT:"
        clean = re.sub(r'^[#*\s]+', '', stripped)
        clean = re.sub(r'[*:]+$', '', clean).strip()

        is_header = False
        for header in headers:
            if clean.upper() == header or clean.upper().startswith(header):
                flush_paragraph()
                html_parts.append(f"<h3>{header.title()}</h3>")
                # If there's text after the header on the same line, start a paragraph
                remainder = clean[len(header):].strip().lstrip(':').strip()
                if remainder:
                    current_paragraph.append(remainder)
                is_header = True
                break

        if not is_header:
            # Strip any leading bullet characters the AI might sneak in
            cleaned_line = re.sub(r'^[•\-\*]\s*', '', stripped)
            current_paragraph.append(cleaned_line)

    flush_paragraph()

    return '<div class="analysis">' + "\n".join(html_parts) + '</div>'


def format_sources_html(article_list):
    """Build a compact list of source links for a topic."""
    if not article_list:
        return ""

    seen_titles = set()
    links = []
    for article in article_list[:8]:
        title = article.get("title", "")
        link = article.get("link", "")
        if not link or title in seen_titles:
            continue
        seen_titles.add(title)
        short_title = title[:60] + "..." if len(title) > 60 else title
        links.append(f'<a href="{link}" target="_blank">{short_title}</a>')

    if not links:
        return ""

    return '<div class="sources">' + " ".join(links) + '</div>'


def build_html(summaries_by_topic, articles_by_topic, market_data):
    """Assemble the final index.html from template, analysis, and market data."""

    today = datetime.now(timezone.utc).strftime("%A, %B %-d, %Y")

    # Build market section
    content_parts = []
    market_html = format_market_html(market_data)
    if market_html:
        content_parts.append(market_html)

    # Build topic sections
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

    # Read template and fill in placeholders
    with open("template.html", "r") as f:
        template = f.read()

    html = template.replace("{date}", today).replace("{content}", content)

    with open("index.html", "w") as f:
        f.write(html)

    print(f"Wrote index.html ({len(html):,} bytes)")
