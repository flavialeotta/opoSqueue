from pydantic import BaseModel


class SSHProfile(BaseModel):
    name: str
    host: str
    username: str
    port: int = 22