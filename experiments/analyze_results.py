import csv
import re
import statistics

RESULT_PATH = "results/model_experiment.csv"


def normalize(text):
    return re.sub(r"[^가-힣a-zA-Z0-9]", "", text).lower()


def edit_distance(a, b):
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]

    for i in range(len(a) + 1):
        dp[i][0] = i

    for j in range(len(b) + 1):
        dp[0][j] = j

    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1

            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost
            )

    return dp[len(a)][len(b)]


def analyze():
    with open(RESULT_PATH, encoding="utf-8-sig") as file:
        rows = list(csv.DictReader(file))

    for model in ["tiny", "base", "small"]:
        data = [row for row in rows if row["model"] == model]

        total_chars = 0
        total_errors = 0
        correct = 0
        count = 0
        times = []

        for row in data:
            reference = normalize(row["reference"])
            prediction = normalize(row["prediction"])

            times.append(float(row["elapsed"]))

            if reference:
                total_chars += len(reference)
                total_errors += edit_distance(reference, prediction)
                count += 1

                if reference == prediction:
                    correct += 1
            else:
                print(f"\n[{model}] 무음 인식: {row['prediction']!r}")

        cer = total_errors / total_chars * 100
        accuracy = correct / count * 100

        print(f"\n=== {model} 분석 결과 ===")
        print(f"평가 문장 수: {count}")
        print(f"완전 일치: {correct}/{count}")
        print(f"완전 일치율: {accuracy:.2f}%")
        print(f"문자 오류율(CER): {cer:.2f}%")
        print(f"평균 처리 시간: {statistics.mean(times):.4f}초")
        print(f"중앙값 처리 시간: {statistics.median(times):.4f}초")
        print(f"최대 처리 시간: {max(times):.4f}초")


if __name__ == "__main__":
    analyze()