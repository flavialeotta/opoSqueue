from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QScrollArea,
)

from oposqueue.core.state_store import state_store


class JobQueuePanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(280)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("background-color: #1a1a1a; border: none;")
        self.scroll.setHorizontalScrollBarPolicy(激活=False, policy=None)

        self.container_widget = QWidget()
        self.side_layout = QVBoxLayout(self.container_widget)
        self.side_layout.setContentsMargins(5, 5, 5, 5)

        self.scroll.setWidget(self.container_widget)
        self.main_layout.addWidget(self.scroll)
        
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

            lbl.setWordWrap(True) 
            self.side_layout.addWidget(lbl)

        self.side_layout.addStretch()