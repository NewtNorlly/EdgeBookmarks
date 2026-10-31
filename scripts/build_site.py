# -*- coding: utf-8 -*-
"""Generate the static bookmark-manager page from site/data/bookmarks.json."""
import html
import json
import os
from collections import OrderedDict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "site", "data", "bookmarks.json")
OUT = os.path.join(BASE, "site", "index.html")

LEVEL_NAMES = {
    "A": "重要",
    "B": "一般有用",
    "C": "影视资源",
    "S": "绝不能删",
    "D": "敏感内容",
}


def esc(value):
    return html.escape(str(value or ""), quote=False)


def attr(value):
    return html.escape(str(value or ""), quote=True)


def main():
    with open(DATA, "r", encoding="utf-8") as handle:
        data = json.load(handle)

    levels = data.get("levels", [])
    bookmarks = data.get("bookmarks", [])
    public_count = data.get("publicCount", len(bookmarks))

    tree = []
    sections = []
    for level in levels:
        level_id = level["id"]
        level_items = [item for item in bookmarks if item["level"] == level_id]
        categories = OrderedDict()
        for item in level_items:
            categories.setdefault(item["category"], []).append(item)

        cat_links = []
        category_html = []
        for cat_index, (category, items) in enumerate(categories.items(), 1):
            cat_anchor = f"cat-{level_id.lower()}-{cat_index}"
            cat_links.append(
                f'<li><a href="#{cat_anchor}">{esc(category)} <span>{len(items)}</span></a></li>'
            )
            rows = []
            for item_index, item in enumerate(items, 1):
                rows.append(
                    "<li>"
                    f'<a href="{attr(item["url"])}" target="_blank" rel="noopener noreferrer">'
                    f'<span class="num">{item_index:02d}</span>'
                    f'<span class="bm-title">{esc(item["title"])}</span>'
                    f'<span class="bm-domain">{esc(item["domain"])}</span>'
                    "</a>"
                    "</li>"
                )
            category_html.append(
                f'<section class="category" id="{cat_anchor}">'
                '<header class="category-head">'
                f'<h3>{esc(category)}</h3>'
                f'<span>{len(items)} 条</span>'
                "</header>"
                f'<ol class="bookmarks">{"".join(rows)}</ol>'
                "</section>"
            )

        tree.append(
            '<div class="tree-level">'
            f'<a class="tree-row" href="#level-{attr(level_id.lower())}">'
            f'<span class="tree-letter">{esc(level_id)}</span>'
            f'<span class="tree-name">{esc(LEVEL_NAMES.get(level_id, level["title"]))}</span>'
            f'<span class="tree-count">{level["count"]}</span>'
            "</a>"
            f'<ul class="tree-cats">{"".join(cat_links)}</ul>'
            "</div>"
        )

        sections.append(
            f'<section class="level" id="level-{attr(level_id.lower())}">'
            '<header class="level-head">'
            f'<span class="level-letter" aria-hidden="true">{esc(level_id)}</span>'
            '<div class="level-title">'
            f'<h2>{esc(LEVEL_NAMES.get(level_id, level["title"]))}</h2>'
            f'<p>{esc(level["subtitle"])}</p>'
            "</div>"
            f'<span class="level-count">{level["count"]} 条</span>'
            "</header>"
            f'<div class="categories">{"".join(category_html)}</div>'
            "</section>"
        )

    html_doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#ffffff">
  <meta name="robots" content="noindex, nofollow">
  <meta name="description" content="Edge Bookmarks — {public_count} 条公开收藏的网络书签页。">
  <title>网络书签 / Edge Bookmarks</title>
  <link rel="icon" href="./favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="./assets/styles.css">
</head>
<body>
  <header class="topbar">
    <div class="brand">
      <h1>网络书签</h1>
      <p>EDGE BOOKMARKS / 2026</p>
    </div>
    <div class="topbar-meta">
      <p><span class="red">{public_count}</span> 条公开收藏</p>
      <p>最后整理 2026.11</p>
    </div>
  </header>

  <div class="layout">
    <aside class="sidebar">
      <p class="sidebar-label">文件夹 / FOLDERS</p>
      <nav aria-label="书签文件夹">
        {''.join(tree)}
      </nav>
    </aside>

    <main class="content">
      <p class="lede">A/B/C/S/D 五级个人收藏。按主题分组，保留最优来源；重复与失效链接已清理。</p>
      {''.join(sections)}
    </main>
  </div>

  <footer class="footer">
    <div class="footer-line">
      <span>EDGE BOOKMARKS / 2026</span>
      <span>PUBLIC {public_count}</span>
      <span><a href="./bookmarks-import.html" download>IMPORT HTML <span class="red">↗</span></a></span>
    </div>
  </footer>
</body>
</html>
"""
    with open(OUT, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(html_doc)
    print(f"Wrote {OUT} ({public_count} public bookmarks, {len(sections)} levels)")


if __name__ == "__main__":
    main()
