# pr_agent/static_checks.py
from radon.complexity import cc_visit

def run_checks(files_changed: dict) -> list:
    """Run static analysis on changed files."""
    findings = []

    for file_path, lines in files_changed.items():
        if not file_path.endswith(".py"):
            continue

        file_content = "".join([line['content'] + "\n" for line in lines if line['type'] in ('added', 'context')])
        if not file_content.strip():
            continue

        try:
            blocks = cc_visit(file_content)
            for block in blocks:
                if block.complexity > 10:
                    findings.append({
                        "file": file_path,
                        "line": block.lineno,
                        "message": f"High cyclomatic complexity ({block.complexity}) in `{block.name}`",
                        "severity": "warning"
                    })
        except Exception as e:
            print(f"Error checking {file_path}: {e}")

    return findings
