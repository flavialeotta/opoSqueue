from pydantic import BaseModel
from typing import Optional


class Job(BaseModel):
    job_id: str
    partition: str
    name: str
    user: str
    state: str
    runtime: str
    nodes: str
    cpus: int
    reason: str
    allocated_memory: Optional[int] = None  # in MB
    memory_used: Optional[int] = None  # in MB (when available)
    memory_percent: Optional[float] = None  # percentage used