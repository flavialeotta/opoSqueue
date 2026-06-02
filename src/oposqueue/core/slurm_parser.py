from oposqueue.models.job import Job
from oposqueue.models.node import Node

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


def parse_scontrol_job_memory(raw: str):
    """
    Parse scontrol show job output to extract memory information.
    Returns a dict with allocated_memory (in MB) and memory_used if available.
    """
    memory_info = {
        "allocated_memory": None,
        "memory_used": None,
        "memory_percent": None,
    }
    
    lines = raw.strip().splitlines()
    
    for line in lines:
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        # Parse TRES (Trackable RESources) fields - format: cpu=4,mem=8192M,node=1
        if key in ["AllocTRES", "ReqTRES"] and memory_info["allocated_memory"] is None:
            tres_parts = value.split(",")
            for part in tres_parts:
                if "=" in part:
                    tres_key, tres_val = part.split("=", 1)
                    tres_key = tres_key.strip()
                    tres_val = tres_val.strip()
                    if tres_key == "mem":
                        allocated_mb = _convert_memory_to_mb(tres_val)
                        if allocated_mb:
                            memory_info["allocated_memory"] = allocated_mb
                            break

        # Fallback to individual memory fields if TRES doesn't have it
        elif key in ["MinMemoryNode", "MaxMemory", "MemoryPerNode", "Memory", "ReqMem"] and memory_info["allocated_memory"] is None:
            if key == "MinMemoryNode" and ":" in value:
                mem_part = value.split(":")[-1]
                allocated_mb = _convert_memory_to_mb(mem_part)
                if allocated_mb:
                    memory_info["allocated_memory"] = allocated_mb
            else:
                allocated_mb = _convert_memory_to_mb(value)
                if allocated_mb:
                    memory_info["allocated_memory"] = allocated_mb
    
    return memory_info


def parse_sstat_maxrss(raw: str) -> int:
    """
    Parse sstat output for MaxRSS to obtain memory used in MB.
    """
    lines = [line.strip() for line in raw.strip().splitlines() if line.strip()]
    for line in lines:
        if line.lower().startswith("maxrss"):
            continue
        # If pipe-separated output is used, MaxRSS should be the last field.
        parts = line.split("|")
        candidate = parts[-1].strip() if len(parts) > 1 else line.strip()
        if candidate.lower() in ("unknown", "n/a", "-"):
            continue
        memory_mb = _convert_memory_to_mb(candidate)
        if memory_mb:
            return memory_mb
    return None


def _convert_memory_to_mb(memory_str: str) -> int:
    """
    Convert memory string (like "8000M", "8G", "500") to MB.
    Returns None if conversion fails.
    """
    if not memory_str:
        return None
    
    memory_str = memory_str.strip().upper()
    
    try:
        if memory_str.endswith("G"):
            return int(float(memory_str[:-1]) * 1024)
        elif memory_str.endswith("M"):
            return int(memory_str[:-1])
        elif memory_str.endswith("K"):
            return int(float(memory_str[:-1]) / 1024)
        elif memory_str.endswith("T"):
            return int(float(memory_str[:-1]) * 1024 * 1024)
        else:
            # Assume MB if no unit specified
            return int(memory_str)
    except (ValueError, IndexError):
        return None