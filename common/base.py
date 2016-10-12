from abc import abstractmethod, ABCMeta


class Base(metaclass=ABCMeta):

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def play(self):
        pass
