from PySide6.QtCore import QObject, Signal


class StateStore(QObject):
    jobs_updated = Signal()
    nodes_updated = Signal()

    def __init__(self):
        super().__init__()

        self.jobs = []
        self.nodes = []

    def update_jobs(self, jobs):
        self.jobs = jobs
        self.jobs_updated.emit()

    def update_nodes(self, nodes):
        self.nodes = nodes
        self.nodes_updated.emit()


state_store = StateStore()