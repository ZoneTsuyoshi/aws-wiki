"""各ページで略語が最初に出たところに、正式名称を（）で付ける。対応表は data/abbreviations.json。

見出し、コード、リンク先、試験バッジの行は書き換えない。
「Velocity Template Language（VTL）」のように正式名称がすでに書いてあれば、付け足さない。
「OU（組織単位）」のように別の説明が括弧にあれば、その括弧の中に正式名称を足す。
"""

import json
import re
from pathlib import Path

DATA = json.loads(
    (Path(__file__).resolve().parent.parent / "data" / "abbreviations.json").read_text(encoding="utf-8")
)
GLOSSARY = DATA["terms"]

WORD = re.compile(
    r"(?<![A-Za-z0-9_\-/.:@$#])("
    + "|".join(re.escape(k) for k in sorted(GLOSSARY, key=len, reverse=True))
    + r")(?![A-Za-z0-9_\-/…])([（(])?"
)

# 書き換えない部分: インラインコード、画像、リンク先、HTML タグ、属性、URL、アイコン、
# 略語を含む製品名（"keep"）
PROTECTED = re.compile(
    r"`[^`]*`|!\[[^\]]*\]\([^)]*\)|\]\([^)]*\)|\]\[[^\]]*\]|<[^>]+>|\{[^}]*\}|https?://\S+|:[a-z0-9-]+:|"
    + "|".join(re.escape(k) for k in DATA["keep"])
)
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
SKIP_LINE = re.compile(r"^\s*(#|<|\*\[|\[[^\]]+\]:\s)")

OPEN = "（("
CLOSE = "）)"


def _full_name(abbr, markdown):
    entry = GLOSSARY[abbr]
    if isinstance(entry, str):
        return entry
    for sense in entry:
        if any(word in markdown for word in sense.get("when", [])) or "when" not in sense:
            return sense["full"]
    return entry[-1]["full"]


def _mentions(text, full):
    name = re.sub(r"^(AWS|Amazon) ", "", full).lower()
    return name in text.lower()


def _expand_text(text, markdown, done):
    def replace(m):
        abbr, paren = m.group(1), m.group(2)
        if abbr in done:
            return m.group(0)
        done.add(abbr)
        full = _full_name(abbr, markdown)
        if paren:
            # 「HTTPS（443 番）」は「HTTPS（Hypertext Transfer Protocol Secure、443 番）」にする
            inner = re.match(r"[^）)]*", text[m.end():]).group(0)
            return m.group(0) if _mentions(inner, full) else f"{abbr}{paren}{full}、"
        before = text[m.start() - 1] if m.start() > 0 else ""
        after = text[m.end()] if m.end() < len(text) else ""
        if before in OPEN and after in CLOSE:
            # 「インスタンスメタデータサービス（IMDS）」は「（IMDS、Instance Metadata Service）」にする
            return abbr if _mentions(text[max(0, m.start() - 80):m.start()], full) else f"{abbr}、{full}"
        return f"{abbr}（{full}）"

    return WORD.sub(replace, text)


def _expand_line(line, markdown, done):
    out = []
    pos = 0
    for m in PROTECTED.finditer(line):
        out.append(_expand_text(line[pos:m.start()], markdown, done))
        out.append(m.group(0))
        pos = m.end()
    out.append(_expand_text(line[pos:], markdown, done))
    return "".join(out)


def on_page_markdown(markdown, page, config, files):
    done = set()
    fence = None
    lines = []
    for line in markdown.split("\n"):
        m = FENCE.match(line)
        if fence:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence):
                fence = None
        elif m:
            fence = m.group(1)
        elif not SKIP_LINE.match(line) and ".exam-badge" not in line:
            line = _expand_line(line, markdown, done)
        lines.append(line)
    return "\n".join(lines)
