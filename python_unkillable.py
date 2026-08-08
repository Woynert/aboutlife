#!/usr/bin/env python3

import os
import shutil
import subprocess
import tempfile
import uuid
import random
import time
import psutil  # pip install psutil

import sys
import setproctitle
from typing import List


# Check if binary exists
def find_executable(binary_name):
    binary_path = shutil.which(binary_name)
    if binary_path is None:
        raise FileNotFoundError(f"Executable '{binary_name}' not found.")
    return binary_path


# Create symlink in a random temporary folder
def create_symlink_in_random_temp(binary_path):
    # Choose a random temporary directory
    rootdir = random.choice(["/tmp", "/dev/shm"])
    workdir = os.path.join(rootdir, str(uuid.uuid4()))
    os.makedirs(workdir, exist_ok=True)

    # Create a symlink with a random name
    symlink_path = os.path.join(workdir, str(uuid.uuid4()))
    os.symlink(binary_path, symlink_path)
    return symlink_path, workdir


# Get a random process name (excluding system process names containing '[')
def get_random_process_name():
    processes = [
        proc.info["cmdline"]
        for proc in psutil.process_iter(attrs=["cmdline"])
        if proc.info["cmdline"] != None
        and len(proc.info["cmdline"]) > 0
        and "[" not in " ".join(proc.info["cmdline"])
    ]

    return " ".join(random.choice(processes))


# Launch the binary with a custom process name
def launch_with_custom_name(command: List[str], procname):
    # Launch a subprocess with a specified process name
    # command = f"exec -a '{procname}' {symlink_path} --preferences"
    # subprocess.Popen(['bash', '-c', command])
    print("Now launching : " + command + " : " + procname)
    setproctitle.setproctitle(procname)
    subprocess.run(command)

    # setproctitle(argv[1])
    # run(argv[2:])


# Cleanup symlink and workdir
def cleanup_paths(symlink_path, workdir):
    try:
        os.remove(symlink_path)
        os.rmdir(workdir)
    except Exception as e:
        print(f"Cleanup error: {e}")


def main(binary_name):
    # 1: Check if binary exists.
    binary_path = find_executable(binary_name)

    # 2: Create symlink in a random temp folder.
    symlink_path, workdir = create_symlink_in_random_temp(binary_path)
    print("Symlink path:", symlink_path)
    print("Working directory:", workdir)
    print("Contents:", os.listdir(workdir))

    # 3: Get a random process name.
    procname = get_random_process_name()
    print("Chosen process name:", procname)

    # 4: Launch the binary with a custom process name.
    launch_with_custom_name(symlink_path, procname)

    # 5: Remove symlink and workdir after a delay.
    time.sleep(1)
    cleanup_paths(symlink_path, workdir)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python script.py <binary_name>")
        sys.exit(1)
    main(sys.argv[1])
