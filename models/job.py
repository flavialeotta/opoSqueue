from pydantic import BaseModel


class Job(BaseModel):
    job_id: str
    partition: str
    name: str
    user: str
    state: str
    runtime: str
    nodes: str  # Changed from int to str to hold node names like "node01"
    cpus: int   # Add this to track resource usage
    reason: str