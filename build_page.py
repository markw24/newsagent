# build_page.py — reads template.html, injects summaries and market data, writes index.html

import os
from datetime import date

TEMPLATE_FILE = "template.html"
OUTPUT_FILE = "index.html"


def bullets_to_html(bullet_text):
    """Convert lines starting with • into an HTML unordered list."""
    lines = bullet_text.strip().splitlines()
    list_items = []
    for line in lines:
        line = line.strip()
        if line.startswith("•"):
            item_text = line[1:].strip()
            list_items.append(f"    <li>{item_text}</li>")
        elif line:
            # Non-bullet lines (e.g. intro sentences) become their own list item
            list_items.append(f"    <li>{line}</li>")
    if not list_items:
        return "<ul><li>No summary available.</li></ul>"
    return "<ul>\n" + "\n".join(list_items) + "\n  </ul>"


def build_sources_html(article_list):
    """Build a sources div with links to original articles. Max 5 links."""
    links = []
    for article in article_list[:5]:
        link = article.get("link", "")
        title = article.get("title", "")
        if link and title:
            links.append(f'    <a href="{link}">{title}</a>')
    if not links:
        return ""
    return '  <div class="sources">\n' + "\n".join(links) + "\n  </div>"


def build_section(topic_name, bullet_text, article_list):
    """Wrap a topic name, bullet summary, and source links in a <section> block."""
    html_list = bullets_to_html(bullet_text)
    sources_html = build_sources_html(article_list)
    section = (
        f"  <section>\n"
        f"    <h2>{topic_name}</h2>\n"
        f"    {html_list}\n"
        f"{sources_html}\n"
        f"  </section>"
    )
    return section


def build_market_dashboard(market_data):
    """Build an HTML market dashboard section. Returns empty string if no data."""
    if not market_data:
        return ""

    cards = []
    for item in market_data:
        pct = item["pct"]
        price = item["price"]
        direction = "up" if pct >= 0 else "down"
        pct_sign = "+" if pct >= 0 else ""

        # Format price based on symbol type
        if item["symbol"] == "BTC-USD":
            price_str = f"${price:,.0f}"
        elif item["symbol"] == "^TNX":
            price_str = f"{price:.2f}%"
        elif item["symbol"] == "^VIX":
            price_str = f"{price:.2f}"
        else:
            price_str = f"{price:,.2f}"

        change_html = f'<div class="market-change">{pct_sign}{pct:.2f}%</div>'
        label_html = ""
        if item["label"]:
            label_html = f'\n      <div class="vix-label">{item["label"]}</div>'

        card = (
            f'    <div class="market-card {direction}">\n'
            f'      <div class="market-name">{item["name"]}</div>\n'
            f'      <div class="market-price">{price_str}</div>\n'
            f'      {change_html}{label_html}\n'
            f'    </div>'
        )
        cards.append(card)

    cards_html = "\n".join(cards)
    return (
        f'  <section class="market-dashboard">\n'
        f'    <h2>Markets</h2>\n'
        f'    <div class="market-grid">\n'
        f'{cards_html}\n'
        f'    </div>\n'
        f'  </section>'
    )


def build_html(summaries_by_topic, articles_by_topic, market_data):
    """
    Read template.html, inject market dashboard, today's date, and topic summaries.
    Write result to index.html.
    """
    try:
        with open(TEMPLATE_FILE, "r", encoding="utf-8") as template_file:
            template_text = template_file.read()
    except Exception as error:
        print(f"Error: could not read {TEMPLATE_FILE} — {error}")
        raise SystemExit(1)

    market_html = build_market_dashboard(market_data)

    section_blocks = []
    if market_html:
        section_blocks.append(market_html)
    for topic_name, bullet_text in summaries_by_topic.items():
        article_list = articles_by_topic.get(topic_name, [])
        section_blocks.append(build_section(topic_name, bullet_text, article_list))

    content_html = "\n\n".join(section_blocks)
    today_string = date.today().strftime("%A, %B %-d, %Y")

    final_html = template_text.replace("{date}", today_string)
    final_html = final_html.replace("{content}", content_html)

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as output_file:
            output_file.write(final_html)
        print(f"Wrote {OUTPUT_FILE} successfully.")
    except Exception as error:
        print(f"Error: could not write {OUTPUT_FILE} — {error}")
        raise SystemExit(1)
