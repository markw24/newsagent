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


def format_signal_box_html(synthesis_text):
    """Parse synthesis text and render the Signal Box as an HTML table."""
    if not synthesis_text:
        return ""

    lines = synthesis_text.split("\n")
    in_signal_box = False
    rows = []

    for line in lines:
        stripped = line.strip()
        if re.match(r'^SIGNAL BOX', stripped, re.IGNORECASE):
            in_signal_box = True
            continue
        if re.match(r'^THEME OF THE DAY', stripped, re.IGNORECASE):
            break
        if in_signal_box and "|" in stripped:
            parts = [p.strip() for p in stripped.split("|")]
            if len(parts) == 3:
                rows.append(parts)

    if not rows:
        return ""

    dir_css = {
        "rising": "dir-up", "accelerating": "dir-up", "emerging": "dir-up",
        "falling": "dir-down", "weakening": "dir-down",
        "stable": "dir-stable", "shifting": "dir-shift",
    }

    row_html = ""
    for signal, direction, comment in rows:
        css = dir_css.get(direction.lower(), "dir-stable")
        row_html += (
            f'<tr>'
            f'<td class="sig-label">{signal}</td>'
            f'<td class="sig-dir {css}">{direction}</td>'
            f'<td class="sig-comment">{comment}</td>'
            f'</tr>'
        )

    return (
        '<section class="signal-box">'
        '<h2>Signal Box</h2>'
        '<table class="signal-table"><tbody>'
        + row_html +
        '</tbody></table></section>'
    )


def format_theme_html(synthesis_text):
    """Extract Theme of the Day from synthesis text and render as a styled section."""
    if not synthesis_text:
        return ""

    lines = synthesis_text.split("\n")
    in_theme = False
    theme_lines = []

    for line in lines:
        stripped = line.strip()
        if re.match(r'^THEME OF THE DAY', stripped, re.IGNORECASE):
            in_theme = True
            remainder = re.sub(r'^THEME OF THE DAY\s*:?\s*', '', stripped, flags=re.IGNORECASE).strip()
            if remainder:
                theme_lines.append(remainder)
            continue
        if in_theme and stripped:
            theme_lines.append(stripped)

    theme_text = " ".join(theme_lines).strip()
    if not theme_text or theme_text.lower() == "none":
        return ""

    return (
        '<section class="theme-of-day">'
        '<h2>Theme of the Day</h2>'
        f'<p>{theme_text}</p>'
        '</section>'
    )


def format_analysis_html(analysis_text):
    """
    Convert the AI analysis text into styled HTML.
    Wraps section headers in <h3> tags and regular text in <p> tags.
    """
    if not analysis_text:
        return '<div class="analysis"><p>No analysis available.</p></div>'

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
        if not stripped:
            flush_paragraph()
            continue

        clean = re.sub(r'^[#*\s]+', '', stripped)
        clean = re.sub(r'[*:]+$', '', clean).strip()

        is_header = False
        for header in headers:
            if clean.upper() == header or clean.upper().startswith(header):
                flush_paragraph()
                html_parts.append(f"<h3>{header.title()}</h3>")
                remainder = clean[len(header):].strip().lstrip(':').strip()
                if remainder:
                    current_paragraph.append(remainder)
                is_header = True
                break

        if not is_header:
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


def build_html(summaries_by_topic, articles_by_topic, market_data, synthesis_text=""):
    """Assemble the final index.html from template, analysis, market data, and synthesis."""

    today = datetime.now(timezone.utc).strftime("%A, %B %-d, %Y")

    content_parts = []

    market_html = format_market_html(market_data)
    if market_html:
        content_parts.append(market_html)

    signal_box_html = format_signal_box_html(synthesis_text)
    if signal_box_html:
        content_parts.append(signal_box_html)

    theme_html = format_theme_html(synthesis_text)
    if theme_html:
        content_parts.append(theme_html)

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
