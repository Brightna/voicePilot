import csv

from compare_correction import (
    INPUT_PATH,
    VOCABULARY,
    correct_text,
    edit_distance,
    normalize
)


def analyze():
    with open(INPUT_PATH, encoding="utf-8-sig") as file:
        rows = list(csv.DictReader(file))

    for model in ["base", "small"]:
        for threshold in [0.6, 0.8, 0.9]:
            print(f"\n=== {model} / threshold={threshold} ===")

            for row in rows:
                if row["model"] != model:
                    continue

                reference = row["reference"]
                original = row["prediction"]

                corrected = correct_text(
                    original,
                    VOCABULARY,
                    threshold,
                    use_jamo=True
                )

                if normalize(original) == normalize(corrected):
                    continue

                before = edit_distance(
                    normalize(reference),
                    normalize(original)
                )

                after = edit_distance(
                    normalize(reference),
                    normalize(corrected)
                )

                if after < before:
                    result = "개선"
                elif after > before:
                    result = "악화"
                else:
                    result = "오류 수 동일"

                print(f"\n[{result}] {row['filename']}")
                print("정답:", reference)
                print("보정 전:", original)
                print("보정 후:", corrected)
                print(f"오류 수: {before} -> {after}")


if __name__ == "__main__":
    analyze()