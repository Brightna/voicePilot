
import sounddevice as sd
from faster_whisper import WhisperModel

models = {}


# Whisper 모델 불러오기
def load_model(model_size="base"):
    if model_size not in models:
        print(f"{model_size} 모델을 불러오는 중...")

        models[model_size] = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8"
        )

    return models[model_size]


# 음성 녹음
def record_audio():
    samplerate = 16000
    duration = 5

    print(f"{duration}초 동안 말씀해 주세요!")

    audio = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype="float32"
    )

    sd.wait()
    print("녹음 완료!")

    return audio.flatten()

# 녹음된 음성 인식
def transcribe_audio(audio, model_size="base"):
    whisper_model = load_model(model_size)

    segments, info = whisper_model.transcribe(
        audio,
        language="ko",
        beam_size=5,
        initial_prompt="계산기, 크롬, 메모장, 파일 탐색기, 바탕화면, 다운로드, 문서, 실행, 검색"
    )

    text = ""

    for segment in segments:
        text += segment.text

    return text.strip()


# 기본 음성 인식
def listen():
    try:
        audio = record_audio()
        text = transcribe_audio(audio, "base")

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
