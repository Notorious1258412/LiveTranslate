import numpy as np
from asr.whisper_engine import WhisperEngine


engine = WhisperEngine("small")


# 測試用靜音
audio = np.zeros(
    16000,
    dtype=np.float32
)


text = engine.transcribe(audio)

print("結果:")
print(text)