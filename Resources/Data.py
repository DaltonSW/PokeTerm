from abc import ABC, abstractmethod

class AbstractData(ABC):
    @abstractmethod
    def PrintData(self):
        print('')