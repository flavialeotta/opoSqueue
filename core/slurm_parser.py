from models.job import Job
from models.node import Node

DELIMITER = "|"


def parse_squeue(raw: str):
    jobs = []
    lines = raw.strip().splitlines()

    for line in lines:
        parts = line.split(DELIMITER)

        if len(parts) != 9:
            continue

        jobs.append(
            Job(
                job_id=parts[0],
                partition=parts[1],
                name=parts[2],
                user=parts[3],
                state=parts[4],
                runtime=parts[5],
                nodes=parts[6],   # This will now be the node list (e.g., "node01")
                cpus=int(parts[7]),
                reason=parts[8],
            )
        )
    return jobs

def parse_sinfo(raw: str):
    nodes = []
    lines = raw.strip().splitlines()

    for line in lines:
        parts = line.split("|")
        if len(parts) != 4:
            continue

        # parts[3] is "Alloc/Idle/Other/Total" (e.g., "4/24/0/28")
        cpu_data = parts[3].split("/")
        
        nodes.append(
            Node(
                name=parts[0],
                partition=parts[1],
                state=parts[2],
                cpus_alloc=int(cpu_data[0]),
                cpus_total=int(cpu_data[3]),
            )
        )
    return nodes