"""Render an Instagram post described by post.yaml into PNG slides.

    python render.py posts/2026-10/13-alghashqy-abzac/post.yaml [--sheet]

Writes 01.png, 02.png … and caption.txt next to post.yaml; --sheet also
writes _sheet.png, all slides side by side, for a quick look. Exits with
status 1 when text runs past a slide's safe area, naming the slide.

Chromium: Playwright's own, or the executable in $CHROMIUM.
"""

import argparse
import os
import re
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright

SKILL = Path(__file__).resolve().parents[1]

RUBRICS = {
    "avtorlar-mektebi": "Авторлар мектебі",
    "uzindi": "Үзінді",
    "aptanyn-kitaby": "Аптаның кітабы",
    "avtor": "Автор",
    "dayeksoz": "Дәйексөз",
    "zhanalyq": "Жаңалық",
    "baiqau": "Байқау",
    "sen-ne-deisin": "Сен не дейсің?",
    "biz-turaly": "Біз туралы",
}

LAYOUTS = {
    "cover", "step", "text", "cta", "excerpt_cover", "excerpt_page", "continue",
    "book", "author_cover", "quote", "feature", "contest",
    "story_question", "story_post", "reels_cover",
}
IMAGE_FIELDS = ("cover", "photo", "screenshot", "image")


def load(path: Path) -> dict:
    post = yaml.safe_load(path.read_text(encoding="utf-8"))
    if post.get("rubric") not in RUBRICS:
        sys.exit(f"rubric must be one of: {', '.join(RUBRICS)}")
    slides = post.get("slides") or []
    if not slides:
        sys.exit("post has no slides")
    for i, s in enumerate(slides, 1):
        if s.get("layout") not in LAYOUTS:
            sys.exit(f"slide {i}: unknown layout {s.get('layout')!r}")
        for key in IMAGE_FIELDS:
            if s.get(key):
                img = (path.parent / s[key]).resolve()
                if not img.exists():
                    sys.exit(f"slide {i}: image not found: {s[key]}")
                s[key] = img.as_uri()
    return post


def page(post: dict) -> str:
    env = Environment(loader=FileSystemLoader(SKILL / "templates"), autoescape=True)
    brand = SKILL / "brand"
    mark = (brand / "logo-mark-teal.svg").read_text()
    mark = mark.replace('fill="#036672"', 'fill="currentColor"')
    icons = (brand / "icons.svg").read_text()

    def icon(name: str) -> str:
        m = re.search(rf'<symbol id="{name}"([^>]*)>(.*?)</symbol>', icons, re.S)
        return f'<svg xmlns="http://www.w3.org/2000/svg"{m.group(1)}>{m.group(2)}</svg>'

    total = len(post["slides"])
    slides = [{"layout": s["layout"], "data": s, "n": n, "total": total, "file": f"{n:02d}"}
              for n, s in enumerate(post["slides"], 1)]
    return env.get_template("slides.html.j2").render(
        slides=slides, label=RUBRICS[post["rubric"]], mark=mark, icon=icon,
        fonts=(SKILL / "fonts").as_uri())


# Text must end above the frame's bottom minus data-bottom, and no line may
# be wider than its block.
CHECK = """
(frame) => {
  const top = frame.getBoundingClientRect().top;
  const limit = top + frame.offsetHeight - Number(frame.dataset.bottom);
  const bad = [];
  for (const el of frame.querySelectorAll('.flow')) {
    const r = el.getBoundingClientRect();
    if (r.bottom > limit + 1) bad.push(`text ends ${Math.round(r.bottom - limit)}px too low`);
    if (el.scrollWidth > el.clientWidth + 1) bad.push('a word is wider than the line');
  }
  return bad;
}
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("post", type=Path)
    ap.add_argument("--sheet", action="store_true", help="also write _sheet.png")
    args = ap.parse_args()
    post_path = args.post.resolve()
    out = post_path.parent
    post = load(post_path)

    for old in out.glob("[0-9][0-9].png"):
        old.unlink()
    html = out / "_render.html"
    html.write_text(page(post), encoding="utf-8")
    problems = []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=os.environ.get("CHROMIUM") or None)
        tab = browser.new_page(viewport={"width": 1080, "height": 1920})
        tab.goto(html.as_uri())
        tab.evaluate("document.fonts.ready")
        frames = tab.query_selector_all(".f")
        for frame in frames:
            name = frame.get_attribute("data-name")
            frame.screenshot(path=out / f"{name}.png")
            problems += [f"slide {name}: {msg}" for msg in frame.evaluate(CHECK)]
        if args.sheet:
            # A quarter-size row of all slides.
            tab.add_style_tag(content="body{zoom:.25;display:flex;gap:40px;align-items:flex-start;"
                                      "width:max-content;padding:40px;margin:0}.f{margin:0}")
            tab.set_viewport_size({"width": 400, "height": 400})
            tab.locator("body").screenshot(path=out / "_sheet.png")
        browser.close()
    html.unlink()

    caption = (post.get("caption") or "").strip()
    tags = " ".join(post.get("hashtags") or [])
    text = f"{caption}\n\n{tags}" if tags else caption
    (out / "caption.txt").write_text(text + "\n", encoding="utf-8")
    print(f"{len(post['slides'])} slides → {out}")
    if problems:
        print("\n".join(problems), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
