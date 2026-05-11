from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
)

from PySide6.QtCore import Qt

from ui.windows.connection_dialogue import ConnectionDialog
from ui.windows.save_select_screen import SaveSelectScreen

import asyncio

from core.ssh_manager import SSHManager
from core.polling_service import PollingService
from ui.windows.cluster_view import ClusterView

class TitleScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HPC Quest")

        layout = QVBoxLayout()

        title = QLabel("HPC QUEST")
        title.setAlignment(Qt.AlignCenter)

        continue_button = QPushButton("Continue")
        new_game_button = QPushButton("New Connection")
        settings_button = QPushButton("Settings")

        continue_button.clicked.connect(self.open_save_select)
        new_game_button.clicked.connect(self.open_connection_dialog)

        layout.addWidget(title)
        layout.addWidget(continue_button)
        layout.addWidget(new_game_button)
        layout.addWidget(settings_button)

        self.setLayout(layout)

        # Keep references alive
        self.connection_dialog = None
        self.save_select_screen = None

        self.ssh = SSHManager()
        self.poller = None
        self.cluster_view = None

    def open_connection_dialog(self):
        self.connection_dialog = ConnectionDialog(self.handle_connection)
        self.connection_dialog.show()

    def open_save_select(self):
        self.save_select_screen = SaveSelectScreen(
            self.handle_saved_profile
        )
        self.save_select_screen.show()

    def handle_connection(self, profile, password):
        asyncio.create_task(
            self.connect_to_cluster(profile, password)
        )

    def handle_saved_profile(self, profile):
        print("Selected profile:", profile.name)

    async def connect_to_cluster(self, profile, password):
        try:
            await self.ssh.connect(
                host=profile.host,
                username=profile.username,
                password=password,
                port=profile.port,
            )

            print("SSH connected")

            self.poller = PollingService(self.ssh)

            asyncio.create_task(self.poller.start())

            self.cluster_view = ClusterView()
            self.cluster_view.resize(800, 600)
            self.cluster_view.show()

        except Exception as e:
            print("Connection failed:", e)