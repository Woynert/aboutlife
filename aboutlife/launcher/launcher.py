import time
import subprocess
import time
import sys
import os
from aboutlife.overlay import client


POLLING_DELAY = 5  # seconds
bin_path = sys.argv[0]


def main():
    print("I: Launcher: Checking for graphical session")
    if not is_graphical_session():
        print("I: Launcher: Not a graphical session, exiting")
        sys.exit(1)

    while True:
        # try spawning

        print("I: Launcher: Polling for _daemon_")
        state = client.get_state()
        print(f"I: Launcher: got state '{state}'")

        if state is None:
            print("I: Launcher: launching _daemon_")
            process_cmd = [
                # systemd cgroup disowning spawn
                # extracted from https://stackoverflow.com/a/57041270
                "systemd-run",
                "--user",
                "--scope",
                "--slice=slice",
                # process disowning spawn
                # + Ensure normal user environment
                "/usr/bin/env",
                "bash",
                "-c",
                f"( nohup sh -c '{bin_path} &' >/tmp/aboutlife_obscure.log 2>&1 ) & ",
                # f"( nohup sh -c '{bin_path} &' >/dev/null 2>&1 ) & ",
                # f"{bin_path} & pid=$! ; echo \"pid $pid\"", # DEBUG
            ]
            process = subprocess.Popen(
                process_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True, # ensures output is returned as a string
            )
            stdout, stderr = process.communicate()
            print(f"I: Launcher: process return code {process.returncode}")
            print("Error:", stderr)
            print("Out:", stdout)

        time.sleep(POLLING_DELAY)


def is_graphical_session() -> bool:
    display = os.environ.get("DISPLAY")
    session_type = os.environ.get("XDG_SESSION_TYPE")
    return display is not None and session_type in {"x11", "wayland"}
