from abc import ABC, abstractmethod
import Colors
import re


class AbstractData(ABC):
    @abstractmethod
    def PrintData(self):
        print('')

    def __init__(self):
        self.ID = -1
        self.name = "Data-Not-Found"

    @property
    def PrintName(self) -> str:
        self.name = re.sub('-', ' ', self.name)
        return self.name.title()
