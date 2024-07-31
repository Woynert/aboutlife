import os
import random
from pathlib import Path
from typing import Optional
from aboutlife.utils import get_resource_path
from aboutlife.overlay.feed.common import get_file_line_count, read_file_line

QUOTE_LIST_PATH = "overlay/feed/quotes.txt"


"""
Picks a random URL from a text file
"""


def get_random_quote() -> Optional[str]:
    image_list_path = Path(get_resource_path()) / QUOTE_LIST_PATH
    if not os.path.exists(image_list_path):
        return None

    list_length = get_file_line_count(image_list_path)
    if not list_length:
        return None

    line_number = random.randint(0, list_length)
    return read_file_line(image_list_path, line_number)


if __name__ == "__main__":
    print(get_random_quote())
