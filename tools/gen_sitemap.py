#!/usr/bin/env python3
"""sitemap.xml を生成する。アニメを追加・更新したら再実行して push すること。"""

from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://ugoku-zukai4kosen.com"


def main() -> None:
    urls = ["%s/" % BASE, "%s/about.html" % BASE, "%s/privacy.html" % BASE]
    for d in ("handotai", "kairo"):
        for f in sorted((ROOT / d).glob("*.html")):
            urls.append("%s/%s/%s" % (BASE, d, f.name))

    today = date.today().isoformat()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        lines.append("  <url><loc>%s</loc><lastmod>%s</lastmod></url>" % (u, today))
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("sitemap.xml: %d URLs" % len(urls))


if __name__ == "__main__":
    main()
