import csv
import numpy as np

INPUT_PATH = "results/rms_measurement.csv"
OUTPUT_PATH = "results/rms_threshold_experiment.csv"

THRESHOLDS = [
    0.002, 0.003, 0.005, 0.007,
    0.010, 0.015, 0.020, 0.030
]

CONDITIONS = [
    "silence",
    "quiet_voice",
    "normal_voice",
    "loud_voice",
    "keyboard",
    "mouse"
]


def main():
    data = {c: [] for c in CONDITIONS}

    with open(INPUT_PATH, encoding="utf-8-sig") as file:
        for row in csv.DictReader(file):
            data[row["condition"]].append(float(row["rms"]))

    rows = []

    print("RMS Threshold Experiment")
    print("-" * 90)
    print(
        f"{'Threshold':>10}"
        + "".join(f"{c:>13}" for c in CONDITIONS)
    )

    for threshold in THRESHOLDS:
        row = {"threshold": threshold}

        for condition in CONDITIONS:
            values = np.array(data[condition])
            rate = np.mean(values >= threshold) * 100
            row[condition] = round(float(rate), 2)

        rows.append(row)

        print(
            f"{threshold:>10.3f}"
            + "".join(
                f"{row[c]:>12.2f}%"
                for c in CONDITIONS
            )
        )

    with open(
        OUTPUT_PATH, "w",
        newline="", encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["threshold"] + CONDITIONS
        )
        writer.writeheader()
        writer.writerows(rows)

    print("\nSaved:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
