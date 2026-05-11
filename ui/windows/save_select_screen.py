from PySide6.QtWidgets import QWidget, QVBoxLayout

from core.profile_manager import profile_manager
from ui.widgets.save_slot_widget import SaveSlotWidget


class SaveSelectScreen(QWidget):
    def __init__(self, on_profile_selected):
        super().__init__()

        layout = QVBoxLayout()

        profiles = profile_manager.load_profiles()

        for profile in profiles:
            widget = SaveSlotWidget(profile, on_profile_selected)
            layout.addWidget(widget)

        self.setLayout(layout)