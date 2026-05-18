from pydantic import BaseModel


class Node(BaseModel):
    name: str
    partition: str
    state: str
    cpus_alloc: int
    cpus_total: int