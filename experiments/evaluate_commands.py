import csv
import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from speech.command_parser import parse_command
from speech.error_correction import correct_text


LABEL_PATH = "dataset/command_labels.csv"
INPUT_PATH = "results/model_experiment_prompt.csv"

VOCABULARY = [
    "계산기", "크롬", "메모장",
    "파일 탐색기", "바탕화면",
    "다운로드", "문서",
    "파이썬", "인공지능"
]

SLOTS = {
    "open_app": ["target"],
    "web_search": ["query"],
    "open_file": ["name", "folder"],
    "unknown": []
}

CONDITIONS = [
    ("none", 0.0),
    ("char", 0.6),
    ("char", 0.8),
    ("char", 0.9),
    ("jamo", 0.6),
    ("jamo", 0.8),
    ("jamo", 0.9)
]


# 1. 비교용 문자열 정규화
def normalize(text):
    return re.sub(r"[\s.,!?]", "", text).lower()


# 2. 명령어 분석 성능 평가
def evaluate(rows, labels, method="none", threshold=0.9):
    type_correct = 0
    full_correct = 0
    false_execution = 0
    unknown_count = 0

    for row in rows:
        expected = labels[row["filename"]]
        text = row["prediction"]

        # 오류 보정
        if method != "none":
            text = correct_text(
                text,
                VOCABULARY,
                threshold,
                use_jamo=(method == "jamo")
            )

        # 명령어 분석
        actual = parse_command(text)

        # 명령 유형 비교
        type_match = expected["type"] == actual["type"]

        # 실행 대상 및 세부 정보 비교
        slot_match = all(
            normalize(expected[key]) ==
            normalize(actual.get(key, ""))
            for key in SLOTS[expected["type"]]
        )

        if type_match:
            type_correct += 1

        if type_match and slot_match:
            full_correct += 1
        else:
            print(f"\n[실패] {row['filename']}")
            print("인식:", row["prediction"])
            print("보정 후:", text)
            print("정답:", expected)
            print("분석:", actual)

        # 실행하면 안 되는 명령 평가
        if expected["type"] == "unknown":
            unknown_count += 1

            if actual["type"] != "unknown":
                false_execution += 1

    total = len(rows)

    print("\n--- 평가 결과 ---")
    print(f"명령 유형 정확도: {type_correct}/{total}")
    print(f"유형 정확도: {type_correct / total * 100:.2f}%")
    print(f"전체 명령 일치: {full_correct}/{total}")
    print(f"전체 명령 정확도: {full_correct / total * 100:.2f}%")
    print(f"잘못된 실행 판단: {false_execution}/{unknown_count}")


# 3. 모델 및 보정 방식별 비교 실험
def main():
    with open(LABEL_PATH, encoding="utf-8-sig") as file:
        labels = {
            row["filename"]: row
            for row in csv.DictReader(file)
        }

    with open(INPUT_PATH, encoding="utf-8-sig") as file:
        dataset = list(csv.DictReader(file))

    for model in ["base", "small"]:
        print(f"\n=== {model} 모델 ===")

        rows = [
            row for row in dataset
            if row["model"] == model
        ]

        for method, threshold in CONDITIONS:
            print(f"\n--- {method} / {threshold} ---")

            evaluate(
                rows,
                labels,
                method,
                threshold
            )


if __name__ == "__main__":
    main()