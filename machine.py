from abc import ABC, abstractmethod
import threading


class Machine(ABC, threading.Thread):

    def __init__(self, id):
        super().__init__()
        self.id = id

    @abstractmethod
    def run(self):
        pass