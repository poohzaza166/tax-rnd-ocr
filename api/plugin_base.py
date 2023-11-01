from abc import ABC, abstractmethod

class PluginBase(ABC):

    @abstractmethod
    def can_handle(self, text):
        pass

    @abstractmethod
    def handle(self, text):
        pass