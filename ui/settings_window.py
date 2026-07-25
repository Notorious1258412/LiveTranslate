import json
import os
from model_manager import get_whisper_models,get_translate_models
from audio_device_manager import get_loopback_devices
from PySide6.QtWidgets import QWidget,QFormLayout,QLineEdit,QComboBox,QPushButton,QVBoxLayout,QLabel

CONFIG_FILE="config.json"

class SettingsWindow(QWidget):
    def __init__(self,subtitle_window=None):
        super().__init__()
        self.subtitle_window=subtitle_window
        self.setWindowTitle("LiveTranslate 設定")
        self.resize(420,550)
        self.load_config()
        self.init_ui()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE,"r",encoding="utf-8") as f:
                    self.data=json.load(f)
            except:
                self.data={}
        else:
            self.data={}

    def save_config(self):
        with open(CONFIG_FILE,"w",encoding="utf-8") as f:
            json.dump(
                self.data,
                f,
                indent=4,
                ensure_ascii=False
            )

    def refresh_subtitle(self):
        if self.subtitle_window:
            self.subtitle_window.load_style()
            self.subtitle_window.update_font()

    def init_ui(self):
        layout=QVBoxLayout()

        title=QLabel("LiveTranslate 設定")
        layout.addWidget(title)

        form=QFormLayout()

        # 音訊裝置
        self.audio_device=QComboBox()
        audio_devices=get_loopback_devices()
        self.audio_device.addItems(
            audio_devices
        )
        current_device=self.data.get(
            "audio",
            {}
        ).get(
            "device",
            ""
        )
        if current_device:
            self.audio_device.setCurrentText(
                current_device
            )
        self.audio_device.currentTextChanged.connect(
            self.update_audio_device
        )
        form.addRow(
            "音訊裝置",
            self.audio_device
        )

        self.audio_seconds=QLineEdit(
            str(self.data.get("audio_seconds",10))
        )
        self.audio_seconds.returnPressed.connect(
            self.update_audio_seconds
        )
        form.addRow(
            "音訊擷取秒數",
            self.audio_seconds
        )

        self.whisper_model=QComboBox()

        from model_manager import (
            get_whisper_models,
            get_translate_models
        )
        models=get_whisper_models()

        self.whisper_model.addItems(
            models
        )

        self.whisper_model.setCurrentText(
            self.data.get(
                "whisper_model",
                "small.en"
            )
        )
        self.whisper_model.currentTextChanged.connect(
            self.update_whisper
        )
        form.addRow(
            "語音辨識模型",
            self.whisper_model
        )

        self.language=QLineEdit(
            self.data.get(
                "language",
                "en"
            )
        )
        self.language.returnPressed.connect(
            self.update_language
        )
        form.addRow(
            "辨識語言",
            self.language
        )

        self.target=QLineEdit(
            self.data.get(
                "target",
                "zho_Hant"
            )
        )
        self.target.returnPressed.connect(
            self.update_target
        )
        form.addRow(
            "翻譯目標語言",
            self.target
        )
        self.translate_model=QComboBox()

        self.translate_model.addItems(
            get_translate_models()
        )

        self.translate_model.setCurrentText(
            self.data.get(
                "translate_model",
                ""
            )
        )

        self.translate_model.currentTextChanged.connect(
            self.update_translate_model
        )

        form.addRow(
            "翻譯模型",
            self.translate_model
        )
        subtitle=self.data.get(
            "subtitle",
            {}
        )

        self.subtitle_width=QLineEdit(
            str(
                subtitle.get(
                    "width",
                    900
                )
            )
        )
        self.subtitle_width.returnPressed.connect(
            self.update_size
        )
        form.addRow(
            "字幕寬度",
            self.subtitle_width
        )

        self.subtitle_height=QLineEdit(
            str(
                subtitle.get(
                    "height",
                    180
                )
            )
        )
        self.subtitle_height.returnPressed.connect(
            self.update_size
        )
        form.addRow(
            "字幕高度",
            self.subtitle_height
        )

        self.text_color=QLineEdit(
            subtitle.get(
                "text_color",
                "white"
            )
        )
        self.text_color.returnPressed.connect(
            self.update_text_color
        )
        form.addRow(
            "字體顏色",
            self.text_color
        )

        self.font_ratio=QLineEdit(
            str(
                subtitle.get(
                    "font_ratio",
                    7
                )
            )
        )
        self.font_ratio.returnPressed.connect(
            self.update_subtitle
        )
        form.addRow(
            "字幕字體比例",
            self.font_ratio
        )

        self.background=QLineEdit(
            subtitle.get(
                "background",
                "rgba(0,0,0,160)"
            )
        )
        self.background.returnPressed.connect(
            self.update_background
        )
        form.addRow(
            "字幕背景",
            self.background
        )

        layout.addLayout(form)

        close_btn=QPushButton("關閉")
        close_btn.clicked.connect(
            self.close
        )
        layout.addWidget(close_btn)

        self.setLayout(layout)
    def update_audio_seconds(self):
        self.data["audio_seconds"]=int(
            self.audio_seconds.text()
        )
        self.save_config()

    def update_whisper(self,text):
        self.data["whisper_model"]=text
        self.save_config()

    def update_language(self):
        self.data["language"]=self.language.text()
        self.save_config()

    def update_target(self):
        self.data["target"]=self.target.text()
        self.save_config()

    def update_size(self):
        if "subtitle" not in self.data:
            self.data["subtitle"]={}

        try:
            width=int(
                self.subtitle_width.text()
            )
            height=int(
                self.subtitle_height.text()
            )

            width=max(
                400,
                min(
                    width,
                    1600
                )
            )

            height=max(
                80,
                min(
                    height,
                    500
                )
            )

            self.data["subtitle"]["width"]=width
            self.data["subtitle"]["height"]=height

            self.subtitle_width.setText(
                str(width)
            )
            self.subtitle_height.setText(
                str(height)
            )

            self.save_config()

            if self.subtitle_window:
                self.subtitle_window.resize(
                    width,
                    height
                )
                self.subtitle_window.update_font()

        except:
            pass

    def update_subtitle(self):
        if "subtitle" not in self.data:
            self.data["subtitle"]={}

        self.data["subtitle"]["font_ratio"]=int(
            self.font_ratio.text()
        )

        self.save_config()
        self.refresh_subtitle()

    def update_background(self):
        if "subtitle" not in self.data:
            self.data["subtitle"]={}

        self.data["subtitle"]["background"]=(
            self.background.text()
        )

        self.save_config()
        self.refresh_subtitle()

    def update_text_color(self):
        if "subtitle" not in self.data:
            self.data["subtitle"]={}

        self.data["subtitle"]["text_color"]=(
            self.text_color.text()
        )

        self.save_config()
        self.refresh_subtitle()

    def update_translate_model(self,text):

        self.data["translate_model"]=text

        self.save_config()

    def update_audio_device(self,text):

        if "audio" not in self.data:

            self.data["audio"]={}


        self.data["audio"]["device"]=text


        self.save_config()