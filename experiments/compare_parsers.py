import csv
import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from experiments.baselines.command_parser_v1 import parse_command as parse_v1
from speech.command_parser import parse_command as parse_v2
from speech.error_correction import correct_text


INPUT_PATH = "results/model_experiment_prompt.csv"
LABEL_PATH = "dataset/command_labels.csv"
OUTPUT_PATH = "results/parser_experiment.csv"

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


def normalize(text):
    return re.sub(r"[\s.,!?]", "", text).lower()


def evaluate(rows, labels, parser, correction):
    type_correct = 0
    full_correct = 0
    false_execution = 0
    unknown_count = 0

    for row in rows:
        expected = labels[row["filename"]]
        text = row["prediction"]

        if correction:
            text = correct_text(
                text, VOCABULARY,
                threshold=0.9,
                use_jamo=True
            )

        actual = parser(text)

        type_match = expected["type"] == actual["type"]

        slot_match = all(
            normalize(expected[key])
            == normalize(actual.get(key, ""))
            for key in SLOTS[expected["type"]]
        )

        if type_match:
            type_correct += 1

        if type_match and slot_match:
            full_correct += 1
        else:
            print(f"\n[실패] {row['filename']}")
            print("인식:", row["prediction"])
            print("입력:", text)
            print("정답:", expected)
            print("결과:", actual)

        if expected["type"] == "unknown":
            unknown_count += 1

            if actual["type"] != "unknown":
                false_execution += 1

    total = len(rows)

    return {
        "total": total,
        "type_correct": type_correct,
        "type_accuracy": round(type_correct / total * 100, 2),
        "full_correct": full_correct,
        "full_accuracy": round(full_correct / total * 100, 2),
        "false_execution": false_execution,
        "unknown_count": unknown_count
    }


def main():
    with open(LABEL_PATH, encoding="utf-8-sig") as file:
        labels = {
            row["filename"]: row
            for row in csv.DictReader(file)
        }

    with open(INPUT_PATH, encoding="utf-8-sig") as file:
        dataset = list(csv.DictReader(file))

    parsers = {
        "V1": parse_v1,
        "V2": parse_v2
    }

    results = []

    for model in ["base", "small"]:
        rows = [
            row for row in dataset
            if row["model"] == model
        ]

        for version, parser in parsers.items():
            for correction in [False, True]:

                method = "jamo_0.9" if correction else "none"

                print("\n" + "=" * 50)
                print(model, version, method)
                print("=" * 50)

                metrics = evaluate(
                    rows, labels, parser, correction
                )

                result = {
                    "model": model,
                    "parser": version,
                    "correction": method,
                    **metrics
                }

                results.append(result)

    with open(
        OUTPUT_PATH, "w",
        newline="", encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=results[0].keys()
        )
        writer.writeheader()
        writer.writerows(results)

    print("\n=== 전체 실험 결과 ===\n")

    for row in results:
        print(
            f"{row['model']:5} | "
            f"{row['parser']} | "
            f"{row['correction']:8} | "
            f"유형: {row['type_accuracy']:6.2f}% | "
            f"전체: {row['full_accuracy']:6.2f}% | "
            f"잘못된 실행 판단: "
            f"{row['false_execution']}/{row['unknown_count']}"
        )

    print("\n저장 완료:", OUTPUT_PATH)


if __name__ == "__main__":
    main()