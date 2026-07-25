import os
from faster_whisper import WhisperModel
import numpy as np

class WhisperEngine:
    def __init__(self,model_name="small.en"):

        model_path=os.path.join(
            "MODEL",
            "whisper",
            "models--Systran--faster-whisper-"+model_name
        )

        print(
            "檢查 Whisper 路徑:",
            os.path.abspath(model_path)
        )

        if os.path.exists(model_path):
            print(
                "載入本機 Whisper 模型:",
                model_path
            )
            model_name=model_path

        else:
            print(
                "載入下載 Whisper 模型:",
                model_name
            )

        self.model=WhisperModel(
            model_name,
            device="cpu",
            compute_type="int8"
        )

    def transcribe(self,audio):

        if audio.dtype!=np.float32:

            audio=audio.astype(
                np.float32
            )
 
        segments,info=self.model.transcribe(
            audio,
            language="en",
            beam_size=1,
            temperature=0,
            without_timestamps=True,

            # 開啟語音活動偵測
            vad_filter=True,

            vad_parameters={
                "min_silence_duration_ms":500
            },
            condition_on_previous_text=False
        )
        result=[]
        for segment in segments:
            text=segment.text.strip()
            if text:
                result.append(
                    text
                )
        text=" ".join(result)

        # 過濾重複字
        words=text.split()
        if len(words)>5:
            filtered=[]
            last=""
            count=0
            for w in words:
                if w.lower()==last.lower():
                    count+=1
                    if count>=3:
                        continue
                else:
                    count=0

                filtered.append(w)
                last=w

            text=" ".join(filtered)

        # 防止異常超長字幕
        if len(text)>200:
            text=text[:200]
        return text