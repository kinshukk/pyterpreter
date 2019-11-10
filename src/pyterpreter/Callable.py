from abc import ABC, abstractmethod

class Callable(ABC):
    @abstractmethod
    def call(self, interpreter, arguments):
        pass

    @abstractmethod
    def arity(self):
        pass

    @abstractmethod
    def __str__(self):
        pass
