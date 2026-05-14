from PySide6.QtWidgets import (
    QWidget, # blank window
    QVBoxLayout, # stacks element vertically
    QPushButton, # clickable buttons
    QLabel, # text
    QApplication,
)

from PySide6.QtCore import Qt # core elements
import asyncio
import os
import webbrowser

from ui.windows.connection_dialogue import ConnectionDialog
from ui.windows.save_select_screen import SaveSelectScreen
from core.ssh_manager import SSHManager
from core.polling_service import PollingService
from ui.windows.cluster_view import ClusterView
from ui.widgets.fonts import CustomFont

# Title Screen is defined as a child of class QWidget
class TitleScreen(QWidget): 
    def __init__(self):
        # Overwrites the initialization of the QWidget class
        super().__init__()
        self.should_exit = False

        # Set name of the window
        self.setWindowTitle("opoSqueue - HPC nodes view")

        # Initialize window layout
        layout = QVBoxLayout()

        self.title_font = CustomFont("ui/fonts/BoldPixels.ttf", size=50)
        self.objs_font = CustomFont("ui/fonts/FROGBLOCK-V2.1-by-Polyducks.ttf", size=12)

        # Add a title
        title = QLabel("opoSqueue")
        # ...and align it to the center
        title.setAlignment(Qt.AlignCenter)
        title.setFont(self.title_font.pixel_font)

        # Then define buttons
        
        # Check first if there are any connections saved:
        continue_button = QPushButton("Continue")
        continue_button.setFont(self.objs_font.pixel_font)
        connections_saved = [f for f in os.listdir("storage/profiles") if f.endswith('.json')]
        
        if not connections_saved:
            continue_button.setVisible(False)
        
        new_game_button = QPushButton("New Connection")
        new_game_button.setFont(self.objs_font.pixel_font)
        documentation_button = QPushButton("Documentation")
        documentation_button.setFont(self.objs_font.pixel_font)
        exit_button = QPushButton("Exit")
        exit_button.setFont(self.objs_font.pixel_font)


        # What to do when buttons are clicked:
        continue_button.clicked.connect(self.open_save_select)
        new_game_button.clicked.connect(self.open_connection_dialog)
        documentation_button.clicked.connect(lambda: webbrowser.open("README.md"))
        exit_button.clicked.connect(self.trigger_exit)

        layout.addWidget(title)
        layout.addWidget(continue_button)
        layout.addWidget(new_game_button)
        layout.addWidget(documentation_button)
        layout.addWidget(exit_button)

        self.setLayout(layout)

        # Keep references alive
        self.connection_dialog = None
        self.save_select_screen = None

        self.ssh = SSHManager()
        self.poller = None
        self.cluster_view = None

    def trigger_exit(self):
        self.should_exit = True
    
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