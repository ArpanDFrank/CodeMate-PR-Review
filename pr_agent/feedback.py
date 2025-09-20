# pr_agent/feedback.py
def aggregate_feedback(static_results: list, ai_results: dict) -> dict:
    """Combine static and AI feedback."""
    summary = "### Automated PR Review\n\n"
    inline_comments = []

    if static_results:
        summary += "#### Static Analysis\n"
        for f in static_results:
            summary += f"- **{f['severity']}**: {f['message']} at {f['file']}:{f['line']}\n"
            inline_comments.append({"file": f['file'], "line": f['line'], "comment": f"Static check: {f['message']}"})
    else:
        summary += "No static analysis issues found.\n"

    summary += "\n#### AI Review\n" + ai_results.get("summary", "")

    if ai_results.get("inline_comments"):
        inline_comments.extend(ai_results["inline_comments"])

    # Quality scoring
    score = 100 - len(static_results)*5 - len(ai_results.get("inline_comments", []))*3
    score = max(score, 0)

    return {"summary_report": summary, "inline_comments": inline_comments, "quality_score": score}
