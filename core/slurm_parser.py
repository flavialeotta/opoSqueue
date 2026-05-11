from models.job import Job
from models.node import Node

DELIMITER = "|"


def parse_squeue(raw: str):
    jobs = []

    lines = raw.strip().splitlines()

    for line in lines:
        parts = line.split(DELIMITER)

        if len(parts) != 8:
            continue

        jobs.append(
            Job(
                job_id=parts[0],
                partition=parts[1],
                name=parts[2],
                user=parts[3],
                state=parts[4],
                runtime=parts[5],
                nodes=int(parts[6]),
                reason=parts[7],
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

        nodes.append(
            Node(
                name=parts[0],
                partition=parts[1],
                state=parts[2],
                cpus_total=int(parts[3]),
            )
        )

    return nodes