import sounddevice as sd
import numpy as np

samplerate = 16000
duration = 5

print("5초 동안 말씀해 주세요!")

audio = sd.rec(
    samplerate * duration,
    samplerate=samplerate,
    channels=1,
    dtype="float32"
)

sd.wait()

print("녹음 완료!")
print("최대 음량:", np.max(np.abs(audio)))
print("RMS 음량:", np.sqrt(np.mean(audio ** 2)))

print("녹음된 음성을 재생합니다.")

sd.play(audio, samplerate)
sd.wait()