#!/usr/bin/env python3
"""Validate complete question-specific explanations and export the editorial index.

Run from any directory: python tools/audit_question_explanations.py
The CSV is an editorial queue, not an assessment of historical correctness.
"""
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def read_assignment(path, marker):
    text = path.read_text(encoding="utf-8").split(marker, 1)[1].lstrip()
    return json.JSONDecoder(object_pairs_hook=unique_object).raw_decode(text)[0]


def main():
    questions = read_assignment(ROOT / "site/index.html", "const QS=")
    explanations = read_assignment(
        ROOT / "site/question-explanations.js", "window.QUESTION_EXPLANATIONS ="
    )
    by_key = {f"{q['r']}-{q['n']}": q for q in questions}
    if len(by_key) != len(questions):
        raise ValueError("Duplicate question IDs")
    expected = {f"{r}-{n}" for r in range(70, 80) for n in range(1, 51)}
    if set(by_key) != expected:
        raise ValueError("Original question set must contain all 500 questions (70–79)")
    if set(explanations) != expected:
        missing = sorted(expected - set(explanations))
        extra = sorted(set(explanations) - expected)
        raise ValueError(f"Incomplete coverage: missing={missing}, unknown={extra}")
    for key, entry in explanations.items():
        if key not in by_key:
            raise ValueError(f"{key}: no matching question")
        question = by_key[key]
        if entry["answer"] != question["a"]:
            raise ValueError(f"{key}: answer disagrees with original question")
        clues, choices = entry["clues"], entry["choices"]
        if not isinstance(clues, list) or not clues:
            raise ValueError(f"{key}: missing clues")
        if not isinstance(choices, list) or len(choices) != len(question["ch"]):
            raise ValueError(f"{key}: must explain every choice")
        for value in [*clues, entry["reason"], *choices, entry["takeaway"]]:
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{key}: empty explanation")

    output = ROOT / "docs/question-explanation-audit.csv"
    with output.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["문항", "시대", "주제", "문항별 보완", "기존 해설 글자 수", "검토 참고"])
        for question in sorted(questions, key=lambda q: (-q["r"], q["n"])):
            key = f"{question['r']}-{question['n']}"
            hints = []
            if question.get("img"):
                hints.append("사진 보기 대조")
            if any(word in question["q"] for word in ["사이", "이후", "이전", "순서"]):
                hints.append("시간 조건 대조")
            writer.writerow([key, question["era"], question["topic"],
                             "보완" if key in explanations else "미보완",
                             len(question["exp"]), " / ".join(hints)])
    counts = Counter(int(key.split("-")[0]) for key in explanations)
    print(f"Validated {len(explanations)}/{len(questions)} question explanations.")
    for round_number in sorted({q["r"] for q in questions}, reverse=True):
        total = sum(q["r"] == round_number for q in questions)
        print(f"Round {round_number}: {counts[round_number]}/{total}")
    print(f"Editorial queue: {output}")


if __name__ == "__main__":
    main()
