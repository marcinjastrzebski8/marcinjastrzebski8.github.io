#!/usr/bin/env python3
# Script: insert Inter webfont <link> tags into every .html under content/
# Creates a .bak backup of each modified file, and skips files already containing the Inter link.

import os, glob, re, sys

CONTENT_DIR = "/Users/ms1mj/Desktop/PROJECTS/website/marcinjastrzebski8.github.io/content"
FONT_SNIPPET = (
  '  <link rel="preconnect" href="https://fonts.googleapis.com">\n'
  '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
  '  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">\n'
)

html_files = glob.glob(os.path.join(CONTENT_DIR, "**", "*.html"), recursive=True)
if not html_files:
    print("No HTML files found in", CONTENT_DIR)
    sys.exit(1)

for fp in sorted(html_files):
    with open(fp, "r", encoding="utf-8") as f:
        text = f.read()

    if "fonts.googleapis.com/css2?family=Inter" in text:
        print("skip (already present):", fp)
        continue

    m = re.search(r"<head\b[^>]*>", text, flags=re.IGNORECASE)
    if not m:
        print("no <head> tag found, skipping:", fp)
        continue

    insert_pos = m.end()
    new_text = text[:insert_pos] + "\n" + FONT_SNIPPET + text[insert_pos:]

    # backup and write
    bak_fp = fp + ".bak"
    with open(bak_fp, "w", encoding="utf-8") as b:
        b.write(text)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(new_text)
    print("updated:", fp, " (backup:", os.path.basename(bak_fp) + ")")