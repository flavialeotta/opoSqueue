from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)

from core.state_store import state_store


class JobQueuePanel(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.setLayout(self.layout)

        state_store.jobs_updated.connect(self.refresh)

    def refresh(self):
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()

            if widget:
                widget.deleteLater()

        queued_jobs = [
            job for job in state_store.jobs
            if "PENDING" in job.state
        ]

        title = QLabel("QUEUED JOBS")

        self.layout.addWidget(title)

        for job in queued_jobs:
            label = QLabel(
                f"{job.name} ({job.user})"
            )

            self.layout.addWidget(label)