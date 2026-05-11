from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QHBoxLayout,
)

from core.state_store import state_store
from ui.widgets.node_tile import NodeTile


class ClusterView(QWidget):
    def __init__(self):
        super().__init__()
        from ui.widgets.job_queue_panel import JobQueuePanel

        main_layout = QHBoxLayout()
        self.grid = QGridLayout()

        queue_panel = JobQueuePanel()

        main_layout.addLayout(self.grid, 3)
        main_layout.addWidget(queue_panel, 1)

        self.setLayout(main_layout)

        state_store.jobs_updated.connect(self.refresh)

    def refresh(self):
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()

            if widget:
                widget.deleteLater()

        row = 0
        col = 0

        for node in state_store.nodes:
            tile = NodeTile(
                node_name=node.name,
                status=node.state,
            )

            self.grid.addWidget(tile, row, col)

            col += 1

            if col > 7:
                col = 0
                row += 1