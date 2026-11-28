import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from experiments.baselines.command_parser_v1 import parse_command as parse_v1
from speech.command_parser import parse_command as parse_v2


INPUT_PATH = "dataset/parser_validation.csv"
OUTPUT_PATH = "results/parser_validation.csv"

SLOTS = {
    "open_app": ["target"],
    "web_search": ["query"],
    "open_file": ["name", "folder"],
    "unknown": []
}


def evaluate(rows, parser, version):
    type_correct = 0
    full_correct = 0
    false_execution = 0
    unknown_count = 0

    category_results = {
        key: {"correct": 0, "total": 0}
        for key in SLOTS
    }

    print(f"\n=== {version} 검증 결과 ===")

    for row in rows:
        actual = parser(row["text"])
        expected_type = row["type"]

        type_match = actual["type"] == expected_type

        slot_match = all(
            row[key].strip() == actual.get(key, "").strip()
            for key in SLOTS[expected_type]
        )

        full_match = type_match and slot_match

        category_results[expected_type]["total"] += 1

        if type_match:
            type_correct += 1

        if full_match:
            full_correct += 1
            category_results[expected_type]["correct"] += 1
        else:
            print(f"\n[실패] {row['id']}")
            print("입력:", row["text"])
            print("정답:", row)
            print("결과:", actual)

        if expected_type == "unknown":
            unknown_count += 1

            if actual["type"] != "unknown":
                false_execution += 1

    total = len(rows)

    print("\n--- 유형별 전체 명령 일치 ---")

    for category, result in category_results.items():
        print(
            f"{category}: "
            f"{result['correct']}/{result['total']}"
        )

    return {
        "parser": version,
        "total": total,
        "type_correct": type_correct,
        "type_accuracy": round(type_correct / total * 100, 2),
        "full_correct": full_correct,
        "full_accuracy": round(full_correct / total * 100, 2),
        "false_execution": false_execution,
        "unknown_count": unknown_count
    }


def main():
    with open(INPUT_PATH, encoding="utf-8-sig") as file:
        rows = list(csv.DictReader(file))

    if len(rows) != 40:
        raise ValueError("검증 데이터는 40개여야 합니다.")

    results = [
        evaluate(rows, parse_v1, "V1"),
        evaluate(rows, parse_v2, "V2")
    ]

    with open(
        OUTPUT_PATH, "w",
        newline="", encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=results[0].keys()
        )
        writer.writeheader()
        writer.writerows(results)

    print("\n=== 전체 검증 결과 ===")

    for row in results:
        print(
            f"{row['parser']} | "
            f"유형: {row['type_accuracy']:.2f}% | "
            f"전체: {row['full_accuracy']:.2f}% | "
            f"잘못된 실행 판단: "
            f"{row['false_execution']}/{row['unknown_count']}"
        )

    print("\n저장 완료:", OUTPUT_PATH)


if __name__ == "__main__":
    main()