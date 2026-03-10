# synthesize.py — makes one cross-topic OpenAI call to produce Signal Box and Theme of the Day

import os
import openai
from config import OPENAI_MODEL

SYNTHESIS_PROMPT = (
    "You are an intelligence analyst producing a cross-topic synthesis for a morning briefing.\n\n"
    "You will receive intelligence analyses from multiple topics. Your job is to:\n"
    "1. Identify the 3-5 most significant signals across all topics.\n"
    "2. Identify the single overarching theme or tension of the day (if one exists).\n\n"
    "Produce your response in EXACTLY this format:\n\n"
    "SIGNAL BOX:\n"
    "Signal | Direction | Comment\n"
    "[signal name] | [Up/Down/Watch/Neutral] | [one sentence comment]\n"
    "(repeat for each signal, 3-5 rows total)\n\n"
    "THEME OF THE DAY:\n"
    "[3-4 sentences connecting the day's biggest threads, or 'None today' if no clear theme]\n\n"
    "RULES:\n"
    "- Signal names: 2-4 words, e.g. 'Fed Rate Bets', 'AI Regulation', 'Ukraine Talks'\n"
    "- Direction must be exactly one of: Up, Down, Watch, Neutral\n"
    "- Each comment is exactly one sentence — no more.\n"
    "- Do not add any other sections or text outside this format."
)


def synthesize_all_topics(summaries_by_topic):
    """
    Make one OpenAI call across all topic summaries.
    Returns (signal_box_text, theme_text) as strings.
    Reads OPENAI_API_KEY from the environment.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Warning: OPENAI_API_KEY not set — skipping synthesis.")
        return "", ""

    combined = ""
    for topic_name, analysis in summaries_by_topic.items():
        combined += f"=== {topic_name} ===\n{analysis}\n\n"

    client = openai.OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            max_tokens=600,
            messages=[
                {"role": "system", "content": SYNTHESIS_PROMPT},
                {"role": "user", "content": combined},
            ],
        )
        raw = response.choices[0].message.content.strip()
    except Exception as error:
        print(f"Warning: synthesis failed — {error}")
        return "", ""

    # Split on THEME OF THE DAY: to separate signal box from theme
    if "THEME OF THE DAY:" in raw:
        parts = raw.split("THEME OF THE DAY:", 1)
        signal_box_text = parts[0].replace("SIGNAL BOX:", "").strip()
        theme_text = parts[1].strip()
    else:
        signal_box_text = raw.replace("SIGNAL BOX:", "").strip()
        theme_text = ""

    return signal_box_text, theme_text
