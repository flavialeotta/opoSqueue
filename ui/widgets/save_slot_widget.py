from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout


class SaveSlotWidget(QFrame):
    def __init__(self, profile, on_click):
        super().__init__()

        self.profile = profile
        self.on_click = on_click

        self.setFixedHeight(96)

        self.setStyleSheet(
            """
            QFrame {
                background-color: #111111;
                border: 2px solid #AAAAAA;
            }
            """
        )

        layout = QVBoxLayout()

        display_name = profile.name if profile.name else profile.host

        title = QLabel(display_name)
        subtitle = QLabel(profile.username)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.setLayout(layout)

    def mousePressEvent(self, event):
        self.on_click(self.profile)