import csv
import re
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from speech.error_correction import correct_text, edit_distance


INPUT_PATH = "results/model_experiment_prompt.csv"
RESULT_PATH = "results/correction_experiment.csv"

MODELS = ["base", "small"]
THRESHOLDS = [0.5, 0.6, 0.7, 0.8, 0.9]

VOCABULARY = [
    "계산기",
    "크롬",
    "메모장",
    "파일 탐색기",
    "바탕화면",
    "다운로드",
    "문서",
    "파이썬",
    "인공지능"
]


def normalize(text):
    return re.sub(r"[^가-힣a-zA-Z0-9]", "", text).lower()


def evaluate(rows, method, threshold):
    total_chars = 0
    total_errors = 0
    correct = 0
    count = 0

    improved = 0
    worsened = 0
    changed = 0
    overcorrected = 0
    silence_output = 0
    total_time = 0.0

    for row in rows:
        reference = normalize(row["reference"])
        original = row["prediction"]

        start = time.perf_counter()

        if method == "none":
            corrected = original
        else:
            corrected = correct_text(
                original,
                VOCABULARY,
                threshold,
                use_jamo=(method == "jamo")
            )

        total_time += time.perf_counter() - start

        before = normalize(original)
        after = normalize(corrected)

        if before != after:
            changed += 1

        if not reference:
            if after:
                silence_output += 1
            continue

        before_error = edit_distance(reference, before)
        after_error = edit_distance(reference, after)

        if after_error < before_error:
            improved += 1

        if after_error > before_error:
            worsened += 1

        if before_error == 0 and after_error > 0:
            overcorrected += 1

        if reference == after:
            correct += 1

        total_chars += len(reference)
        total_errors += after_error
        count += 1

    return {
        "accuracy": round(correct / count * 100, 2),
        "cer": round(total_errors / total_chars * 100, 2),
        "improved": improved,
        "worsened": worsened,
        "changed": changed,
        "overcorrected": overcorrected,
        "silence_output": silence_output,
        "avg_time_ms": round(total_time / len(rows) * 1000, 4)
    }


def run_experiment():
    with open(INPUT_PATH, encoding="utf-8-sig") as file:
        dataset = list(csv.DictReader(file))

    with open(
        RESULT_PATH, "w", encoding="utf-8-sig", newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "model",
            "method",
            "threshold",
            "accuracy",
            "cer",
            "improved",
            "worsened",
            "changed",
            "overcorrected",
            "silence_output",
            "avg_time_ms"
        ])

        for model in MODELS:
            rows = [
                row for row in dataset
                if row["model"] == model
            ]

            print(f"\n=== {model} 모델 ===")

            conditions = [("none", 0)]

            for method in ["char", "jamo"]:
                for threshold in THRESHOLDS:
                    conditions.append((method, threshold))

            for method, threshold in conditions:
                result = evaluate(rows, method, threshold)

                writer.writerow([
                    model,
                    method,
                    threshold,
                    *result.values()
                ])

                print(
                    f"{method:4s} | "
                    f"threshold={threshold:.1f} | "
                    f"ACC={result['accuracy']:.2f}% | "
                    f"CER={result['cer']:.2f}% | "
                    f"개선={result['improved']} | "
                    f"악화={result['worsened']} | "
                    f"과잉보정={result['overcorrected']}"
                )

    print("\n실험 완료:", RESULT_PATH)


if __name__ == "__main__":
    run_experiment()