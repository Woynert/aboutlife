import time
import subprocess
from aboutlife.plugin import Plugin


AUTOSHUTDOWN_HOUR = 9 +12 # PM
AUTOSHUTDOWN_MINUTE = 30
SLEEP_SECS = 60
# SLEEP_SECS = 10


class AutoShutdownPlugin(Plugin):
    def setup(self, dont_actually_shutdown: bool = False):
        if (dont_actually_shutdown):
            print("AutoShutdownPlugin: D: Will not actually shutdown.")
        else:
            print("AutoShutdownPlugin: WAR: Ready to actually shutdown for real.")

        while True:
            time.sleep(SLEEP_SECS)

            curr_time = time.localtime()
            curr_hour = curr_time.tm_hour
            curr_minute = curr_time.tm_min

            if ((curr_hour > AUTOSHUTDOWN_HOUR) or
                (curr_hour == AUTOSHUTDOWN_HOUR and curr_minute >= AUTOSHUTDOWN_MINUTE)):
                print("AutoShutdownPlugin: I: Shutting down")
                subprocess.run(["shutdown", "now"])

    def process(self):
        pass

    def cleanup(self):
        pass


def main():
    plugin = AutoShutdownPlugin()
    plugin.setup(True)
if __name__ == "__main__":
    main()
