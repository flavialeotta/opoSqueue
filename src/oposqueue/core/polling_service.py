import asyncio

from oposqueue.core.state_store import state_store
from oposqueue.core.slurm_parser import parse_squeue, parse_sinfo



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

                state_store.update_jobs(jobs)
                state_store.update_nodes(nodes)
                

                print(f"Updated jobs: {len(jobs)}")

            except Exception as e:
                import traceback
                traceback.print_exc()

            await asyncio.sleep(5)

    def stop(self):
        self.running = False