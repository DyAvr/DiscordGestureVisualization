import asyncio
import json
import os
import sys
import cv2
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QMainWindow, QPushButton, QWidget, QCheckBox, QComboBox, QLineEdit,
                             QDialog, QHBoxLayout, QGroupBox, QLabel, QDialogButtonBox, QVBoxLayout, QStyleFactory,
                             QSizePolicy)

from bot import Bot


class GestureControlApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gesture Recognition for Discord")
        self.setStyleSheet(discord_style)
        self.setGeometry(0, 0, 1280, 720)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.start_button = QPushButton("Старт")
        self.start_button.setStyleSheet("font-size: 32px;")
        self.start_button.setFixedSize(500, 75)
        self.start_button.clicked.connect(self.start)
        layout.addWidget(self.start_button)
        self.settings_button = QPushButton("Настройки")
        self.settings_button.setFixedSize(500, 75)
        self.settings_button.setStyleSheet("font-size: 32px;")
        self.settings_button.clicked.connect(self.settings)
        layout.addWidget(self.settings_button)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.avatar_checkbox = QCheckBox("Менять аватарку")
        self.send_gesture_checkbox = QCheckBox("Отправлять жест в чат")
        self.camera_combobox = QComboBox()
        self.gesture_checkboxes = []
        gestures = ["👍", "👎", "✌️", "👌", "✋"]
        for gesture in gestures:
            checkbox = QCheckBox(gesture)
            self.gesture_checkboxes.append(checkbox)
        self.token_edit = QLineEdit()
        self.channel_edit = QLineEdit()
        camera_indices = get_available_cameras()
        for index in camera_indices:
            self.camera_combobox.addItem(f"Camera {index}", index)
        self.setStyle(QStyleFactory.create('Fusion'))
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as f:
                settings = json.load(f)
            self.avatar_checkbox.setChecked(settings.get("avatar_checkbox", True))
            self.send_gesture_checkbox.setChecked(settings.get("send_gesture_checkbox", True))
            self.camera_combobox.setCurrentIndex(settings.get("camera_index", 0))
            self.token_edit.setText(settings.get("token", ""))
            self.channel_edit.setText(settings.get("channel_id", 0))
            for i, checkbox in enumerate(self.gesture_checkboxes):
                checkbox.setChecked(settings.get("gesture_checkboxes", [True] * len(self.gesture_checkboxes))[i])
        else:
            self.avatar_checkbox.setChecked(True)
            self.send_gesture_checkbox.setChecked(True)
            for checkbox in self.gesture_checkboxes:
                checkbox.setChecked(True)

    def start(self):
        c_index = self.camera_combobox.currentIndex()
        if c_index < 0:
            c_index = 0
        bot = Bot(self.token_edit.text(), self.channel_edit.text(), c_index)
        bot.start()
        self.close()

    def settings(self):
        settings_dialog = QDialog(self)
        settings_dialog.setWindowTitle("Settings")
        settings_dialog.setGeometry(0, 0, 1280, 720)
        layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        mode_group = QGroupBox("Mode of operation")
        mode_layout = QVBoxLayout()
        mode_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mode_layout.addWidget(self.avatar_checkbox)
        mode_layout.addWidget(self.send_gesture_checkbox)
        mode_group.setLayout(mode_layout)
        top_layout.addWidget(mode_group)

        gestures_group = QGroupBox("Select gestures")
        gestures_layout = QVBoxLayout()
        gestures_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        gestures_label = QLabel("Select available gestures:")
        gestures_layout.addWidget(gestures_label)
        for checkbox in self.gesture_checkboxes:
            checkbox.setStyleSheet("font-size: 28px;")
            gestures_layout.addWidget(checkbox)
        gestures_group.setLayout(gestures_layout)
        top_layout.addWidget(gestures_group)

        layout.addLayout(top_layout)

        camera_group = QGroupBox("Select camera")
        camera_layout = QVBoxLayout()
        camera_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        camera_layout.addWidget(self.camera_combobox)
        camera_group.setLayout(camera_layout)
        layout.addWidget(camera_group)

        bottom_layout = QHBoxLayout()
        token_group = QGroupBox("Bot token and channel ID settings")
        token_layout = QVBoxLayout()
        token_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        token_label = QLabel("Bot token:")
        token_layout.addWidget(token_label)
        token_layout.addWidget(self.token_edit)
        channel_label = QLabel("Channel ID:")
        token_layout.addWidget(channel_label)
        token_layout.addWidget(self.channel_edit)
        token_group.setLayout(token_layout)
        bottom_layout.addWidget(token_group)

        layout.addLayout(bottom_layout)

        ok_button = QDialogButtonBox.StandardButton.Ok
        cancel_button = QDialogButtonBox.StandardButton.Cancel
        button_box = QDialogButtonBox(ok_button | cancel_button)

        button_box.accepted.connect(lambda: self.save_settings(settings_dialog))
        button_box.rejected.connect(settings_dialog.reject)
        button_box.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        layout.addWidget(button_box, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)

        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        settings_dialog.setLayout(layout)
        settings_dialog.showMaximized()

    def save_settings(self, dialog):
        # Создаем словарь с настройками
        settings = {
            "avatar_checkbox": self.avatar_checkbox.isChecked(),
            "send_gesture_checkbox": self.send_gesture_checkbox.isChecked(),
            "camera_index": self.camera_combobox.currentIndex(),
            "gesture_checkboxes": [checkbox.isChecked() for checkbox in self.gesture_checkboxes],
            "token": self.token_edit.text(),
            "channel_id": self.channel_edit.text()
        }

        # Записываем словарь в json файл
        with open("settings.json", "w") as f:
            json.dump(settings, f)

        # Закрываем диалог настроек
        dialog.accept()


def get_available_cameras():
    camera_indices = []
    for i in range(10):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            camera_indices.append(i)
            cap.release()
    return camera_indices


discord_style = """

QWidget {
    color: #FFFFFF;
}

QComboBox {
    border: 1px solid gray;
    border-radius: 3px;
    font-size: 18px;
    color: #4F545C;
    padding: 1px 18px 1px 3px;
    min-width: 6em;
}

QComboBox::down-arrow:on { /* shift the arrow when popup is open */
    top: 1px;
    left: 1px;
}

QPushButton {
    background-color: #4F545C;
    border: 2px solid gray;
    border-radius: 15px;
    margin-top: 10px;
    height:40px;
    width:150px;
    font-size: 20px;
}

QLineEdit {
    font-size: 18px;
    color: #4F545C;
}

QLabel {
    font-size: 18px;
}

QMainWindow {
    background-image: url("images/discord_background.png"); 
    background-repeat: no-repeat; 
    background-position: center;
}

QDialog {
    background-image: url("images/discord_background.png"); 
    background-repeat: no-repeat; 
    background-position: center;
}

QGroupBox {
    background-color: #4F545C;
    border: 2px solid gray;
    border-radius: 5px;
    margin-top: 3ex; /* leave space at the top for the title */
    font-size: 20px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    border: 2px solid gray;
    border-radius: 5px;
    subcontrol-position: top left; /* position at the top center */
    padding: 0 3px;
    font-size: 20px;
    background-color: #4F545C;
}

QCheckBox {
    spacing: 5px;
    font-size: 18px;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
}

QCheckBox::indicator:unchecked {
    image: url('images/unchecked.png');
}

QCheckBox::indicator:checked {
    image: url("images/checked.png");
}

"""