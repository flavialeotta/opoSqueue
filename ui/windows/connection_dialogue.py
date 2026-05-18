from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QCheckBox,
)
from PySide6.QtCore import Qt
from ui.widgets.fonts import CustomFont # Import your font tool
from models.ssh_profile import SSHProfile
from core.profile_manager import *

from core.asset_path import get_asset_path

class ConnectionDialog(QWidget):
    def __init__(self, on_connect):
        super().__init__()

        self.on_connect = on_connect
        self.setWindowTitle("New Connection")

        self.objs_font = CustomFont(get_asset_path("ui/fonts/FROGBLOCK-V2.1-by-Polyducks.ttf"), size=12)
        pixel_font = self.objs_font.pixel_font

        self.title_font = CustomFont(get_asset_path("ui/fonts/BoldPixels.ttf"), size=30)
        title_font = self.title_font.pixel_font

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Header
        header = QLabel("NEW CONNECTION")
        header.setFont(title_font)
        header.setAlignment(Qt.AlignCenter)

        # Inputs
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Save Slot Name")
        self.name_input.setFont(pixel_font)

        self.host_input = QLineEdit()
        self.host_input.setPlaceholderText("Host")
        self.host_input.setFont(pixel_font)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFont(pixel_font)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(pixel_font)

        self.save_checkbox = QCheckBox("Save profile")
        self.save_checkbox.setFont(pixel_font)

        for widget in [self.name_input, self.host_input, self.username_input, self.password_input, self.save_checkbox]:
            widget.setFixedWidth(300)

        # Buttons
        self.connect_button = QPushButton("Connect")
        self.connect_button.setFont(pixel_font)
        self.connect_button.clicked.connect(self.connect_clicked)

        self.back_button = QPushButton("Cancel")
        self.back_button.setFont(pixel_font)


        layout.addWidget(header)
        layout.addSpacing(10)
        layout.addWidget(self.name_input)
        layout.addWidget(self.host_input)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.save_checkbox)
        layout.addSpacing(10)
        layout.addWidget(self.connect_button)
        layout.addWidget(self.back_button)
        
        self.setLayout(layout)

    def connect_clicked(self):
        if not self.host_input.text() or not self.username_input.text():
            print("Error: Host and Username are required!")
            return
        
        profile = SSHProfile(
            name=self.name_input.text(),
            host=self.host_input.text(),
            username=self.username_input.text(),
        )

        if self.save_checkbox.isChecked():
            profile_manager.save_profile(profile)

        self.on_connect(profile, self.password_input.text())