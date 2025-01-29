def format_time_from_secs(seconds: int) -> str:
    sec = seconds % 60
    min = int((seconds - sec) / 60)
    return f"{str(min).zfill(2)}:{str(sec).zfill(2)}"
