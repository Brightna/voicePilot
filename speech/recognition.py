
import sounddevice as sd
from faster_whisper import WhisperModel

model = None


# Whisper 모델 불러오기
def load_model():
    global model

    if model is None:
        model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8"
        )

    return model


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
def listen():
    try:
        whisper_model = load_model()
        audio = record_audio()

        segments, info = whisper_model.transcribe(
            audio,
            language="ko",
            beam_size=5
        )

        text = ""

        for segment in segments:
            text += segment.text

        text = text.strip()

        print("인식 결과:", text)

        return text

    except sd.PortAudioError as e:
        print("마이크 오류:", e)
        return ""

    except Exception as e:
        print("음성 인식 오류:", e)
        return ""


if __name__ == "__main__":
    listen()