"""問題集の形式を検査し、正解の偏りを表示する。"""
import collections
import glob
import os
import re
import sys

QUESTION = re.compile(r"^### 問(\d+) \{#q(\d+)\}$", re.M)
OPTION = re.compile(r"^- ([A-Z])\. (.+)$", re.M)
ANSWER = re.compile(r"^    \*\*正解: ([A-Z](?:, [A-Z])*)\*\*$", re.M)
SELECT = re.compile(r"（(\d)つ選択）")
MIN_PER_SKILL = 3


def check(path, errors, letters):
    text = open(path, encoding="utf-8").read()
    marks = list(QUESTION.finditer(text))
    if not marks:
        errors.append(f"{path}: 問題がありません")
    longest = total = 0
    for i, mark in enumerate(marks):
        where = f"{path} 問{mark.group(1)}"
        if int(mark.group(1)) != i + 1 or mark.group(1) != mark.group(2):
            errors.append(f"{where}: 番号が連番ではありません")
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        body = text[mark.end():end]
        head, sep, answer_part = body.partition('??? success "答えと解説"')
        if not sep:
            errors.append(f"{where}: 答えの折りたたみがありません")
            continue
        options = OPTION.findall(head)
        names = [name for name, _ in options]
        answer = ANSWER.search(answer_part)
        if not answer:
            errors.append(f"{where}: 正解の行がありません")
            continue
        correct = answer.group(1).split(", ")
        select = SELECT.search(head)
        expected = int(select.group(1)) if select else 1
        if len(correct) != expected:
            errors.append(f"{where}: 正解の数が問題文と合いません")
        if names != [chr(65 + n) for n in range(len(names))]:
            errors.append(f"{where}: 選択肢が A から順に並んでいません")
        if len(names) != (5 if select and expected == 2 else 6 if select else 4):
            errors.append(f"{where}: 選択肢の数が不正です（{len(names)}個）")
        for name in correct:
            if name not in names:
                errors.append(f"{where}: 正解 {name} が選択肢にありません")
        for name in names:
            if not re.search(rf"^    - {name}: ", answer_part, re.M):
                errors.append(f"{where}: 選択肢 {name} の解説がありません")
        if "**スキル:**" not in answer_part or "services/" not in answer_part:
            errors.append(f"{where}: スキルか参照先がありません")
        letters.update(correct)
        if not select:
            total += 1
            length = {name: len(option) for name, option in options}
            if length.get(correct[0], 0) == max(length.values()):
                longest += 1
    return len(marks), longest, total


def check_skills(paths, errors):
    """対応表にある C03 の全スキルに、最低限の問題数があるか確かめる。"""
    tags = collections.Counter()
    for path in paths:
        for line in re.findall(r"\*\*スキル:\*\*(.*)", open(path, encoding="utf-8").read()):
            tags.update(re.findall(r"C03 (\d\.\d\.\d+)", line.split("**参照")[0]))
    table = open("docs/courses/dva/coverage.md", encoding="utf-8").read().split("## DVA-C02")[0]
    for skill in re.findall(r"\[(\d\.\d\.\d+)\]\(domain", table):
        if tags[skill] < MIN_PER_SKILL:
            errors.append(f"スキル {skill}: 問題が {tags[skill]}問しかありません")


def main():
    errors = []
    letters = collections.Counter()
    pattern = "docs/courses/*/exercises/*.md"
    paths = [p for p in sorted(glob.glob(pattern)) if os.path.basename(p) != "index.md"]
    count = 0
    for path in paths:
        questions, longest, total = check(path, errors, letters)
        count += questions
        print(f"{path}: {questions}問, 正解が最長の選択肢: {longest}/{total}")
    print(f"合計 {count}問, 正解の分布: {dict(sorted(letters.items()))}")
    check_skills(paths, errors)
    for error in errors:
        print("ERROR", error)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
