import json
import os
from PySide6.QtWidgets import QWidget,QLabel,QVBoxLayout
from PySide6.QtCore import Qt,QPoint,QTimer
from PySide6.QtGui import QFont,QGuiApplication

CONFIG_FILE="config.json"

class SubtitleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.drag_pos=QPoint()
        self.resize_margin=15
        self.resize_mode=None
        self.resize_start_x=0
        self.resize_start_width=0
        self.resize_start_pos_x=0
        self.settings=None

        self.min_width=400
        self.max_width=1600
        
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint|
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.setMinimumWidth(self.min_width)
        self.setMaximumWidth(self.max_width)
        self.min_height=80
        self.max_height=500

        layout=QVBoxLayout(self)
        layout.setContentsMargins(10,10,10,10)

        self.label=QLabel()
        self.label.setWordWrap(True)
        self.label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(self.label)

        self.save_timer=QTimer()
        self.save_timer.setSingleShot(True)
        self.save_timer.timeout.connect(
            self.save_geometry
        )

        self.load_geometry()
        self.load_style()
        self.update_font()

    def get_subtitle_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE,"r",encoding="utf-8") as f:
                    data=json.load(f)
                return data.get("subtitle",{})
            except:
                pass
        return {}

    def load_style(self):
        cfg=self.get_subtitle_config()

        text_color=cfg.get(
            "text_color",
            "white"
        )
        background=cfg.get(
            "background",
            "rgba(0,0,0,160)"
        )
        radius=cfg.get(
            "radius",
            10
        )
        padding=cfg.get(
            "padding",
            10
        )

        self.label.setStyleSheet(
            f"""
            QLabel{{
                color:{text_color};
                background-color:{background};
                border-radius:{radius}px;
                padding:{padding}px;
            }}
            """
        )

    def update_text(self,english,chinese):
        text=english+"\n"+chinese

        self.label.setText(text)

        self.label.setFixedWidth(
            self.width()-20
        )

        self.adjust_text_size()

    def adjust_text_size(self):
        self.label.setMaximumHeight(
            self.height()-20
        )

    def update_font(self):
        cfg=self.get_subtitle_config()

        ratio=cfg.get(
            "font_ratio",
            7
        )

        minimum=cfg.get(
            "font_size_min",
            12
        )

        size=min(
            60,
            max(
                minimum,
                int(self.height()/ratio)
            )
        )

        self.label.setFont(
            QFont(
                "Microsoft JhengHei",
                size
            )
        )
    def load_geometry(self):
        if not os.path.exists(CONFIG_FILE):
            self.resize(900,self.fixed_height)
            return

        try:
            with open(CONFIG_FILE,"r",encoding="utf-8") as f:
                data=json.load(f)

            cfg=data.get("subtitle",{})

            self.setGeometry(
                cfg.get("x",300),
                cfg.get("y",700),
                cfg.get("width",900),
                cfg.get("height",180)
            )

        except:
            self.resize(
                900,
                self.fixed_height
            )

    def save_geometry(self):
        data={}

        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE,"r",encoding="utf-8") as f:
                    data=json.load(f)
            except:
                data={}

        cfg=data.get("subtitle",{})

        cfg.update({
            "x":self.x(),
            "y":self.y(),
            "width":self.width(),
            "height":self.height()
        })

        data["subtitle"]=cfg

        with open(CONFIG_FILE,"w",encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

    def delayed_save(self):
        self.save_timer.start(500)

    def mousePressEvent(self,event):
        if event.button()==Qt.MouseButton.RightButton:
            from ui.settings_window import SettingsWindow

            if self.settings is None:
                self.settings=SettingsWindow(self)

            self.settings.show()
            self.settings.raise_()
            self.settings.activateWindow()
            return

        if event.button()!=Qt.MouseButton.LeftButton:
            return

        x=event.position().x()

        if x<=self.resize_margin:
            self.resize_mode="left"
            self.resize_start_x=event.globalPosition().x()
            self.resize_start_width=self.width()
            self.resize_start_pos_x=self.x()

        elif x>=self.width()-self.resize_margin:
            self.resize_mode="right"
            self.resize_start_x=event.globalPosition().x()
            self.resize_start_width=self.width()

        else:
            self.resize_mode="move"
            self.drag_pos=event.globalPosition().toPoint()

    def mouseMoveEvent(self,event):
        x=event.position().x()

        if not event.buttons():
            if x<=self.resize_margin or x>=self.width()-self.resize_margin:
                self.setCursor(
                    Qt.CursorShape.SizeHorCursor
                )
            else:
                self.setCursor(
                    Qt.CursorShape.ArrowCursor
                )
            return

        if self.resize_mode=="right":
            diff=event.globalPosition().x()-self.resize_start_x

            new_width=self.resize_start_width+diff

            new_width=max(
                self.min_width,
                min(
                    new_width,
                    self.max_width
                )
            )

            self.resize(
                int(new_width),
                self.height()
            )

        elif self.resize_mode=="left":
            diff=event.globalPosition().x()-self.resize_start_x

            new_width=self.resize_start_width-diff

            new_width=max(
                self.min_width,
                min(
                    new_width,
                    self.max_width
                )
            )

            new_x=self.resize_start_pos_x+(
                self.resize_start_width-new_width
            )

            self.setGeometry(
                int(new_x),
                self.y(),
                int(new_width),
                self.height()
            )

        elif self.resize_mode=="move":
            current=event.globalPosition().toPoint()

            diff=current-self.drag_pos

            pos=self.pos()+diff

            screen=QGuiApplication.primaryScreen().availableGeometry()

            x=max(
                screen.left(),
                min(
                    pos.x(),
                    screen.right()-self.width()
                )
            )

            y=max(
                screen.top(),
                min(
                    pos.y(),
                    screen.bottom()-self.height()
                )
            )

            self.move(
                x,
                y
            )

            self.drag_pos=current

    def mouseReleaseEvent(self,event):
        self.resize_mode=None
        self.setCursor(
            Qt.CursorShape.ArrowCursor
        )

        self.update_font()
        self.delayed_save()

    def resizeEvent(self,event):
        w=max(
            self.min_width,
            min(
                self.width(),
                self.max_width
            )
        )

        h=max(
            self.min_height,
            min(
                self.height(),
                self.max_height
            )
        )

        if w!=self.width() or h!=self.height():
            self.resize(
                w,
                h
            )

        self.label.setFixedWidth(
            self.width()-20
        )

        self.update_font()
        self.delayed_save()

    def moveEvent(self,event):
        self.delayed_save()

    def closeEvent(self,event):
        self.save_geometry()
        event.accept()