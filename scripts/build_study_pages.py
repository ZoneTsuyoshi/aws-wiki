"""分野別の学習ページに、スキルのタグから問題の一覧を書き込む。

--check を付けると書き込まず、最新でないページや行き先のない問題があれば失敗する。
"""
import glob
import os
import re
import sys

COURSE = "docs/courses/dva"
START = "<!-- questions:start -->"
END = "<!-- questions:end -->"
QUESTION = re.compile(r"^### 問(\d+) \{#q\d+\}\n(.*?)(?=^### 問|\Z)", re.M | re.S)
TAG = re.compile(r"\*\*スキル:\*\*(.*)")
SKILL = re.compile(r"C0[23] ((\d)\.\d\.\d+)")


def load_questions():
    questions = {}
    for path in sorted(glob.glob(f"{COURSE}/exercises/*.md")):
        service = os.path.basename(path)[:-3]
        if service == "index":
            continue
        for number, body in QUESTION.findall(open(path, encoding="utf-8").read()):
            skills = SKILL.findall(TAG.search(body).group(1).split("**参照")[0])
            stem = body.strip().split("\n\n")[0].replace("`", "").replace("|", "/")
            stem = stem[:50] + "…" if len(stem) > 50 else stem
            questions[(service, int(number))] = (skills, stem)
    return questions


def rows(items):
    if not items:
        return "この組み合わせの問題はまだありません。\n"
    lines = ["| 問題 | スキル | 内容 |", "|---|---|---|"]
    for (service, number), skills, stem in items:
        link = f"[{service} 問{number}](../../exercises/{service}.md#q{number})"
        lines.append(f"| {link} | {', '.join(skills)} | {stem} |")
    return "\n".join(lines) + "\n"


def select(questions, domain, services):
    items = []
    for (service, number), (skills, stem) in questions.items():
        matched = [skill for skill, first in skills if first == domain]
        if matched and service in services:
            items.append(((service, number), matched, stem))
    return items


def render(path, content, block):
    if START not in content or END not in content:
        raise SystemExit(f"{path}: 問題一覧の目印がありません")
    head, _, rest = content.partition(START)
    _, _, tail = rest.partition(END)
    return f"{head}{START}\n\n{block}\n{END}{tail}"


def main():
    check = "--check" in sys.argv
    questions = load_questions()
    listed = set()
    stale = []
    for directory in sorted(glob.glob(f"{COURSE}/study/domain*")):
        domain = directory[-1]
        pages = sorted(glob.glob(f"{directory}/*.md"))
        services = {os.path.basename(p)[:-3] for p in pages} - {"index"}
        everything = {service for service, _ in questions}
        for path in pages:
            name = os.path.basename(path)[:-3]
            targets = everything - services if name == "index" else {name}
            items = select(questions, domain, targets)
            listed.update(key for key, _, _ in items)
            content = open(path, encoding="utf-8").read()
            updated = render(path, content, rows(items))
            if updated != content:
                stale.append(path)
                if not check:
                    open(path, "w", encoding="utf-8").write(updated)
    missing = [key for key in questions if key not in listed]
    print(f"問題 {len(questions)}問, 学習ページに載っていない問題 {len(missing)}問")
    for service, number in missing:
        print("ERROR 行き先なし", service, number)
    if check:
        for path in stale:
            print("ERROR 問題一覧が古いページ", path)
    sys.exit(1 if missing or (check and stale) else 0)


if __name__ == "__main__":
    main()
