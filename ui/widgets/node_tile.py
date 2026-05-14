from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class NodeTile(QFrame):
    def __init__(self, node_name, status, allocated_cpus, total_cpus, user="---", is_highlighted=False):
        super().__init__()
        self.setFixedSize(95, 105) # Sized for readability
        layout = QVBoxLayout()
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(2)

        # 1. Node Name
        name_lbl = QLabel(node_name)
        name_lbl.setAlignment(Qt.AlignCenter)
        name_lbl.setStyleSheet("font-size: 10px; font-weight: bold; color: #EEE;")

        # 2. CPU Fraction (e.g., 4/64)
        cpu_lbl = QLabel(f"CPU: {allocated_cpus}/{total_cpus}")
        cpu_lbl.setAlignment(Qt.AlignCenter)
        cpu_lbl.setStyleSheet("font-size: 9px; color: #888;")

        # 3. Status Block
        self.icon = QLabel("■")
        self.icon.setAlignment(Qt.AlignCenter)
        self.icon.setStyleSheet(f"font-size: 32px; color: {self.get_color(status)};")

        # 4. Occupying User
        user_lbl = QLabel(user if user else "IDLE")
        user_lbl.setAlignment(Qt.AlignCenter)
        # If it's the current user, make the text Gold
        user_lbl.setStyleSheet(f"font-size: 9px; color: {'#FFD700' if is_highlighted else '#666'};")

        layout.addWidget(name_lbl)
        layout.addWidget(cpu_lbl)
        layout.addWidget(self.icon)
        layout.addWidget(user_lbl)
        self.setLayout(layout)

        # Highlight the whole frame if it's the user's node
        border = "2px solid #FFD700" if is_highlighted else "1px solid #333"
        self.setStyleSheet(f"QFrame {{ border: {border}; background: #111; border-radius: 4px; }}")

    def get_color(self, status):
        s = status.lower()
        if "idle" in s: return "#2ecc71" # Green
        if "alloc" in s: return "#e74c3c" # Red
        if "mix" in s: return "#f1c40f"   # Yellow
        return "#555" # Gray (Down)