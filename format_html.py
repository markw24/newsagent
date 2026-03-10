# format_html.py — converts analysis text and data into styled HTML fragments

import re

# Section headers the AI is instructed to produce
ANALYSIS_HEADERS = [
    "SITUATION ASSESSMENT",
    "SIGNAL VS NOISE",
    "IMPLICATIONS & WATCH LIST",
    "IMPLICATIONS &amp; WATCH LIST",
    "CONTRARIAN CHECK",
]


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
        label_html = f'<div class="vix-label">{item["label"]}</div>' if item.get("label") else ""
        cards.append(
            f'<div class="market-card {direction}">'
            f'<div class="market-name">{item["name"]}</div>'
            f'<div class="market-price">{price_str}</div>'
            f'<div class="market-change">{change_str}</div>'
            f'{label_html}</div>'
        )

    return (
        '<section><h2>Markets</h2>'
        '<div class="market-grid">' + "".join(cards) + '</div></section>'
    )


def format_analysis_html(analysis_text):
    """Convert AI analysis text into styled HTML with h3 section headers and p tags."""
    if not analysis_text:
        return '<div class="analysis"><p>No analysis available.</p></div>'

    lines = analysis_text.split("\n")
    html_parts = []
    current_paragraph = []

    def flush():
        text = " ".join(current_paragraph).strip()
        if text:
            html_parts.append(f"<p>{text}</p>")
        current_paragraph.clear()

    for line in lines:
        stripped = line.strip()
        if not stripped:
            flush()
            continue
        clean = re.sub(r'^[#*\s]+', '', stripped)
        clean = re.sub(r'[*:]+$', '', clean).strip()
        is_header = False
        for header in ANALYSIS_HEADERS:
            if clean.upper() == header or clean.upper().startswith(header):
                flush()
                html_parts.append(f"<h3>{header.title()}</h3>")
                remainder = clean[len(header):].strip().lstrip(':').strip()
                if remainder:
                    current_paragraph.append(remainder)
                is_header = True
                break
        if not is_header:
            cleaned_line = re.sub(r'^[•\-\*]\s*', '', stripped)
            current_paragraph.append(cleaned_line)

    flush()
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


def format_signal_box_html(signal_box_text):
    """Parse pipe-delimited Signal Box rows into an HTML table section."""
    if not signal_box_text:
        return ""
    rows = []
    for line in signal_box_text.strip().split("\n"):
        line = line.strip()
        if not line or "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 3 or parts[0].lower() == "signal":
            continue
        signal, direction, comment = parts[0], parts[1], " | ".join(parts[2:])
        dir_class = f"sb-{direction.lower()}"
        rows.append(
            f'<tr><td class="sb-signal">{signal}</td>'
            f'<td class="sb-direction {dir_class}">{direction}</td>'
            f'<td class="sb-comment">{comment}</td></tr>'
        )
    if not rows:
        return ""
    return (
        '<section><h2>Signal Box</h2>'
        '<table class="signal-box">'
        '<thead><tr><th>Signal</th><th>Dir</th><th>Comment</th></tr></thead>'
        '<tbody>' + "".join(rows) + '</tbody>'
        '</table></section>'
    )


def format_theme_html(theme_text):
    """Wrap theme text in a styled card section, or return empty string."""
    if not theme_text or theme_text.strip().lower() == "none today":
        return ""
    return (
        '<section>'
        '<div class="theme-card">'
        '<div class="theme-label">Theme of the Day</div>'
        f'<p>{theme_text}</p>'
        '</div></section>'
    )
