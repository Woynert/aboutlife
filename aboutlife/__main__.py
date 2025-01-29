#!/usr/bin/env python
import sys
from pathlib import Path

# support to run as module or script
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

import argparse


def main():
    print("I: Booting")
    parser = argparse.ArgumentParser(description="Aboutlife")
    parser.add_argument(
        "--obfuscated", action="store_true", help="Launch main deamon obfuscated"
    )
    parser.add_argument("--daemononly", action="store_true", help="Run server only")
    parser.add_argument("--overlay", action="store_true", help="Launch overlay plugin")
    parser.add_argument("--sticky", action="store_true", help="Launch sticky plugin")
    args = parser.parse_args()

    if args.overlay:
        from aboutlife.overlay import overlay

        print("I: Launching overlay")
        overlay.main()

    elif args.sticky:
        from aboutlife.sticky import sticky

        print("I: Launching sticky")
        sticky.main()

    elif args.daemononly:
        from aboutlife import daemon

        print("I: Launching daemon server only")
        daemon.main(False)

    elif args.obfuscated:
        from aboutlife.launcher import launcher

        print("I: Launching daemon obfuscated")
        launcher.main()

    else:
        from aboutlife import daemon

        print("I: Launching aboutlife")
        daemon.main()


if __name__ == "__main__":
    main()
