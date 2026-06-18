from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PySide6.QtCore import Qt
from oposqueue.core.state_store import state_store

class JobQueuePanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(180) 
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("background-color: #1a1a1a; border: none;")
        
        self.container_widget = QWidget()
        self.side_layout = QVBoxLayout(self.container_widget)
        self.side_layout.setContentsMargins(5, 5, 5, 5)
        
        self.scroll.setWidget(self.container_widget)
        self.main_layout.addWidget(self.scroll)
        


    def refresh(self, search_text=""):
        
        while self.side_layout.count():
            child = self.side_layout.takeAt(0)
            if child.widget(): 
                child.widget().deleteLater()

        clean_search = search_text.strip().lower()

        for job in state_store.jobs:
            # Check if this row matches our User name or Job ID search query
            is_match = False
            if clean_search:
                if clean_search in job.user.lower() or clean_search in str(job.job_id).lower():
                    is_match = True
            
            if is_match:
                color = "#00FFFF" 
            else:
                color = "#FFD700" if job.state == "RUNNING" else "#FFFFFF"
            
            job_info = f"[{job.job_id}] {job.user} | {job.runtime}"
            if job.allocated_memory:
                job_info += f" | {job.allocated_memory}MB"
            
            lbl = QLabel(job_info)
            
            
            bg_style = "background-color: #2c3e50;" if is_match else ""
            lbl.setStyleSheet(f"""
                color: {color}; 
                {bg_style}
                font-family: 'Consolas', 'Courier New', monospace; 
                font-size: 11px;
                font-weight: {'bold' if is_match else '500'};
                line-height: 1.2;
            """)
            lbl.setWordWrap(True) 
            self.side_layout.addWidget(lbl)
            
        self.side_layout.addStretch()