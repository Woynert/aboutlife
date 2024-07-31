from typing import Optional


def get_file_line_count(file_path) -> Optional[int]:
    try:
        with open(file_path, "rb") as f:
            return sum(1 for _ in f)
    except Exception:
        pass
    return None


def read_file_line(file_path, line_number) -> Optional[str]:
    try:
        with open(file_path, "r") as file:
            for current_line_number, line in enumerate(file, start=1):
                if current_line_number == line_number:
                    return line.strip()
    except Exception:
        pass
    return None
