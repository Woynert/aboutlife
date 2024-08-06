from dataclasses import asdict, dataclass
from datetime import datetime
import json
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


def write_log(logs: List[Log]) -> bool:
    date = datetime.now().strftime("%Y-%m-%d")
    logs_col = LogCollection(date, logs)

    try:
        data = json.dumps(asdict(logs_col), indent=4)
        file_path = str(Path(get_data_path()) / LOG_FILE_NAME)
        printerr(f"I: writting log to {file_path}")

        # overwrite
        with open(file_path, "w") as file:
            file.write(data)
    except Exception as e:
        print(e)
    return False


def read_log() -> Optional[List[Log]]:
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

    write_log(logs_col.logs)
