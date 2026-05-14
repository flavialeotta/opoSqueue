import sys
import asyncio
from core.ssh_manager import SSHManager
from core.polling_service import PollingService
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QInputDialog, QLineEdit, QPushButton
from qasync import QEventLoop

# Import your screens
from ui.windows.title_screen import TitleScreen
# Make sure ConnectionDialog is updated to be a QWidget!
from ui.windows.connection_dialogue import ConnectionDialog 
from ui.windows.cluster_view import ClusterView
from ui.windows.save_select_screen import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("opoSqueue")
        self.resize(300, 300)

        # Apply the Dark Mode style to everything
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

        # Create screens
        self.title_screen = TitleScreen()
        self.conn_screen = ConnectionDialog(on_connect=self.handle_connection) 
        self.cluster_view = ClusterView()
        self.back_to_menu_btn = QPushButton("BACK TO MENU")
        self.save_select_screen = SaveSelectScreen(
            on_profile_selected=self.handle_saved_profile,
            on_back=lambda: self.stack.setCurrentIndex(0)
        )
        
        self.stack.addWidget(self.title_screen) # Index 0
        self.stack.addWidget(self.conn_screen)  # Index 1
        self.stack.addWidget(self.cluster_view)
        self.stack.addWidget(self.save_select_screen)# Index 3

        # Logic to switch pages
        self.title_screen.new_game_button.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.conn_screen.back_button.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.cluster_view.back_button.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.title_screen.continue_button.clicked.disconnect() # Clear existing dummy links
        self.title_screen.continue_button.clicked.connect(self.show_save_selection)

        self.ssh = SSHManager()
        self.poller = PollingService(self.ssh)


    def handle_connection(self, profile, password):
        print(f"Connecting to {profile.host} as {profile.username}...")
        asyncio.create_task(self.start_ssh_session(profile, password))

    def handle_saved_profile(self, profile):
        """This is called when a slot is clicked in SaveSelectScreen"""
        # Create a popup dialog for the password
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
        self.save_select_screen.reload_profiles() # This works now because save_select_screen exists here!
        self.stack.setCurrentIndex(3)

    async def start_ssh_session(self, profile, password):
        try:
            print(f"Attempting to connect to {profile.host}...")
            await self.ssh.connect(profile.host, profile.username, password)
            

            # If we reach here, connection was successful!
            print("Connected! Switching to Cluster View...")
            
            # 1. Start the poller (it runs in its own while loop)
            asyncio.create_task(self.poller.start())
            
            # 2. Switch the UI to the ClusterView (Index 2)
            self.stack.setCurrentIndex(2)
            
        except Exception as e:
            print(f"Connection Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # This setup handles the "Opossum" shutdown perfectly
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