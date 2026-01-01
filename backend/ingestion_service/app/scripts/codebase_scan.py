# app/scripts/codebase_scan.py

import os
import ast
from pathlib import Path

# ---------------------------------------------
# Anchor project root safely
# ---------------------------------------------
SCRIPT_DIR = Path(__file__).resolve()
APP_DIR = SCRIPT_DIR.parents[1]          # app/
PROJECT_ROOT = APP_DIR                   # scan app/ only (safe)


def analyze_python_file(file_path: Path):
    try:
        source = file_path.read_text(encoding="utf-8", errors="ignore")
        tree = ast.parse(source)
    except Exception as e:
        return {
            "file": str(file_path),
            "error": str(e)
        }

    imports, functions, classes = [], [], []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.append(n.name)

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for n in node.names:
                imports.append(f"{module}.{n.name}")

        elif isinstance(node, ast.FunctionDef):
            functions.append(node.name)

        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)

    return {
        "file": str(file_path.relative_to(PROJECT_ROOT)),
        "lines": source.count("\n") + 1,
        "imports": sorted(set(imports)),
        "functions": sorted(functions),
        "classes": sorted(classes),
    }


def scan_codebase():
    results = []

    for root, _, files in os.walk(PROJECT_ROOT):
        for file in files:
            if file.endswith(".py"):
                path = Path(root) / file
                results.append(analyze_python_file(path))

    return sorted(results, key=lambda x: x.get("file", ""))


def main():
    report = scan_codebase()
    output_file = APP_DIR / "CODEBASE_SNAPSHOT.txt"

    with output_file.open("w", encoding="utf-8") as f:
        for entry in report:
            f.write("=" * 80 + "\n")
            f.write(f"FILE: {entry.get('file')}\n")

            if "error" in entry:
                f.write(f"ERROR: {entry['error']}\n")
                continue

            f.write(f"LINES: {entry['lines']}\n\n")

            if entry["imports"]:
                f.write("IMPORTS:\n")
                for i in entry["imports"]:
                    f.write(f"  - {i}\n")
                f.write("\n")

            if entry["classes"]:
                f.write("CLASSES:\n")
                for c in entry["classes"]:
                    f.write(f"  - {c}\n")
                f.write("\n")

            if entry["functions"]:
                f.write("FUNCTIONS:\n")
                for fn in entry["functions"]:
                    f.write(f"  - {fn}\n")
                f.write("\n")

    print(f"\n✅ Codebase snapshot written to:\n{output_file}\n")


if __name__ == "__main__":
    main()
