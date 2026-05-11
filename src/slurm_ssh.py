import paramiko

class SlurmClient:
    def __init__(self, host, user, pwd):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.client = None

    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.host, username=self.user, password=self.pwd)

    def get_node_status(self):
        # sinfo gives us: NodeName, State (e.g., idle, alloc, down)
        stdin, stdout, stderr = self.client.exec_command("sinfo --format='%n %t' --noheader")
        output = stdout.read().decode()
        
        nodes = []
        for line in output.strip().split('\n'):
            name, state = line.split()
            nodes.append({"name": name, "state": state})
        return nodes