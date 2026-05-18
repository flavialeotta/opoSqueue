from PySide6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QLabel
from oposqueue.ui.widgets.fonts import CustomFont
from oposqueue.core.profile_manager import *
from oposqueue.core.asset_path import get_asset_path

class SaveSlotWidget(QFrame):
    def __init__(self, profile, on_connect):
        super().__init__()
        layout = QHBoxLayout()
        font = CustomFont(get_asset_path("ui/fonts/FROGBLOCK-V2.1-by-Polyducks.ttf"), size=10).pixel_font
        
        name_lbl = QLabel(f"{profile.name} ({profile.host})")
        name_lbl.setFont(font)
        
        connect_btn = QPushButton("CONNECT")
        connect_btn.setFont(font)
        connect_btn.clicked.connect(lambda: on_connect(profile))
        
        delete_btn = QPushButton("DEL")
        delete_btn.setFont(font)
        delete_btn.setStyleSheet("color: red;")
        delete_btn.clicked.connect(lambda: self.delete_this(profile))
        
        layout.addWidget(name_lbl, 1) # Takes up space
        layout.addWidget(connect_btn)
        layout.addWidget(delete_btn)
        self.setLayout(layout)
        self.setStyleSheet("border-bottom: 1px solid #333; padding: 5px;")

    def delete_this(self, profile):
        profile_manager.delete_profile(profile.name)
        # Work in progres...