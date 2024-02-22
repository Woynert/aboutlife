from abc import ABC, abstractmethod


class Plugin(ABC):
    def setup(self):
        pass

    # runs every tick
    @abstractmethod
    def process(self):
        pass

    # info useful for restarting the plugin
    @abstractmethod
    def health_check(self) -> bool:
        pass

    # frees resources on exit
    @abstractmethod
    def cleanup():
        pass
