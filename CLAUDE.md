# The Daily Edge — CLAUDE.md

A personal intelligence briefing that runs automatically every morning.
It fetches RSS feeds, analyzes them with OpenAI, and outputs a single
mobile-friendly HTML page. Runs free via GitHub Actions once per day.

---

## Project Goals

- Completely free to run (GitHub Actions free tier + OpenAI API)
- Beginner-friendly: files under 150 lines, simple variable names
- One output: a single `index.html` that looks good on mobile (including dark mode)
- Intelligence analysis, NOT bullet-point summaries — connect dots across articles
- Explain each file's purpose in comments at the top

---

## File Structure

```
daily-news-agent/
├── CLAUDE.md               # This file — project guide for Claude
├── README.md               # Human-readable project overview
├── requirements.txt        # Python packages to install
├── config.py               # RSS feed URLs and topic names
├── fetch_feeds.py          # Downloads and parses RSS feeds
├── fetch_markets.py        # Fetches live market data from Yahoo Finance
├── summarize.py            # Sends content to OpenAI for intelligence analysis
├── build_page.py           # Assembles the final HTML page (prose format)
├── run.py                  # Main script — calls the above in order
├── template.html           # HTML skeleton with {date} and {content} placeholders
└── .github/
    └── workflows/
        └── daily.yml       # GitHub Actions schedule (runs once per day)
```

---

## What Each File Does

| File | Purpose |
|------|---------|
| `config.py` | Lists topics and RSS feed URLs. Edit to change sources. |
| `fetch_feeds.py` | Uses `feedparser` to download feeds and return article lists. |
| `fetch_markets.py` | Uses `yfinance` to fetch market prices and daily changes. |
| `summarize.py` | Sends articles to OpenAI with an intelligence analyst prompt. Returns analytical prose per topic with sections: Situation Assessment, Signal vs Noise, Implications & Watch List, Contrarian Check. |
| `build_page.py` | Takes analysis text, parses section headers, renders as styled HTML prose (not bullet lists). Includes source links per topic. |
| `run.py` | Entry point. Calls fetch → markets → summarize → build in order. |
| `template.html` | HTML skeleton with dark mode support and typography for prose reading. |
| `daily.yml` | Tells GitHub to run `run.py` every morning and commit `index.html`. |

---

## Output Format

The AI produces ANALYTICAL PROSE, not bullet-point summaries. Each topic section has:
1. **Situation Assessment** — What's actually happening, synthesized across articles
2. **Signal vs Noise** — What matters vs what's ephemeral
3. **Implications & Watch List** — Second-order effects, specific things to monitor
4. **Contrarian Check** — Consensus view and what would break it

`build_page.py` parses these sections into styled `<h3>` headers and `<p>` paragraphs
inside a `<div class="analysis">` wrapper. It also appends source article links.

---

## Tech Stack

- **Language:** Python 3.11+
- **RSS parsing:** `feedparser`
- **Market data:** `yfinance`
- **Analysis:** OpenAI API (`gpt-4o-mini`)
- **Output:** Static HTML (no server, no database)
- **Automation:** GitHub Actions (free tier)
- **Hosting:** GitHub Pages (free)

---

## Coding Rules (enforce these always)

1. **File length:** Keep every file under 150 lines. Split if needed.
2. **Variable names:** Use plain English — `article_list`, not `al`.
3. **No paid services:** Do not suggest services that require a credit card to start.
4. **Comments:** One-line comment at top of every file explaining what it does.
5. **No classes unless necessary:** Plain functions, procedural and readable.
6. **Error handling:** Simple `try/except` with `print()`. No cryptic errors.
7. **No external databases:** All data in memory. Only output is `index.html`.
8. **Secrets via environment variables:** API keys from `os.environ`, never hardcoded.

---

## OpenAI API Usage Rules

- **Model:** Always use `gpt-4o-mini` — cheapest and fast enough.
- **Max tokens:** 800 per topic (increased from 512 to support prose analysis).
- **Prompt style:** System prompt contains the full intelligence analyst instructions. User prompt contains the raw article text.
- **One call per topic:** Batch all articles for a topic into a single API call.

---

## Future Direction (Phase 2)

This project will evolve into a personal intelligence system that combines:
1. RSS feeds (current — world news)
2. Personally saved articles from an iOS app (Save to KB, stored in Supabase)
3. Multi-day continuity (previous briefings fed back as context)

The synthesis layer will cross-reference personal research with world events.
See the architecture blueprint for full Phase 2 spec.

---

## Common Mistakes to Avoid

- Do not produce bullet-point summaries. The prompt explicitly requests prose analysis.
- Do not import `openai` inside a loop — import once at the top.
- Do not store article content in files — process in memory, discard after.
- Do not use `requests` for RSS — `feedparser` handles this.
- Do not commit `.env` files — use GitHub Secrets for the API key.
