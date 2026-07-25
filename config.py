import json,os

class Config:
    def __init__(self,filename="config.json"):
        self.filename=filename
        self.reload()

    def reload(self):
        if os.path.exists(self.filename):
            with open(self.filename,"r",encoding="utf-8") as f:
                self.data=json.load(f)
        else:
            self.data={}

        audio=self.data.get("audio",{})
        whisper=self.data.get("whisper",{})
        translator=self.data.get("translator",{})

        self.audio_seconds=audio.get(
            "seconds",
            10
        )

        self.audio_device=audio.get(
            "device",
            None
        )

        self.whisper_model=whisper.get(
            "model",
            "small.en"
        )

        self.whisper_language=whisper.get(
            "language",
            "en"
        )

        self.translate_model=translator.get(
            "model",
            "facebook/nllb-200-distilled-600M"
        )

        self.translate_target=translator.get(
            "target",
            "zho_Hant"
        )

        self.audio_device=self.data.get(
            "audio",
            {}
        ).get(
            "device",
            None
        )

    @property
    def subtitle(self):
        return self.data.get(
            "subtitle",
            {}
        )

    def show(self):
        print("目前設定:")
        print("Audio seconds :",self.audio_seconds)
        print("Audio device  :",self.audio_device)
        print("Whisper model :",self.whisper_model)
        print("Language      :",self.whisper_language)
        print("Translator    :",self.translate_model)
        print("Target        :",self.translate_target)