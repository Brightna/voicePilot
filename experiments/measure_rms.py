import csv
import time

import numpy as np
import sounddevice as sd


SAMPLE_RATE = 16000
DEVICE = 5
DURATION = 5
FRAME_MS = 30
FRAME_SIZE = int(SAMPLE_RATE * FRAME_MS / 1000)

OUTPUT_PATH = "results/rms_measurement.csv"

CONDITIONS = [
    ("silence", "아무 소리도 내지 마세요."),
    ("quiet_voice", "작은 목소리로 계속 말하세요."),
    ("normal_voice", "평소 목소리로 계속 말하세요."),
    ("loud_voice", "큰 목소리로 계속 말하세요."),
    ("keyboard", "키보드를 계속 타이핑하세요."),
    ("mouse", "마우스를 반복해서 클릭하세요.")
]


def calculate_rms(frame):
    return float(np.sqrt(np.mean(frame ** 2)))


def record_audio():
    audio = sd.rec(
        int((DURATION + 1) * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        device=DEVICE
    )

    time.sleep(1)

    print("지금 시작!", flush=True)

    sd.wait()

    print("측정 완료!")

    return audio.flatten()[SAMPLE_RATE:]


def measure_frames(audio):
    values = []

    for start in range(
        0, len(audio) - FRAME_SIZE + 1, FRAME_SIZE
    ):
        frame = audio[start:start + FRAME_SIZE]
        values.append(calculate_rms(frame))

    return values


def main():
    rows = []

    for condition, instruction in CONDITIONS:
        print("\n" + "=" * 45)
        print("측정 조건:", condition)
        print(instruction)

        input("준비되면 Enter를 누르세요.")

        audio = record_audio()
        values = measure_frames(audio)

        print(f"최솟값: {np.min(values):.6f}")
        print(f"평균값: {np.mean(values):.6f}")
        print(f"중앙값: {np.median(values):.6f}")
        print(f"95백분위: {np.percentile(values, 95):.6f}")
        print(f"최댓값: {np.max(values):.6f}")

        for index, rms in enumerate(values):
            rows.append({
                "condition": condition,
                "frame": index,
                "time": round(index * FRAME_MS / 1000, 3),
                "rms": rms
            })

    with open(
        OUTPUT_PATH, "w",
        newline="", encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["condition", "frame", "time", "rms"]
        )

        writer.writeheader()
        writer.writerows(rows)

    print("\n저장 완료:", OUTPUT_PATH)


if __name__ == "__main__":
    main()