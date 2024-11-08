import os
import subprocess
from abc import ABC, abstractmethod


class Plugin(ABC):
    must_read_pid = False
    current_instance_pid = -1

    def setup(self):
        pass

    # runs every tick
    @abstractmethod
    def process(self):
        pass

    # frees resources on exit
    @abstractmethod
    def cleanup():
        pass

    # spawns new process if pid is not alive
    def spawn_if_pid_is_dead(self, pid_path: str, command: str):
        try:
            # read pid

            if self.must_read_pid:
                pid = -1
                with open(pid_path, "r") as f:
                    pid = int(f.read().strip())
                self.must_read_pid = False
                self.current_instance_pid = pid

            if is_pid_alive(self.current_instance_pid):
                return

            # spawn instance, then save and read pid to keep track of it

            process_cmd = [
                "bash",
                "-c",
                f'( ({command} & pid=$! ; echo "$pid" > {pid_path} ) ) & ',
            ]
            process = subprocess.Popen(process_cmd)
            process.wait()
            self.must_read_pid = True

        except Exception as e:
            self.must_read_pid = False
            self.current_instance_pid = -1
            raise e


def is_pid_alive(pid):
    if pid < 0:
        return False
    try:
        # doesn't kill it, just checks
        os.kill(pid, 0)
    except OSError:
        return False
    return True
