from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from core.profile_manager import profile_manager
from ui.widgets.save_slot_widget import SaveSlotWidget
from ui.widgets.fonts import CustomFont
from core.asset_path import get_asset_path

class SaveSelectScreen(QWidget):
    def __init__(self, on_profile_selected, on_back):
        super().__init__()
        self.on_profile_selected = on_profile_selected
        self.on_back = on_back
        self.objs_font = CustomFont(get_asset_path("ui/fonts/FROGBLOCK-V2.1-by-Polyducks.ttf"), size=12)
        
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        self.reload_profiles()

    def reload_profiles(self):
        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        top_bar = QHBoxLayout()
        back_btn = QPushButton("< BACK")
        back_btn.setFont(self.objs_font.pixel_font)
        back_btn.setFixedWidth(100)
        back_btn.clicked.connect(self.on_back)
        
        title = QLabel("CHOOSE A SAVE SLOT")
        title.setFont(self.objs_font.pixel_font)
        title.setAlignment(Qt.AlignCenter)
        
        top_bar.addWidget(back_btn)
        top_bar.addStretch() 
        top_bar.addWidget(title)
        top_bar.addStretch() 
        
        self.main_layout.addLayout(top_bar)

        profiles = profile_manager.load_profiles()
        
        if not profiles:
            empty_msg = QLabel("No saved connections found.")
            empty_msg.setFont(self.objs_font.pixel_font) 
            empty_msg.setAlignment(Qt.AlignCenter)
            self.main_layout.addWidget(empty_msg)
        else:
            for profile in profiles:
                slot = SaveSlotWidget(profile, self.on_profile_selected)
                self.main_layout.addWidget(slot)
        
        self.main_layout.addStretch()