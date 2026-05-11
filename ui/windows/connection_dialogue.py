from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QCheckBox,
)

from models.ssh_profile import SSHProfile
from core.profile_manager import profile_manager


class ConnectionDialog(QWidget):
    def __init__(self, on_connect):
        super().__init__()

        self.on_connect = on_connect

        self.setWindowTitle("New Connection")

        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Save Slot Name")

        self.host_input = QLineEdit()
        self.host_input.setPlaceholderText("Host")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.save_checkbox = QCheckBox("Save profile")

        connect_button = QPushButton("Connect")
        connect_button.clicked.connect(self.connect_clicked)

        layout.addWidget(QLabel("=== NEW CONNECTION ==="))
        layout.addWidget(self.name_input)
        layout.addWidget(self.host_input)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.save_checkbox)
        layout.addWidget(connect_button)

        self.setLayout(layout)

    def connect_clicked(self):
        profile = SSHProfile(
            name=self.name_input.text(),
            host=self.host_input.text(),
            username=self.username_input.text(),
        )

        if self.save_checkbox.isChecked():
            profile_manager.save_profile(profile)

        self.on_connect(profile, self.password_input.text())