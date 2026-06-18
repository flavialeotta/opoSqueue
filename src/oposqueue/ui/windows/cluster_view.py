from PySide6.QtWidgets import (
    QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, 
    QPushButton, QLineEdit, QLabel, QScrollArea, QSplitter
)
from PySide6.QtCore import Qt
from oposqueue.core.state_store import state_store
from oposqueue.ui.widgets.node_tile import NodeTile
from oposqueue.ui.widgets.fonts import CustomFont
from oposqueue.ui.widgets.job_queue_panel import JobQueuePanel
from oposqueue.core.asset_path import get_asset_path

class ClusterView(QWidget):
    def __init__(self):
        super().__init__()
        self.objs_font = CustomFont(get_asset_path("ui/fonts/FROGBLOCK-V2.1-by-Polyducks.ttf"), size=12)

        self.main_container = QVBoxLayout()
        self.main_container.setContentsMargins(10, 10, 10, 10)
        self.main_container.setSpacing(5)
        
        # Top Bar
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
        
        # FIX 1: Wrap the legend in a QWidget to prevent it from stretching vertically
        self.legend_widget = QWidget()
        self.legend_layout = self.create_legend()
        self.legend_widget.setLayout(self.legend_layout)
        self.legend_widget.setFixedHeight(25) # Hard lock its size!
        
        # Grid area for nodes
        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        self.grid.setAlignment(Qt.AlignTop)  
        self.grid.setSizeConstraint(QGridLayout.SetMinAndMaxSize)
        
        self.grid_widget = QWidget()
        self.grid_widget.setLayout(self.grid)
        self.grid_widget.setStyleSheet("background-color: #0a0a0a;")
        
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.grid_widget)
        self.scroll.setWidgetResizable(True)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setStyleSheet("background-color: #0a0a0a; border: none;")
        
        self.queue_panel = JobQueuePanel()

        # Splitter Layout Setup
        self.content_splitter = QSplitter(Qt.Horizontal)
        self.content_splitter.addWidget(self.scroll)            
        self.content_splitter.addWidget(self.queue_panel)   
        
        self.content_splitter.setStretchFactor(0, 3)
        self.content_splitter.setStretchFactor(1, 1)
        
        # Assemble Main Layout Component Elements
        self.main_container.addLayout(top_bar)
        self.main_container.addWidget(self.legend_widget) # Add as widget!
        self.main_container.addWidget(self.content_splitter) 
        
        self.setLayout(self.main_container)
        self.back_button.clicked.connect(self.handle_back_click)

        # Signals
        state_store.nodes_updated.connect(self.refresh)
        state_store.jobs_updated.connect(self.refresh)

    def handle_back_click(self):
        top_window = self.window()
        self.hide()
        
        if top_window:
            top_window.setMinimumSize(0, 0)
            top_window.setMaximumSize(16777215, 16777215)
            top_window.resize(580, 500) 
            
            if hasattr(top_window, 'title_screen') and top_window.title_screen:
                top_window.title_screen.show()
                
            top_window.adjustSize()

    # FIX 2: Dynamic resize handling without infinite recursion loops
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.refresh()

    def create_legend(self):
        legend = QHBoxLayout()
        legend.setContentsMargins(0, 0, 0, 0)
        items = [("■ IDLE", "#2ecc71"), ("■ ALLOC", "#e74c3c"), ("■ MIXED", "#f1c40f"), ("■ DOWN", "#7f8c8d")]
        for text, color in items:
            lbl = QLabel(text)
            lbl.setStyleSheet(f"color: {color}; font-weight: bold; margin-right: 15px; font-size: 10px;")
            legend.addWidget(lbl)
        legend.addStretch()
        return legend

    def refresh(self):
        # Prevent layout recalculation crashes if the view isn't fully built yet
        if not hasattr(self, 'scroll') or self.scroll is None:
            return

        # Temporarily block signals to stop recursion loops during grid drawing
        self.grid.invalidate()

        while self.grid.count():
            child = self.grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        target_user = self.filter_input.text().strip().lower()
        seen_nodes = set()
        
        # FIX 3: Safe, ironclad width calculations utilizing the scroll viewport bounds
        available_width = self.scroll.viewport().width()
        if available_width <= 100: 
            available_width = 600 # Clean default fallback value for initial launch step
            
        tile_width = 115 
        max_cols = max(1, available_width // tile_width)

        row, col = 0, 0
        for node in state_store.nodes:
            if node.name in seen_nodes:
                continue
            seen_nodes.add(node.name)

            unique_users = set()
            is_me = False
            job_id = ""
            allocated_memory = None
            memory_used = None
            memory_percent = None
            
            for job in state_store.jobs:
                if job.state == "RUNNING" and node.name in job.nodes:
                    unique_users.add(job.user)
                    job_id = job.job_id
                    allocated_memory = job.allocated_memory
                    memory_used = job.memory_used
                    memory_percent = job.memory_percent
                    
                    if target_user != "" and target_user in job.user.lower():
                        is_me = True

            node_user = ", ".join(unique_users) if unique_users else ""

            tile = NodeTile(
                node_name=node.name,
                status=node.state,
                allocated_cpus=getattr(node, 'cpus_alloc', 0), 
                total_cpus=node.cpus_total,
                user=node_user,
                is_highlighted=is_me,
                job_id=job_id,
                allocated_memory=allocated_memory,
                memory_used=memory_used,
                memory_percent=memory_percent
            )
            self.grid.addWidget(tile, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1