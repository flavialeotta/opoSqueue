import asyncio

from oposqueue.core.state_store import state_store
from oposqueue.core.slurm_parser import parse_squeue, parse_sinfo, parse_scontrol_job_memory, parse_sstat_maxrss



class PollingService:
    def __init__(self, ssh_manager):
        self.ssh = ssh_manager
        self.running = False

    async def start(self):
        self.running = True

        while self.running:
            try:
                raw_jobs = await self.ssh.run_command("squeue --noheader --format='%i|%P|%j|%u|%T|%M|%N|%C|%R'")
                raw_nodes = await self.ssh.run_command("sinfo -N --noheader -o '%N|%P|%T|%C'")

                jobs = parse_squeue(raw_jobs)
                nodes = parse_sinfo(raw_nodes)

                # Fetch memory information for each running job
                for job in jobs:
                    if job.state in ["RUNNING", "COMPLETING"]:
                        try:
                            scontrol_output = await self.ssh.run_command(f"scontrol show job {job.job_id}")
                            memory_info = parse_scontrol_job_memory(scontrol_output)
                            job.allocated_memory = memory_info["allocated_memory"]

                            job.memory_used = None
                            for sstat_target in (f"{job.job_id}.batch", job.job_id):
                                try:
                                    cmd = f"sstat -j {sstat_target} -o MaxRSS -n"
                                    sstat_output = await self.ssh.run_command(cmd)
                                    used_mb = parse_sstat_maxrss(sstat_output)
                                    if used_mb:
                                        job.memory_used = used_mb
                                        break
                                except Exception:
                                    continue

                            if job.memory_used and job.allocated_memory:
                                job.memory_percent = round(job.memory_used / job.allocated_memory * 100, 1)
                            else:
                                job.memory_percent = None
                        except Exception as e:
                            print(f"Failed to fetch memory info for job {job.job_id}: {e}")
                            import traceback
                            traceback.print_exc()

                state_store.update_jobs(jobs)
                state_store.update_nodes(nodes)
                

                print(f"Updated jobs: {len(jobs)}")

            except Exception as e:
                import traceback
                traceback.print_exc()

            await asyncio.sleep(5)

    def stop(self):
        self.running = False