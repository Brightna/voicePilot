
import os
import time

from speech.recognition import load_model, record_audio, transcribe_audio


def compare_models():
    model_sizes = ["tiny", "base", "small"]
    results = []

    # 음성 한 번 녹음
    audio = record_audio()

    for model_size in model_sizes:
        print(f"\n[{model_size}] 모델 테스트 시작")

        # 모델 로딩 시간 측정
        load_start = time.time()
        load_model(model_size)
        load_elapsed = time.time() - load_start

        # 음성 인식 시간 측정
        start_time = time.time()
        text = transcribe_audio(audio, model_size)
        elapsed_time = time.time() - start_time

        print("인식 결과:", text)
        print(f"모델 로딩 시간: {load_elapsed:.2f}초")
        print(f"음성 인식 시간: {elapsed_time:.2f}초")

        results.append({
            "model": model_size,
            "text": text,
            "load_time": load_elapsed,
            "elapsed": elapsed_time
        })

    # 결과 저장
    os.makedirs("results", exist_ok=True)

    with open(
        "results/model_comparison.txt",
        "w",
        encoding="utf-8"
    ) as file:
        for result in results:
            file.write(f"모델: {result['model']}\n")
            file.write(f"인식 결과: {result['text']}\n")
            file.write(f"모델 로딩 시간: {result['load_time']:.2f}초\n")
            file.write(f"음성 인식 시간: {result['elapsed']:.2f}초\n")
            file.write("-" * 30 + "\n")

    print("\n비교 결과 저장 완료!")


if __name__ == "__main__":
    compare_models()
