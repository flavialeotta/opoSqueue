import os
import sys
import asyncio
from core.ssh_manager import SSHManager
from core.polling_service import PollingService
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QInputDialog, QLineEdit, QPushButton
from qasync import QEventLoop

from ui.windows.title_screen import TitleScreen
from ui.windows.connection_dialogue import ConnectionDialog 
from ui.windows.cluster_view import ClusterView
from ui.windows.save_select_screen import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("opoSqueue")
        self.resize(300, 300)

        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #2e2e2e;
                color: #ffffff;
            }
            QLineEdit {
                background-color: #1e1e1e;
                color: #00ff00;
                border: 1px solid #444;
                padding: 5px;
                font-family: 'Consolas', monospace;
            }
            QPushButton {
                background-color: #4a4a4a;
                border: 1px solid #666;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #5a5a5a;
            }
        """)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.title_screen = TitleScreen()
        self.conn_screen = ConnectionDialog(on_connect=self.handle_connection) 
        self.cluster_view = ClusterView()
        self.back_to_menu_btn = QPushButton("BACK TO MENU")
        self.save_select_screen = SaveSelectScreen(
            on_profile_selected=self.handle_saved_profile,
            on_back=lambda: self.stack.setCurrentIndex(0)
        )
        
        self.stack.addWidget(self.title_screen)
        self.stack.addWidget(self.conn_screen)
        self.stack.addWidget(self.cluster_view)
        self.stack.addWidget(self.save_select_screen)

        # Logic to switch pages
        self.title_screen.new_game_button.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.conn_screen.back_button.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.cluster_view.back_button.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.title_screen.continue_button.clicked.disconnect()
        self.title_screen.continue_button.clicked.connect(self.show_save_selection)

        self.ssh = SSHManager()
        self.poller = PollingService(self.ssh)


    def handle_connection(self, profile, password):
        print(f"Connecting to {profile.host} as {profile.username}...")
        asyncio.create_task(self.start_ssh_session(profile, password))

    def handle_saved_profile(self, profile):
        """This is called when a slot is clicked in SaveSelectScreen"""
        app = QApplication.instance()
        app.setFont(self.title_screen.objs_font.pixel_font)
        password, ok = QInputDialog.getText(
            self, "Security Check", 
            f"Password for {profile.username}:", 
            QLineEdit.Password
        )
        if ok and password:
            asyncio.create_task(self.start_ssh_session(profile, password))

    def show_save_selection(self):
        self.save_select_screen.reload_profiles()
        self.stack.setCurrentIndex(3)

    async def start_ssh_session(self, profile, password):
        try:
            print(f"Attempting to connect to {profile.host}...")
            await self.ssh.connect(profile.host, profile.username, password)
            
            print("Connected! Switching to Cluster View...")
            
            asyncio.create_task(self.poller.start())
            
            self.stack.setCurrentIndex(2)
            
        except Exception as e:
            print(f"Connection Error: {e}")


def main():
    app = QApplication(sys.argv)

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    main_window = MainWindow()
    main_window.show()

    try:
        with loop:
            loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("Opossum is going to sleep. Goodbye!")


if __name__ == "__main__":
    main()