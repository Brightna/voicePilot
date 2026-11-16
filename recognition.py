
import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel

# Whisper 모델 불러오기
model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

# 음성 녹음
def record_audio():
    samplerate = 16000

    print("3초 동안 말씀해 주세요!")

    audio = sd.rec(
        int(3 * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype="float32"
    )

    sd.wait()
    print("녹음 완료!")

    return audio.flatten()

# 음성 인식
def recognize():
    audio = record_audio()

    segments, info = model.transcribe(
        audio,
        language="ko",
        beam_size=5
    )

    text = ""

    for segment in segments:
        text += segment.text

    print("인식 결과:", text)

    return text


if __name__ == "__main__":
    recognize()
