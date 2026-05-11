from pydantic import BaseModel


class Node(BaseModel):
    name: str
    partition: str
    state: str
    cpus_total: int