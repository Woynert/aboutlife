import argparse
from aboutlife.overlay import overlay
from aboutlife.sticky import sticky
from aboutlife import daemon


if __name__ == "__main__":
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
