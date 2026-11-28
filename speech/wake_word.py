import re

from speech.recognition import (
    record_audio,
    transcribe_audio,
    load_model
)


WAKE_WORD = "피코야"


def normalize_wake_word(text):
    text = text.strip().lower()
    text = re.sub(r"[\s.,!?。！？]", "", text)

    return text


def detect_wake_word(text):
    normalized = normalize_wake_word(text)

    return normalized == WAKE_WORD


def wait_for_wake_word():
    load_model("base")

    print("피코 대기 중...")

    while True:
        audio = record_audio(2)
        text = transcribe_audio(audio, "base")

        print("인식 결과:", text)

        if detect_wake_word(text):
            print("피코 활성화!")
            return True


if __name__ == "__main__":
    wait_for_wake_word()