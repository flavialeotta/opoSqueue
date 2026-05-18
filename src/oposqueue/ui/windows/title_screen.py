from PySide6.QtWidgets import (
    QWidget, # blank window
    QVBoxLayout, # stacks element vertically
    QPushButton, # clickable buttons
    QLabel, # text
    QApplication,
)

from PySide6.QtCore import *
from PySide6.QtGui import QMovie
import asyncio
import os
import webbrowser

from oposqueue.ui.windows.connection_dialogue import ConnectionDialog
from oposqueue.ui.windows.save_select_screen import SaveSelectScreen
from oposqueue.core.ssh_manager import SSHManager
from oposqueue.core.polling_service import PollingService
from oposqueue.ui.windows.cluster_view import ClusterView
from oposqueue.ui.widgets.fonts import CustomFont

from core.asset_path import get_asset_path

# Title Screen is defined as a child of class QWidget
class TitleScreen(QWidget): 
    def __init__(self):
        # Overwrites the initialization of the QWidget class
        super().__init__()
        self.setStyleSheet("background-color: #2e2e2e; color: white;")

        # Set name of the window
        self.setWindowTitle("opoSqueue - HPC nodes view")

        # Initialize window layout
        layout = QVBoxLayout()

        self.title_font = CustomFont(get_asset_path("ui/fonts/BoldPixels.ttf"), size=50)
        self.objs_font = CustomFont(get_asset_path("ui/fonts/FROGBLOCK-V2.1-by-Polyducks.ttf"), size=12)

        # Add a title
        title = QLabel("opoSqueue")
        # ...and align it to the center
        title.setAlignment(Qt.AlignCenter)
        title.setFont(self.title_font.pixel_font)

        # Then define buttons
        
        # Check first if there are any connections saved:
        self.continue_button = QPushButton("Continue")
        self.continue_button.setFont(self.objs_font.pixel_font)

        profiles_dir = get_asset_path("storage/profiles")
        connections_saved = [f for f in os.listdir(profiles_dir) if f.endswith('.json')]
        
        if not connections_saved:
            self.continue_button.setVisible(False)
        
        self.new_game_button = QPushButton("New Connection")
        self.new_game_button.setFont(self.objs_font.pixel_font)
        self.documentation_button = QPushButton("Documentation")
        self.documentation_button.setFont(self.objs_font.pixel_font)
        self.exit_button = QPushButton("Exit")
        self.exit_button.setFont(self.objs_font.pixel_font)


        # What to do when buttons are clicked:
        self.continue_button.clicked.connect(self.open_save_select)
        self.new_game_button.clicked.connect(self.open_connection_dialog)
        self.documentation_button.clicked.connect(lambda: webbrowser.open("https://github.com/flavialeotta/opoSqueue/blob/main/README.md"))
        self.exit_button.clicked.connect(self.trigger_exit)



        # Create a label to hold the GIF
        self.gif_label = QLabel()
        self.gif_label.setAlignment(Qt.AlignCenter)

        # Load the movie
        self.movie = QMovie(get_asset_path("ui/sprites/opossum_sprite.gif"))
        # Scaler
        self.movie.setCacheMode(QMovie.CacheAll)

        self.movie.frameChanged.connect(lambda: self.gif_label.setPixmap(
            self.movie.currentPixmap().scaled(210, 210, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        ))
        self.gif_label.setMovie(self.movie) # sx top dx bottom
        self.gif_label.setContentsMargins(-30, -60, -70, -40)
        

        # Start the animation
        self.movie.start()

        layout.addWidget(title)
        layout.addWidget(title)
        layout.addWidget(self.gif_label)
        layout.addWidget(self.continue_button)
        layout.addWidget(self.new_game_button)
        layout.addWidget(self.documentation_button)
        layout.addWidget(self.exit_button)

        self.setLayout(layout)

        self.connection_dialog = None
        self.save_select_screen = None

        self.ssh = SSHManager()
        self.poller = None
        self.cluster_view = None

    def trigger_exit(self):
        QApplication.instance().quit()
    
    def open_connection_dialog(self):
        self.connection_dialog = ConnectionDialog(self.handle_connection)

    def open_save_select(self):
        pass

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