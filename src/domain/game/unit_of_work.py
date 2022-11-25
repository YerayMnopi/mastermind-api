from abc import ABC, abstractmethod

from .repository import GamesRepository


class GameUnitOfWork(ABC):
    games: GamesRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError
