from PySide6.QtWidgets import (
    QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, 
    QPushButton, QLineEdit, QLabel, QScrollArea
)
from PySide6.QtCore import Qt
from core.state_store import state_store
from ui.widgets.node_tile import NodeTile
from ui.widgets.fonts import CustomFont
from ui.widgets.job_queue_panel import JobQueuePanel

class ClusterView(QWidget):
    def __init__(self):
        super().__init__()
        self.objs_font = CustomFont("ui/fonts/FROGBLOCK-V2.1-by-Polyducks.ttf", size=12)

        self.main_container = QVBoxLayout()
        
        # Top Bar (Back Button + User Search/Filter)
        top_bar = QHBoxLayout()
        self.back_button = QPushButton("BACK")
        self.back_button.setFont(self.objs_font.pixel_font)
        self.back_button.setFixedWidth(80)
        
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Search User to highlight nodes...")
        self.filter_input.setFont(self.objs_font.pixel_font)
        self.filter_input.textChanged.connect(self.refresh)
        
        top_bar.addWidget(self.back_button)
        top_bar.addWidget(self.filter_input)
        
        # Legend
        self.legend_layout = self.create_legend()
        
        content_layout = QHBoxLayout()
        
        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        
        grid_widget = QWidget()
        grid_widget.setLayout(self.grid)
        
        scroll = QScrollArea()
        scroll.setWidget(grid_widget)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: #0a0a0a; border: none;")
        
        self.queue_panel = JobQueuePanel()

        content_layout.addWidget(scroll, 3)
        content_layout.addWidget(self.queue_panel, 1)
        
        # Main Layout
        self.main_container.addLayout(top_bar)
        self.main_container.addLayout(self.legend_layout)
        self.main_container.addLayout(content_layout)
        
        self.setLayout(self.main_container)

        # Signals
        state_store.nodes_updated.connect(self.refresh)
        state_store.jobs_updated.connect(self.refresh)

    def create_legend(self):
        legend = QHBoxLayout()
        items = [("■ IDLE", "#2ecc71"), ("■ ALLOC", "#e74c3c"), ("■ MIXED", "#f1c40f"), ("■ DOWN", "#7f8c8d")]
        for text, color in items:
            lbl = QLabel(text)
            lbl.setStyleSheet(f"color: {color}; font-weight: bold; margin-right: 15px; font-size: 10px;")
            legend.addWidget(lbl)
        legend.addStretch()
        return legend

    def refresh(self):
        while self.grid.count():
            child = self.grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        target_user = self.filter_input.text().strip().lower()
        

        seen_nodes = set()
        
        row, col = 0, 0
        for node in state_store.nodes:
            if node.name in seen_nodes:
                continue
            seen_nodes.add(node.name)

            
            node_user = ""
            is_me = False
            
            for job in state_store.jobs:
                if job.state == "RUNNING" and node.name in job.nodes:
                    node_user = job.user
                    if target_user != "" and target_user in job.user.lower():
                        is_me = True
                    break 

            tile = NodeTile(
                node_name=node.name,
                status=node.state,
                allocated_cpus=getattr(node, 'cpus_alloc', 0), 
                total_cpus=node.cpus_total,
                user=node_user,
                is_highlighted=is_me
            )
            self.grid.addWidget(tile, row, col)
            
            col += 1
            if col > 7:
                col = 0
                row += 1
        