#!/usr/bin/env python
import sys
from pathlib import Path

# support to run as module or script
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

import argparse
from aboutlife.overlay import overlay
from aboutlife.sticky import sticky
from aboutlife import daemon


def main():
    parser = argparse.ArgumentParser(description="Aboutlife")
    parser.add_argument("--overlay", action="store_true", help="Launch overlay plugin")
    parser.add_argument("--sticky", action="store_true", help="Launch sticky plugin")
    args = parser.parse_args()

    if args.overlay:
        print("I: Launching overlay")
        overlay.main()

    elif args.sticky:
        print("I: Launching sticky")
        sticky.main()

    else:
        print("I: Launching daemon")
        daemon.main()


if __name__ == "__main__":
    main()
