import numpy as np
from scipy.signal import resample
from PySide6.QtCore import QThread,Signal
import pyaudiowpatch as pyaudio

from asr.whisper_engine import WhisperEngine
from translator.nllb_engine import NLLBTranslator
from subtitle_filter import SubtitleFilter

def remove_repeat(text):
    words=text.split()
    if len(words)<5:
        return text
    result=[]
    last=""
    count=0
    for w in words:
        if w.lower()==last.lower():
            count+=1
            if count>=3:
                continue
        else:
            count=0
        result.append(w)
        last=w
    return " ".join(result)

class AudioWorker(QThread):
    subtitle_signal=Signal(str,str)

    def __init__(self,p,device_index,device,config):
        super().__init__()

        self.p=p
        self.device_index=device_index
        self.device=device
        self.config=config

        self.running=True
        self.stream=None
        self.audio_buffer=[]

    def run(self):

        CHUNK=1024
        seconds=self.config.audio_seconds
        print("AudioWorker Start")

        self.stream=self.p.open(
            format=pyaudio.paFloat32,
            channels=2,
            rate=48000,
            input=True,
            input_device_index=self.device_index,
            frames_per_buffer=CHUNK
        )

        #print("音訊串流開啟完成")

        #print("音訊串流開啟完成")

        whisper=WhisperEngine(
            self.config.whisper_model
        )
        translator=NLLBTranslator(
            self.config.translate_model
        )
        subtitle_filter=SubtitleFilter()
        while self.running:
            try:
                #print("Audio loop running")
                available=self.stream.get_read_available()

                #print("available:",available)

                if available>=CHUNK:
                    #print("收到音訊:", available)
                    data=self.stream.read(
                        CHUNK,
                        exception_on_overflow=False
                    )
                    audio=np.frombuffer(
                        data,
                        dtype=np.float32
                    )
                    self.audio_buffer.extend(
                        audio
                    )

                else:
                    self.msleep(10)
                    continue

               
                if len(self.audio_buffer)>=int(
                    self.device["defaultSampleRate"]*seconds
                ):
                    audio_data=np.array(
                        self.audio_buffer,
                        dtype=np.float32
                    )
                    self.audio_buffer.clear()
                    if len(audio_data)%2==0:
                        audio_data=audio_data.reshape(
                            -1,
                            2
                        )
                        audio_data=audio_data.mean(
                            axis=1
                        )
                    audio_data=resample(
                        audio_data,
                        int(len(audio_data)/3)
                    )
                    audio_data*=2.0

                    # 音量檢查
                    volume=np.max(
                        np.abs(audio_data)
                    )

                    if volume<0.015:
                        continue
                    #print("開始 Whisper")

                    text=whisper.transcribe(
                        audio_data
                    )
                    text=remove_repeat(
                        text
                    )
                    if len(text)>200:

                        text=text[:200]
 
                    print("Whisper結果:",text)

                    if text:
                        text=subtitle_filter.filter(
                            text
                        )
                        if text:

                            if len(text)>200:
                                text=text[:200]

                                print("開始翻譯")
                            zh_text=translator.translate(
                                text
                            )
                            print(
                                "翻譯結果:",
                                zh_text
                            )
                            
                            if len(zh_text)>200:
                                zh_text=zh_text[:200]
                            self.subtitle_signal.emit(
                                text,
                                zh_text
                            )
            except Exception as e:
                print(
                    "audio error:",
                    e
                )
                self.msleep(100)
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
    def stop(self):
        self.running=False