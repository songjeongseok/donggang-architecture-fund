#!/usr/bin/env python3
"""Validate the pre-opening informational page and stage a public-file allowlist.

Python >= 3.9, standard library only. Never runs a deployment or reads .env.
The intentional no-form/no-script guard must be redesigned before adding intake.
"""

from collections import Counter
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "site"
OUTPUT = ROOT / "dist"
PUBLIC_FILES = ("index.html", ".nojekyll")


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.elements = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_data(self, data):
        self.text.append(data)


def validate_html(source):
    page = Page()
    page.feed(source)
    page.close()
    ids = [attrs["id"] for _, attrs in page.elements if "id" in attrs]
    duplicates = [name for name, count in Counter(ids).items() if count > 1]
    errors = []
    if duplicates:
        errors.append("Duplicate element IDs: " + ", ".join(duplicates))
    if not re.match(r"\s*<!doctype\s+html\s*>", source, re.I):
        errors.append("HTML5 doctype missing")
    if not any(t == "html" and a.get("lang") == "ko" for t, a in page.elements):
        errors.append("Korean document language missing")
    if not any(t == "meta" and a.get("charset", "").lower() == "utf-8" for t, a in page.elements):
        errors.append("UTF-8 declaration missing")
    if not any(t == "meta" and a.get("name") == "viewport" for t, a in page.elements):
        errors.append("Mobile viewport declaration missing")
    if sum(t == "h1" for t, _ in page.elements) != 1:
        errors.append("Exactly one primary heading is required")
    if "현재 기부 신청·입금을 접수하지 않습니다." not in " ".join(page.text):
        errors.append("Pre-opening / no-intake notice missing")
    blocked = {"script", "form", "input", "textarea", "select", "iframe", "object", "embed", "base"}
    anchor_count = 0
    for tag, attrs in page.elements:
        if tag in blocked:
            errors.append("Unsupported intake/active element in pre-opening site: " + tag)
        if any(name.lower().startswith("on") for name in attrs):
            errors.append("Inline JavaScript event handler is not allowed")
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            errors.append("Automatic redirects are not allowed")
        if "src" in attrs or "srcset" in attrs or (tag == "link" and "href" in attrs):
            errors.append("New external/local assets require an explicit public-file review")
        if "href" in attrs:
            href = attrs["href"] or ""
            if tag != "a" or not href.startswith("#"):
                errors.append("Only in-page navigation is enabled in this single-file site")
                continue
            anchor_count += 1
            if unquote(urlsplit(href).fragment) not in ids:
                errors.append("Broken in-page link: " + href)
    if re.search(r"@import\b", source, re.I):
        errors.append("External CSS imports require review")
    for target in re.findall(r"url\s*\(\s*([^)]*)\)", source, re.I):
        target = target.strip().strip("\"'")
        # Inline SVG paint servers (e.g. url(#windows)) remain self-contained.
        if not target.startswith("#") or target[1:] not in ids:
            errors.append("External or unresolved CSS/SVG URL requires review: " + target)
    if re.search(r"claude\.use|localStorage|sessionStorage|\bfetch\s*\(", source):
        errors.append("Unsupported runtime/storage dependency detected")
    # Detect common credential signatures; this is not a complete secret scanner.
    if re.search(r"-----BEGIN [A-Z ]*PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk_live_[A-Za-z0-9]{10,}", source):
        errors.append("Possible credential in public HTML")
    if errors:
        raise ValueError("\n".join(errors))
    return {"in_page_links": anchor_count, "faq_items": sum(t == "details" for t, _ in page.elements), "forms": 0, "scripts": 0}


def build():
    if not SOURCE.is_dir() or SOURCE.is_symlink():
        raise ValueError("Expected a real site directory")
    actual = {p.name for p in SOURCE.iterdir()}
    if actual != set(PUBLIC_FILES):
        raise ValueError("site/ must contain only index.html and .nojekyll; review any additional public files")
    for name in PUBLIC_FILES:
        item = SOURCE / name
        if item.is_symlink() or not item.is_file():
            raise ValueError("Public input must be a regular file: " + name)
    html = (SOURCE / "index.html").read_text(encoding="utf-8")
    result = validate_html(html)
    if OUTPUT.is_symlink() or (OUTPUT.exists() and not OUTPUT.is_dir()):
        raise ValueError("Refusing to replace a non-directory/symlink dist path")
    # Fully validate before replacing previous generated output; no networking.
    with tempfile.TemporaryDirectory(prefix=".pages-build-", dir=ROOT) as staging:
        stage = Path(staging)
        for name in PUBLIC_FILES:
            shutil.copyfile(SOURCE / name, stage / name)
        if OUTPUT.exists():
            shutil.rmtree(OUTPUT)
        stage.rename(OUTPUT)
    files = [{"path": name, "bytes": (OUTPUT / name).stat().st_size,
              "sha256": sha256((OUTPUT / name).read_bytes()).hexdigest()} for name in PUBLIC_FILES]
    report = {"status": "passed", "scope": "local static build only; no deployment", "checks": result,
              "public_files": files, "required_environment_variables": [], "runtime_server": "none"}
    reports = ROOT / ".build"
    reports.mkdir(exist_ok=True)
    (reports / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        build()
    except (ValueError, OSError, UnicodeError) as exc:
        print("Build failed: " + str(exc), file=sys.stderr)
        sys.exit(1)
