import asyncssh


class SSHManager:
    def __init__(self):
        self.connection = None

    async def connect(self, host, username, password, port=22):
        self.connection = await asyncssh.connect(
            host,
            username=username,
            password=password,
            port=port,
            known_hosts=None,
        )

    async def run_command(self, command: str) -> str:
        result = await self.connection.run(command)
        return result.stdout

    async def disconnect(self):
        if self.connection:
            self.connection.close()