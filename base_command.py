from abc import ABC, abstractmethod
#Base commands
class BaseCommand(ABC):

    @abstractmethod
    def run(self):
        pass
