import sounddevice as sd
import numpy as np

print("녹음 시작!")
audio = sd.rec(48000 * 3, samplerate=48000,
               channels=1, dtype='float32')
sd.wait()

print("녹음 완료!")
print("최대 음량:", np.max(np.abs(audio)))