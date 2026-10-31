"""サービス解説の試験バッジと、コースごとのサービス一覧を生成する。

data/exam_services.json: 試験ごとの公式の対象サービス
data/service_pages.json: サービス名から解説の場所（page または page#anchor）への対応

--check を付けると書き込まず、最新でないファイルや不正な対応があれば失敗する。
"""
import collections
import glob
import json
import os
import re
import sys

SERVICES = "docs/services"
COURSES = "docs/courses"
LINK_THRESHOLD = 3
NOTE = "このページは `scripts/build_exam_badges.py` で生成しています。"
EXAMS = {
    "clf": ("CLF", "foundational"),
    "aif": ("AIF", "foundational"),
    "aib": ("AIB", "foundational"),
    "saa": ("SAA", "associate"),
    "dva": ("DVA", "associate"),
    "soa": ("SOA", "associate"),
    "dea": ("DEA", "associate"),
    "mla": ("MLA", "associate"),
    "sap": ("SAP", "professional"),
    "dop": ("DOP", "professional"),
    "aip": ("AIP", "professional"),
    "ans": ("ANS", "specialty"),
    "scs": ("SCS", "specialty"),
}
ICONS = {
    "foundational": "material-sprout",
    "associate": "material-certificate",
    "professional": "material-star-circle",
    "specialty": "material-target",
}
BADGE_LINE = re.compile(r"^.*\{ \.exam-badge[^\n]*\n\n", re.M)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def badge(code, prefix, official=True):
    label, level = EXAMS[code]
    style = "" if official else " .exam-badge--related"
    icon = f":{ICONS[level]}:"
    target = f"{prefix}courses/{code}/services.md"
    return f"[{icon} {label}]({target}){{ .exam-badge .exam-{level}{style} }}"


def badges(codes, prefix, official=True):
    ordered = [code for code in EXAMS if code in codes]
    return " ".join(badge(code, prefix, official) for code in ordered)


def display_name(name):
    name = re.sub(r"\s*\((?:for example|previously|including|with|for all)[^)]*\)", "", name)
    return re.sub(r"\s+\(.*\)$", "", name)


def load_links():
    links = collections.defaultdict(collections.Counter)
    for code in EXAMS:
        for path in glob.glob(f"{COURSES}/{code}/domain*.md"):
            for page in re.findall(r"services/([a-z0-9-]+)\.md", read(path)):
                links[page][code] += 1
    return links


def categories():
    groups = []
    for part in re.split(r"^## ", read(f"{SERVICES}/index.md"), flags=re.M)[1:]:
        title = re.sub(r"\s*\{#.*", "", part.split("\n")[0])
        pages = re.findall(r"^\| \[([^\]]+)\]\(([a-z0-9-]+)\.md\)", part, re.M)
        if pages:
            groups.append((title, pages))
    return groups


def render_service_page(path, page, official, related, by_anchor):
    text = BADGE_LINE.sub("", read(path))
    lines = text.split("\n")
    out = []
    for i, line in enumerate(lines):
        out.append(line)
        if i == 0 and line.startswith("# "):
            parts = []
            if official:
                parts.append(badges(official, "../"))
            if related:
                parts.append(badges(related, "../", official=False))
            if parts:
                out += ["", " ".join(parts)]
            continue
        match = re.match(r"^#{2,3} .+\{#([\w-]+)\}$", line)
        if match and by_anchor.get((page, match.group(1))):
            out += ["", badges(by_anchor[(page, match.group(1))], "../")]
    return "\n".join(out)


def render_course_page(code, homes, exam_names, links, titles, groups):
    label = EXAMS[code][0]
    rows_by_page = collections.defaultdict(dict)
    missing = []
    for name in exam_names[code]:
        targets = homes.get(name)
        if not targets:
            missing.append(display_name(name))
            continue
        for target in targets:
            page, _, anchor = target.partition("#")
            link = f"../../services/{page}.md" + (f"#{anchor}" if anchor else "")
            rows_by_page[page].setdefault(link, display_name(name))
    lines = [
        f"# {label} のサービス一覧",
        "",
        "この試験の公式の対象サービスと、wiki の解説ページの対応です。サービス名を選ぶと、該当する解説に移動します。",
        "",
        f"[コースの概要に戻る](index.md)",
        "",
    ]
    for title, pages in groups:
        rows = []
        for name, page in pages:
            if page in rows_by_page:
                items = sorted(rows_by_page[page].items(), key=lambda item: item[1].lower())
                cells = "、".join(f"[{text}]({link})" for link, text in items)
                rows.append(f"| [{name}](../../services/{page}.md) | {cells} |")
        if rows:
            slug = re.sub(r"[^a-z0-9]+", "-", pages[0][1])
            lines += [f"## {title} {{#group-{slug}}}", "", "| 解説ページ | この試験の対象サービス |", "|---|---|", *rows, ""]
    extra = [
        page
        for page, count in links.items()
        if count[code] >= LINK_THRESHOLD and page not in rows_by_page and page in titles
    ]
    if extra:
        lines += ["## 解説で参照しているページ {#related}", "", "公式の対象サービスの一覧には載っていませんが、このコースの解説で参照しているページです。", ""]
        lines += [f"- [{titles[page]}](../../services/{page}.md)" for page in sorted(extra)]
        lines.append("")
    if missing:
        lines += ["## 専用の解説がないサービス {#not-covered}", "", "公式の対象ですが、サービス解説に専用の説明がありません。コースの分野ページで必要な範囲を説明しています。", ""]
        lines += [f"- {name}" for name in sorted(set(missing))]
        lines.append("")
    return "\n".join(lines)


def render_service_index(official, related):
    def row(match):
        name, page, services = match.group(1), match.group(2), match.group(3)
        parts = []
        if official[page]:
            parts.append(badges(official[page], "../"))
        if related.get(page):
            parts.append(badges(related[page], "../", official=False))
        return f"| [{name}]({page}.md) | {services} | {' '.join(parts)} |"

    text = read(f"{SERVICES}/index.md")
    text = re.sub(r"^\| ページ \| 扱うサービス \|(?: 試験 \|)?\n\|---\|---\|(?:---\|)?$", "| ページ | 扱うサービス | 試験 |\n|---|---|---|", text, flags=re.M)
    return re.sub(r"^\| \[([^\]]+)\]\(([a-z0-9-]+)\.md\) \| (.+?) \|(?: .*\|)?$", row, text, flags=re.M)


def main():
    check = "--check" in sys.argv
    exam_names = json.loads(read("data/exam_services.json"))
    homes = json.loads(read("data/service_pages.json"))
    pages = {
        os.path.basename(p)[:-3]: p
        for p in glob.glob(f"{SERVICES}/*.md")
        if not p.endswith("index.md")
    }
    errors = []
    names = {name for values in exam_names.values() for name in values}
    for name in sorted(names - homes.keys()):
        errors.append(f"対応表にないサービス: {name}")
    for name, targets in homes.items():
        for target in targets:
            page, _, anchor = target.partition("#")
            if page not in pages:
                errors.append(f"存在しないページ: {name} -> {target}")
            elif anchor and f"{{#{anchor}}}" not in read(pages[page]):
                errors.append(f"存在しない見出し: {name} -> {target}")
    official = collections.defaultdict(set)
    by_anchor = collections.defaultdict(set)
    for code, values in exam_names.items():
        for name in values:
            for target in homes.get(name, []):
                page, _, anchor = target.partition("#")
                official[page].add(code)
                if anchor:
                    by_anchor[(page, anchor)].add(code)
    links = load_links()
    outputs = {}
    titles = {}
    related = {}
    for page, path in pages.items():
        titles[page] = read(path).split("\n")[0].lstrip("# ").strip()
        related[page] = {c for c, n in links[page].items() if n >= LINK_THRESHOLD} - official[page]
        outputs[path] = render_service_page(path, page, official[page], related[page], by_anchor)
    outputs[f"{SERVICES}/index.md"] = render_service_index(official, related)
    groups = categories()
    for code in EXAMS:
        outputs[f"{COURSES}/{code}/services.md"] = render_course_page(
            code, homes, exam_names, links, titles, groups
        )
    stale = []
    for path, content in outputs.items():
        current = read(path) if os.path.exists(path) else None
        if current != content:
            stale.append(path)
            if not check:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
    print(f"サービス {len(names)}個, 更新対象 {len(stale)}ファイル")
    for error in errors:
        print("ERROR", error)
    if check:
        for path in stale:
            print("ERROR 生成結果が古いファイル", path)
    sys.exit(1 if errors or (check and stale) else 0)


if __name__ == "__main__":
    main()
