import csv
import time
import os
import wave
import numpy as np
from faster_whisper import WhisperModel

MODEL_SIZES = ["tiny", "base", "small"]
DATASET_DIR = "dataset/audio"
LABEL_PATH = "dataset/labels.csv"
RESULT_PATH = "results/model_experiment_prompt.csv"
INITIAL_PROMPT = "계산기, 크롬, 메모장, 파일 탐색기, 바탕화면, 다운로드, 문서, 실행, 검색"

def load_audio(path):
    with wave.open(path, "rb") as file:
        audio = file.readframes(file.getnframes())

    return np.frombuffer(audio, dtype=np.int16).astype(np.float32) / 32768.0

def run_experiment():
    with open(LABEL_PATH, encoding="utf-8-sig") as file:
        dataset = list(csv.DictReader(file))

    os.makedirs("results", exist_ok=True)

    with open(RESULT_PATH, "w",
              encoding="utf-8-sig", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "model",
            "filename",
            "reference",
            "prediction",
            "elapsed"
        ])

        for model_size in MODEL_SIZES:
            print(f"\n=== {model_size} 모델 ===")

            model = WhisperModel(
                model_size,
                device="cpu",
                compute_type="int8"
            )

            for i, row in enumerate(dataset, start=1):
                path = os.path.join(
                    DATASET_DIR, row["filename"]
                )

                audio = load_audio(path)

                start = time.perf_counter()

                segments, info = model.transcribe(
                    audio,
                    language="ko",
                    beam_size=5,
                    initial_prompt=INITIAL_PROMPT
                )

                prediction = ""

                for segment in segments:
                    prediction += segment.text

                prediction = prediction.strip()
                elapsed = time.perf_counter() - start

                writer.writerow([
                    model_size,
                    row["filename"],
                    row["reference"],
                    prediction,
                    round(elapsed, 4)
                ])

                file.flush()

                print(f"[{i}/{len(dataset)}]")
                print("정답:", row["reference"])
                print("인식:", prediction)
                print(f"시간: {elapsed:.4f}초")

            del model

    print("\n실험 완료:", RESULT_PATH)


if __name__ == "__main__":
    run_experiment()