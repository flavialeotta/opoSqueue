from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)

from oposqueue.core.state_store import state_store


class JobQueuePanel(QWidget):
    def __init__(self):
        super().__init__()
        self.side_layout = QVBoxLayout()
        self.setLayout(self.side_layout)
        
        state_store.jobs_updated.connect(self.refresh)

    def refresh(self):
        while self.side_layout.count():
            child = self.side_layout.takeAt(0)
            if child.widget(): child.widget().deleteLater()

        for job in state_store.jobs:
            color = "#FFD700" if job.state == "RUNNING" else "#FFFFFF"
            
            # Build job info string with memory info if available
            job_info = f"[{job.job_id}] {job.user} | {job.runtime}"
            
            if job.allocated_memory:
                job_info += f" | {job.allocated_memory}MB"
            
            lbl = QLabel(job_info)
            lbl.setStyleSheet(f"color: {color}; font-size: 10px;")
            self.side_layout.addWidget(lbl)