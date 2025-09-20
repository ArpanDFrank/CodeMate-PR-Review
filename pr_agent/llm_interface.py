# pr_agent/llm_interface.py
import os
import openai
from pr_agent.utils import parse_inline_comments
from pr_agent.config import OPENAI_API_KEY

def generate_review_with_llm(diff_text: str) -> dict:
    """Generate AI-based review using OpenAI."""
    if not OPENAI_API_KEY:
        print("OpenAI API key missing. Skipping AI review.")
        return {"summary": "AI review skipped.", "inline_comments": []}

    openai.api_key = OPENAI_API_KEY

    system_msg = {
        "role": "system",
        "content": (
            "You are a professional software engineer reviewing a PR. "
            "Provide summary and inline comments. Format strictly:\n"
            "Summary: [overall summary]\n"
            "### Inline Comments:\n"
            "- File `[path]`, line [num]: [comment]"
        )
    }

    prompt = f"Review the following diff:\n```diff\n{diff_text}\n```"

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[system_msg, {"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1000,
        )
        text = response.choices[0].message.content.strip()
        parts = text.split("### Inline Comments:", 1)
        summary = parts[0].replace("Summary:", "").strip()
        inline_comments = parse_inline_comments(parts[1].strip() if len(parts) > 1 else "")
        return {"summary": summary, "inline_comments": inline_comments}
    except Exception as e:
        print(f"AI review error: {e}")
        return {"summary": f"Error: {e}", "inline_comments": []}
