import os
import requests
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from aboutlife.utils import get_resource_path, get_data_path

IMAGE_LIST_PATH = "overlay/imagefeed/images.txt"


def _download_image(url: str, save_path: str) -> bool:
    try:
        # Send a GET request to the URL
        response = requests.get(url, stream=True)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Open the file in binary write mode
            with open(save_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return True
    except Exception:
        pass
    return False


def _get_file_line_count(file_path) -> Optional[int]:
    try:
        with open(file_path, "rb") as f:
            return sum(1 for _ in f)
    except Exception:
        pass
    return None


def _read_file_line(file_path, line_number) -> Optional[str]:
    try:
        with open(file_path, "r") as file:
            for current_line_number, line in enumerate(file, start=1):
                if current_line_number == line_number:
                    return line.strip()
    except Exception:
        pass
    return None


"""
Picks a random URL from a text file
"""


def _pick_random_image() -> Optional[str]:
    image_list_path = Path(get_resource_path()) / IMAGE_LIST_PATH
    print(image_list_path)
    if not os.path.exists(image_list_path):
        return None

    list_length = _get_file_line_count(image_list_path)
    if not list_length:
        return None

    line_number = random.randint(0, list_length)
    return _read_file_line(image_list_path, line_number)


def get_image_of_the_day() -> Optional[str]:
    date: str = datetime.now().strftime("%Y-%m-%d")
    image_name: str = f"aboutlife-{date}.jpg"

    # today's image already exists?

    path: Path = Path(get_data_path()) / image_name
    if os.path.exists(path):
        return str(path)

    # doesn't exist -> pick a random one and try to download it

    image_url = _pick_random_image()
    if image_url:
        if _download_image(image_url, str(path)):
            return str(path)

    # failed. Let's try to reuse the one from yesterday (if exists)

    date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    image_name = f"aboutlife-{date}.jpg"
    path = Path(get_data_path()) / image_name
    if os.path.exists(path):
        return str(path)

    return None


if __name__ == "__main__":
    print(get_image_of_the_day())
