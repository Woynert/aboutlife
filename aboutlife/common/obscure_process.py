import random
import psutil
import setproctitle


def get_random_process_name() -> str:
    processes = [
        proc.info["cmdline"]
        for proc in psutil.process_iter(attrs=["cmdline"])
        if proc.info["cmdline"] != None
        and len(proc.info["cmdline"]) > 0
        and "[" not in " ".join(proc.info["cmdline"])
    ]

    new_name = " ".join(random.choice(processes))
    return new_name


def obscure_process_name():
    setproctitle.setproctitle(get_random_process_name())
