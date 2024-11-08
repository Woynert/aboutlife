import time
import subprocess
import time
import sys
from aboutlife.overlay import client


POLLING_DELAY = 3  # seconds
bin_path = sys.argv[0]


def main():
    while True:
        # handle requests

        print("I: Launcher: Polling for _daemon_")
        time.sleep(POLLING_DELAY)

        # spawn new daemon if time expires

        if client.get_state() == None:
            process_cmd = [
                "bash",
                "-c",
                f"( nohup sh -c '{bin_path} &' >/dev/null 2>&1 ) & ",
                # f"{bin_path} & pid=$! ; echo \"pid $pid\"", # DEBUG
            ]
            process = subprocess.Popen(process_cmd)
            process.wait()
