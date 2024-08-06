from dataclasses import asdict, dataclass
from datetime import datetime
import json
import os
from pathlib import Path
from typing import List, Optional

from aboutlife.utils import printerr, get_data_path

LOG_FILE_NAME = "tasklog.json"

# log data structure


@dataclass
class Log:
    hour: str
    duration: int
    task: str


@dataclass
class LogCollection:
    date: str
    logs: List[Log]


def _get_log_file_path() -> Path:
    return Path(get_data_path()) / LOG_FILE_NAME


# blocking
def write_log(logs: List[Log]) -> bool:
    date = datetime.now().strftime("%Y-%m-%d")
    logs_col = LogCollection(date, logs)

    try:
        data = json.dumps(asdict(logs_col), indent=4)
        file_path = str(_get_log_file_path())
        printerr(f"I: writting log to {file_path}")

        # overwrite
        with open(file_path, "w") as file:
            file.write(data)
    except Exception as e:
        printerr(e)
    return False


def read_log() -> Optional[List[Log]]:
    date_current = datetime.now().strftime("%Y-%m-%d")
    file_path = str(_get_log_file_path())
    if not os.path.exists(file_path):
        return None

    try:
        # read and parse
        with open(file_path, "r") as file:
            json_data = json.load(file)
        logs_col = LogCollection(**json_data)

        # it's current
        if date_current != logs_col.date:
            return None

        # extract logs
        return logs_col.logs

    except Exception as e:
        printerr(e)

    return None


if __name__ == "__main__":
    date = datetime.now().strftime("%Y-%m-%d")
    hour = datetime.now().strftime("%I:%M %p")

    logs_col = LogCollection(date, [])
    for i in range(5):
        log = Log(hour, 10, "This is my tags")
        logs_col.logs.append(log)
    p_json_pretty = json.dumps(asdict(logs_col), indent=4)

    # print(date, " : ", hour)
    # print(asdict(logs_col))
    # print(p_json_pretty)

    # write_log(logs_col.logs)
    print(read_log())
