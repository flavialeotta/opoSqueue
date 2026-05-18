from pydantic import BaseModel


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