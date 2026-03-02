# The Daily Edge — CLAUDE.md

A personal daily briefing app that fetches RSS feeds, summarizes them with Claude AI,
and outputs a single mobile-friendly HTML page. Runs free via GitHub Actions once per day.

---

## Project Goals

- Completely free to run (GitHub Actions free tier + Claude API)
- Beginner-friendly: files under 150 lines, simple variable names
- One output: a single `index.html` file that looks good on mobile
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
├── summarize.py            # Sends content to Claude API for summaries
├── build_page.py           # Assembles the final HTML page
├── run.py                  # Main script — calls the above in order
├── template.html           # HTML skeleton with a {content} placeholder
└── .github/
    └── workflows/
        └── daily.yml       # GitHub Actions schedule (runs once per day)
```

---

## What Each File Does

| File | Purpose |
|------|---------|
| `config.py` | Lists the 4 topics and their RSS feed URLs. Edit this to change sources. |
| `fetch_feeds.py` | Uses `feedparser` to download each feed and return a list of articles. |
| `summarize.py` | Sends article text to Claude API and gets back a short summary per topic. |
| `build_page.py` | Takes the summaries and writes them into `template.html` → `index.html`. |
| `run.py` | The entry point. Calls fetch → summarize → build in order. |
| `template.html` | A plain HTML file with a `{content}` marker where summaries are inserted. |
| `daily.yml` | Tells GitHub to run `run.py` every morning and commit `index.html`. |

---

## Tech Stack

- **Language:** Python 3.11+
- **RSS parsing:** `feedparser` (free, no API key needed)
- **Summarization:** Anthropic Claude API (`claude-haiku-4-5-20251001` — cheapest model)
- **Output:** Static HTML (no server, no database)
- **Automation:** GitHub Actions (free tier: 2,000 minutes/month)
- **Hosting:** GitHub Pages (free static site hosting)

---

## Coding Rules (enforce these always)

1. **File length:** Keep every file under 150 lines. Split logic into a new file if needed.
2. **Variable names:** Use plain English words — `article_list`, not `al` or `artLst`.
3. **No paid services:** Do not suggest services that require a credit card to start.
4. **Comments:** Add a one-line comment at the top of every file explaining what it does.
5. **No classes unless necessary:** Use plain functions. Keep it procedural and readable.
6. **Error handling:** Use simple `try/except` with a `print()` message. Don't raise cryptic errors.
7. **No external databases:** All data lives in memory during the run. Only output is `index.html`.
8. **Secrets via environment variables:** API keys come from `os.environ`, never hardcoded.

---

## Topics (defined in config.py)

The app covers exactly 4 topics. Each topic has a name and a list of RSS feed URLs.

```python
TOPICS = {
    "Technology": [
        "https://feeds.arstechnica.com/arstechnica/index",
        "https://www.wired.com/feed/rss",
    ],
    "Science": [
        "https://www.sciencedaily.com/rss/all.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml",
    ],
    "World News": [
        "https://feeds.bbci.co.uk/news/world/rss.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    ],
    "Business": [
        "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
    ],
}
```

---

## Claude API Usage Rules

- **Model:** Always use `claude-haiku-4-5-20251001` — it is the cheapest and fast enough.
- **Max articles per topic:** Summarize at most 5 articles per topic to control token usage.
- **Prompt style:** Keep system prompts under 50 words. User prompts should contain the raw article text.
- **One call per topic:** Batch all articles for a topic into a single API call, not one call per article.

### Example prompt structure

```
System: You are a concise news editor. Summarize the key points from these articles in 3–5 bullet points. Be brief and factual.

User: [paste article headlines + first paragraphs here]
```

---

## GitHub Actions Setup

The workflow file (`.github/workflows/daily.yml`) should:

1. Run on a cron schedule: `0 7 * * *` (7 AM UTC daily)
2. Check out the repo
3. Install Python dependencies from `requirements.txt`
4. Run `python run.py`
5. Commit and push the updated `index.html` back to the repo

Required GitHub secret: `ANTHROPIC_API_KEY` — set this in repo Settings → Secrets.

---

## Output Format

`index.html` must:
- Work on mobile screens (use `max-width: 600px` and readable font sizes)
- Show today's date at the top
- Have one section per topic with a heading and bullet-point summaries
- Load instantly (no JavaScript, no external fonts, inline CSS only)
- Be a complete standalone file (no dependencies)

---

## Getting Started (for beginners)

1. Fork this repo on GitHub
2. Add your `ANTHROPIC_API_KEY` to repo Settings → Secrets → Actions
3. Enable GitHub Pages: Settings → Pages → Source: main branch, `/` (root)
4. Push any change to trigger the first run, or wait for the daily schedule
5. Your briefing page will be live at `https://your-username.github.io/daily-news-agent/`

---

## Common Mistakes to Avoid

- Do not use `f-strings` with multi-line prompts — use string concatenation or `textwrap.dedent()`.
- Do not import `anthropic` inside a loop — import once at the top of the file.
- Do not store article content in files — process everything in memory and discard it.
- Do not use `requests` to fetch RSS — `feedparser` handles this already.
- Do not commit `.env` files — use GitHub Secrets for the API key.
