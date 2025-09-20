# pr_agent/utils.py
import re

def print_banner(msg):
    print("\n" + "="*len(msg)*2)
    print(f"| {msg} |")
    print("="*len(msg)*2 + "\n")

def parse_inline_comments(text: str) -> list:
    """Parse inline comments formatted like: File `file.py`, line 12: comment"""
    comments = []
    pattern = r"File `(.*?)`, line (\d+):\s*(.*)"
    for line in text.splitlines():
        m = re.match(pattern, line.strip())
        if m:
            file_path, line_num, comment = m.groups()
            comments.append({"file": file_path, "line": int(line_num), "comment": comment})
    return comments
