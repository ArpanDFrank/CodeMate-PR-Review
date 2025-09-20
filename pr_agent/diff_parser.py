# pr_agent/diff_parser.py
import re

def parse_diff(diff_text: str) -> dict:
    """Parse unified diff string into structured dictionary."""
    files_changed = {}
    current_file = None
    old_line_number = 0
    new_line_number = 0

    for line in diff_text.splitlines():
        if line.startswith('+++ b/'):
            current_file = line[6:].strip()
            files_changed[current_file] = []
        elif line.startswith('@@'):
            match = re.search(r'@@ -(\d+),?\d* \+(\d+),?\d* @@', line)
            if match:
                old_line_number = int(match.group(1)) - 1
                new_line_number = int(match.group(2)) - 1
            else:
                old_line_number = new_line_number = 0
        elif current_file:
            if line.startswith('+'):
                new_line_number += 1
                files_changed[current_file].append({
                    'old_line': None,
                    'new_line': new_line_number,
                    'content': line[1:],
                    'type': 'added'
                })
            elif line.startswith('-'):
                old_line_number += 1
                files_changed[current_file].append({
                    'old_line': old_line_number,
                    'new_line': None,
                    'content': line[1:],
                    'type': 'removed'
                })
            else:
                old_line_number += 1
                new_line_number += 1
                files_changed[current_file].append({
                    'old_line': old_line_number,
                    'new_line': new_line_number,
                    'content': line[1:],
                    'type': 'context'
                })

    return files_changed
