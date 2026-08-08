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
    parser.add_argument("--tray", action="store_true", help="Launch X11 tray plugin")
    parser.add_argument("--autoshutdown", action="store_true", help="Run autoshutdown plugin")
    parser.add_argument("-p", "--port", help="Custom daemon port (debug)", default=0, type=int)
    args = parser.parse_args()

    if args.port != 0:
        from aboutlife.context import Context
        Context.set_rest_port(args.port)
        print("I: Using custom port", args.port)

    if args.overlay:
        from aboutlife.overlay import overlay
        print("I: Launching overlay")
        overlay.main()

    elif args.sticky:
        from aboutlife.sticky import sticky
        print("I: Launching sticky")
        sticky.main()

    elif args.tray:
        from aboutlife.tray import tray
        print("I: Launching X11 tray icon")
        tray.main()

    elif args.autoshutdown:
        from aboutlife.autoshutdown import autoshutdown
        print("I: Launching Auto shutdown plugin")
        autoshutdown.main()

    elif args.daemononly:
        from aboutlife import daemon
        print("I: Launching daemon server only")
        daemon.main(False)

    elif args.obfuscated:
        # Note: This name is incorrect, it should be 'launcher'. The only
        # thing this does is to launch a disowned instance. The actual
        # obfuscation ocurrs in daemon.
        from aboutlife.launcher import launcher
        print("I: Launching daemon obfuscated")
        launcher.main()

    else:
        from aboutlife import daemon
        print("I: Launching aboutlife")
        assert args.port == 0, "Custom port disallowed when booting with default options."
        daemon.main()


if __name__ == "__main__":
    main()
