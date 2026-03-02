# The Daily Edge

A personal daily news briefing that runs automatically every morning.
It fetches RSS feeds, summarizes the top stories with Claude AI, and
publishes a clean mobile-friendly page to GitHub Pages — completely free.

---

## What You Get

- 4 topic sections: VC & Startups, Geopolitics, World News, Financial News
- 4–6 bullet-point summaries per topic, written by Claude
- A single `index.html` that loads instantly on any device
- Automatic daily updates at 7 AM UTC via GitHub Actions

---

## 5-Step Setup

1. **Fork this repo** — click the Fork button at the top right of this page.

2. **Add your API key** — go to your fork's Settings → Secrets and variables →
   Actions → New repository secret. Name it `ANTHROPIC_API_KEY` and paste your
   key from [console.anthropic.com](https://console.anthropic.com).

3. **Enable GitHub Pages** — go to Settings → Pages → Source: Deploy from a
   branch → Branch: `main`, folder: `/ (root)` → Save.

4. **Trigger the first run** — go to Actions → Daily Briefing → Run workflow.
   The first `index.html` will appear in about a minute.

5. **Visit your briefing** — your live page is at:
   `https://<your-username>.github.io/daily-news-agent/`

After setup, the page updates automatically every morning. No further action needed.

---

## How to Change Topics

Open `config.py`. Edit the `TOPICS` dict — change the keys (topic names) and
the lists of RSS feed URLs. Any public RSS feed URL works.

```python
TOPICS = {
    "My Topic": [
        "https://example.com/feed.rss",
    ],
}
```

---

## How to Change the Summary Style

Open `summarize.py`. Edit the `SYSTEM_PROMPT` string near the top of the file.
For example, change "4-6 bullet points" to "2-3 sentences" for shorter output.

---

## Cost

- GitHub Actions: free (well within the 2,000 min/month free tier)
- GitHub Pages: free
- Claude API: ~$0.001–0.005 per daily run using `claude-haiku-4-5-20251001`

---

## File Overview

| File | What it does |
|------|-------------|
| `config.py` | Topics and RSS URLs |
| `fetch_feeds.py` | Downloads RSS feeds with feedparser |
| `summarize.py` | Calls Claude API to summarize articles |
| `build_page.py` | Assembles template + summaries → index.html |
| `run.py` | Entry point — calls the above in order |
| `template.html` | HTML skeleton with `{date}` and `{content}` placeholders |
| `.github/workflows/daily.yml` | GitHub Actions schedule |
