"""問題集のページを検索の対象から外す。問題文は学習ページの一覧から検索できる。"""


def on_page_markdown(markdown, page, config, files):
    if "/exercises/" in page.file.src_uri and not page.file.src_uri.endswith("index.md"):
        page.meta.setdefault("search", {})["exclude"] = True
    return markdown
