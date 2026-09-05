#!/usr/bin/env python3
"""アニメHTMLのサムネイル(thumbs/<dir>/<name>.webp)を一括生成する。

使い方:
    python3 tools/gen_thumbs.py            # 無いものだけ生成
    python3 tools/gen_thumbs.py --force    # 全部作り直す

依存: google-chrome(ヘッドレス起動できること) / Pillow(webp対応)。
新しいアニメを追加したら本スクリプトを再実行し、index.html にカードを足すこと。
"""

import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DIRS = ["handotai", "kairo"]
THUMB_W, THUMB_H = 480, 360
SHOT_W, SHOT_H = 1200, 900


def make_thumb(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        png = Path(td) / "shot.png"
        subprocess.run(
            [
                "google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox",
                "--hide-scrollbars", "--window-size=%d,%d" % (SHOT_W, SHOT_H),
                "--virtual-time-budget=4000",
                "--screenshot=%s" % png, "file://%s" % src,
            ],
            check=True, capture_output=True, timeout=90,
        )
        img = Image.open(png).convert("RGB")
        img = img.resize((THUMB_W, THUMB_H), Image.LANCZOS)
        img.save(dst, "WEBP", quality=82)


def main() -> None:
    force = "--force" in sys.argv
    made = skipped = failed = 0
    for d in DIRS:
        for src in sorted((ROOT / d).glob("*.html")):
            dst = ROOT / "thumbs" / d / (src.stem + ".webp")
            if dst.exists() and not force:
                skipped += 1
                continue
            try:
                make_thumb(src, dst)
                made += 1
                print("ok  %s" % dst.relative_to(ROOT))
            except Exception as e:  # noqa: BLE001
                failed += 1
                print("NG  %s: %s" % (src.name, e))
    print("done: %d生成 / %dスキップ / %d失敗" % (made, skipped, failed))
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
