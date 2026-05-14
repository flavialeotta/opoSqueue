from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)

from core.state_store import state_store


class JobQueuePanel(QWidget):
    def __init__(self):
        super().__init__()
        # Use a name other than self.layout!
        self.side_layout = QVBoxLayout()
        self.setLayout(self.side_layout)
        
        # Connect to the store
        state_store.jobs_updated.connect(self.refresh)

    def refresh(self):
        # Clear existing labels
        while self.side_layout.count():
            child = self.side_layout.takeAt(0)
            if child.widget(): child.widget().deleteLater()

        # Add the jobs with their runtimes
        for job in state_store.jobs:
            color = "#FFD700" if job.state == "RUNNING" else "#FFFFFF"
            lbl = QLabel(f"[{job.job_id}] {job.user} | {job.runtime}")
            lbl.setStyleSheet(f"color: {color}; font-size: 10px;")
            self.side_layout.addWidget(lbl)