import subprocess


def send_notification(title: str, message: str):
    if title == "":
        subprocess.run(["notify-send", "-r", "108", "-t", "1000", message])
    else:
        subprocess.run(["notify-send", "-r", "108", "-t", "1000", title, message])
