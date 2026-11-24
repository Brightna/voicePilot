import sounddevice as sd
import numpy as np
import time
import wave
import os

SAMPLE_RATE = 16000
DURATION = 8
SAVE_DIR = "dataset/audio"


def record_audio(filename):
    print("녹음 준비 중...")

    audio = sd.rec(
        int(SAMPLE_RATE * DURATION),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        device=5
    )

    time.sleep(1)
    print("지금 말씀하세요!", flush=True)

    sd.wait()

    audio = (np.clip(audio, -1, 1) * 32767).astype(np.int16)

    os.makedirs(SAVE_DIR, exist_ok=True)
    path = os.path.join(SAVE_DIR, filename)

    with wave.open(path, "wb") as file:
        file.setnchannels(1)
        file.setsampwidth(2)
        file.setframerate(SAMPLE_RATE)
        file.writeframes(audio.tobytes())

    print("저장 완료:", path)


if __name__ == "__main__":
    commands = [
        "계산기 켜 줘",
        "크롬 실행해 줘",
        "메모장 열어 줘",
        "계산기 좀 띄워 줘",
        "크롬 좀 켜 줄래",
        "메모장 실행 부탁해",
        "나 계산기 쓰고 싶어",
        "인터넷 좀 하고 싶어",
        "메모장 켜 봐",
        "오늘 날씨 검색해 줘",
        "인공지능 뉴스 검색해 줘",
        "숭실대학교 검색해 줘",
        "파이썬 사용법 찾아 줘",
        "내일 서울 날씨 알아봐 줘",
        "구글에서 맛집 검색해 줘",
        "바탕화면에 있는 테스트 파일 열어 줘",
        "다운로드 폴더에 있는 보고서 열어 줘",
        "문서 폴더에 있는 과제 파일 열어 줘",
        "테스트 파일 열어 줘",
        "바탕화면에 있는 사진 열어 줘",
        "안녕 반가워",
        "오늘 너무 피곤하다",
        "계산기 켜지 마",
        "크롬 열 필요 없어",
        "메모장이 어디 있더라",
        "",
        "계산기",
        "열어 줘",
        "구글에서 인공지능이 미래 사회에 미치는 영향에 대해 검색해 줘",
        "바탕화면에 있는 테스트 파일을 찾아서 열어 줘"
    ]

    import csv

    with open("dataset/labels.csv", "w",
              encoding="utf-8-sig", newline="") as file:

        writer = csv.writer(file)
        writer.writerow(["filename", "reference"])

        for i, command in enumerate(commands, start=1):
            filename = f"{i:03d}.wav"
            path = os.path.join(SAVE_DIR, filename)

            print(f"\n[{i}/{len(commands)}]")
            print("발화:", command if command else "(아무 말도 하지 않기)")

            if os.path.exists(path):
                print("기존 녹음 파일 사용")
            else:
                input("Enter를 누르면 녹음 시작")
                record_audio(filename)

            writer.writerow([filename, command])
            file.flush()

    print("\n데이터셋 제작 완료!")