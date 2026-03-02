# build_page.py — reads template.html, injects summaries, and writes index.html

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


def build_section(topic_name, bullet_text):
    """Wrap a topic name and its bullet summary in a <section> block."""
    html_list = bullets_to_html(bullet_text)
    return (
        f"  <section>\n"
        f"    <h2>{topic_name}</h2>\n"
        f"    {html_list}\n"
        f"  </section>"
    )


def build_html(summaries_by_topic):
    """
    Read template.html, inject today's date and topic summaries, write index.html.
    summaries_by_topic: dict of topic_name -> bullet-point string from Claude.
    """
    try:
        with open(TEMPLATE_FILE, "r", encoding="utf-8") as template_file:
            template_text = template_file.read()
    except Exception as error:
        print(f"Error: could not read {TEMPLATE_FILE} — {error}")
        raise SystemExit(1)

    section_blocks = []
    for topic_name, bullet_text in summaries_by_topic.items():
        section_blocks.append(build_section(topic_name, bullet_text))

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
