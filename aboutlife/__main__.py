import threading
import time
from typing import List
import argparse
from aboutlife.overlay import overlay
from aboutlife import daemon


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aboutlife")
    parser.add_argument("--overlay", action="store_true", help="Launch overlay plugin")
    args = parser.parse_args()

    if args.overlay:
        print("Launching overlay")
        overlay.main()

    else:
        daemon.main()
