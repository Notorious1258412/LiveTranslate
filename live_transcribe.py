import sys
import pyaudiowpatch as pyaudio
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QShortcut,QKeySequence

from config import Config
from ui.subtitle_window import SubtitleWindow
from ui.settings_window import SettingsWindow
from audio_device import get_audio_device
from audio_worker import AudioWorker


config=Config()


def get_loopback():

    p=pyaudio.PyAudio()

    devices=[]

    for i in range(p.get_device_count()):

        dev=p.get_device_info_by_index(i)

        if dev.get("isLoopbackDevice"):

            print(
                i,
                dev["name"]
            )

            devices.append(
                (
                    i,
                    dev
                )
            )

    if not devices:
        raise Exception("找不到 Loopback 裝置")


    # 先選第一個以外，可改成設定選擇
    i,dev=devices[0]

    return p,i,{
        "name":dev["name"],
        "defaultSampleRate":dev["defaultSampleRate"],
        "maxInputChannels":dev["maxInputChannels"]
    }

    raise Exception("找不到 Loopback 裝置")


app=QApplication(sys.argv)

window=SubtitleWindow()
window.show()


settings=None


def open_settings():
    global settings

    if settings is None:
        settings=SettingsWindow(window)

    #settings.show()
    settings.raise_()
    settings.activateWindow()


shortcut=QShortcut(
    QKeySequence("F12"),
    window
)

shortcut.activated.connect(
    open_settings
)


try:
    if config.audio_device:
        p,device_index,device=get_audio_device(
            config.audio_device
        )
    else:
        p,device_index,device=get_loopback()

except Exception as e:
    print("音訊錯誤:",e)
    p,device_index,device=get_loopback()


print("Audio:",device["name"])


worker=AudioWorker(
    p,
    device_index,
    device,
    config
)


def update_subtitle(en,zh):

    en=en[:200]
    zh=zh[:200]

    window.update_text(
        en,
        zh
    )


worker.subtitle_signal.connect(
    update_subtitle
)


worker.start()


def close():
    worker.stop()
    worker.wait()
    p.terminate()


app.aboutToQuit.connect(
    close
)


sys.exit(
    app.exec()
)