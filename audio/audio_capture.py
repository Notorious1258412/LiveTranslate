import pyaudiowpatch as pyaudio
import numpy as np


CHUNK = 1024


p = pyaudio.PyAudio()


# 找 WASAPI loopback 裝置
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)

    if dev.get("isLoopbackDevice"):
        print(
            i,
            dev["name"]
        )


# 選第一個 loopback
device_index = None

for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)

    if dev.get("isLoopbackDevice"):
        device_index = i
        break


if device_index is None:
    raise Exception("找不到 WASAPI Loopback")


device = p.get_device_info_by_index(device_index)

print("使用:")
print(device["name"])


stream = p.open(
    format=pyaudio.paFloat32,
    channels=device["maxInputChannels"],
    rate=int(device["defaultSampleRate"]),
    input=True,
    input_device_index=device_index,
    frames_per_buffer=CHUNK
)


print("開始擷取系統聲音")


while True:

    data = stream.read(
        CHUNK,
        exception_on_overflow=False
    )

    audio = np.frombuffer(
        data,
        dtype=np.float32
    )

    print(
        "level:",
        np.abs(audio).mean()
    )