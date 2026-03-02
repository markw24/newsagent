# The Daily Edge

A personal daily news briefing that runs automatically every morning.
It fetches RSS feeds, summarizes the top stories with OpenAI, and
publishes a clean mobile-friendly page to GitHub Pages — completely free.

---

## What You Get

- 4 topic sections: VC & Startups, Geopolitics, World News, Financial News
- 4–6 bullet-point summaries per topic
- A single `index.html` that loads instantly on any device
- Automatic daily updates at 7 AM UTC via GitHub Actions

---

## Setup (start here after adding your secret)

You've already added `OPENAI_API_KEY` as a GitHub secret. Now do these 3 things:

**1. Enable GitHub Pages**

Go to your repo → Settings → Pages → Source: Deploy from a branch →
Branch: `main`, folder: `/ (root)` → click Save.

**2. Trigger the first run**

Go to your repo → Actions → Daily Briefing → click "Run workflow" → Run workflow.
Wait about 60 seconds. When it finishes, `index.html` will appear in your repo.

**3. View your live page**

```
https://markw24.github.io/newsagent/
```

That's it. Every morning at 7 AM UTC it runs automatically and updates the page.

---

## Controlling the Schedule

The schedule is set in `.github/workflows/daily.yml`:

```yaml
- cron: "0 7 * * *"   # 7 AM UTC every day
```

Change `0 7` to whatever time you want. Format is `minute hour` in UTC.
Examples:
- `0 6 * * *` — 6 AM UTC (1 AM US Eastern, 2 PM Sydney)
- `0 12 * * *` — 12 PM UTC (noon)
- `0 7 * * 1-5` — weekdays only

To apply the change: edit the file, commit it, push it.

**To trigger a run manually at any time:**
Go to Actions → Daily Briefing → Run workflow.

**To pause the schedule:**
Go to Actions → Daily Briefing → click the `...` menu → Disable workflow.
Re-enable it the same way when you want it back.

---

## Changing Topics or Feeds

Open `config.py`. Edit the `TOPICS` dict — change the keys (topic names) and
the lists of RSS feed URLs. Any public RSS feed URL works.

```python
TOPICS = {
    "My Topic": [
        "https://example.com/feed.rss",
    ],
}
```

After saving, commit and push the file. The next run will use the new topics.

---

## Changing the Summary Style

Open `summarize.py`. Edit the `SYSTEM_PROMPT` string near the top of the file.
For example, change "4-6 bullet points" to "2-3 sentences" for shorter summaries.

After saving, commit and push.

---

## How to Push Any Change

```bash
cd /Users/markwang/projects/daily-news-agent
git add .
git commit -m "describe your change here"
git push
```

---

## Cost

- GitHub Actions: free (well within the 2,000 min/month free tier)
- GitHub Pages: free
- OpenAI API: ~$0.001–0.003 per daily run using `gpt-4o-mini`

---

## File Overview

| File | What it does |
|------|-------------|
| `config.py` | Topics, RSS URLs, and model name |
| `fetch_feeds.py` | Downloads RSS feeds with feedparser |
| `summarize.py` | Calls OpenAI API to summarize articles |
| `build_page.py` | Assembles template + summaries → index.html |
| `run.py` | Entry point — calls the above in order |
| `template.html` | HTML skeleton with `{date}` and `{content}` placeholders |
| `.github/workflows/daily.yml` | GitHub Actions schedule |
