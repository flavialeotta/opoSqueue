from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout


class NodeTile(QFrame):
    def __init__(self, node_name, status):
        super().__init__()

        self.setFixedSize(64, 64)

        layout = QVBoxLayout()

        icon = QLabel("■")
        label = QLabel(node_name)

        layout.addWidget(icon)
        layout.addWidget(label)

        self.setLayout(layout)

        status = status.lower()

        if "idle" in status:
            color = "#202020"

        elif "alloc" in status:
            color = "#E0E0E0"

        elif "mix" in status:
            color = "#909090"

        elif "down" in status:
            color = "#505050"

        else:
            color = "#707070"

        self.setStyleSheet(
            f'''
            background-color: {color};
            border: 2px solid #AAAAAA;
            '''
        )