from abc import ABC, abstractmethod
from uuid import UUID

from .game import Game
from .guess import Guess


class GamesRepository(ABC):
    """
    All games data operations.
    """

    @abstractmethod
    def get(self, identifier: UUID) -> Game:
        raise NotImplementedError

    @abstractmethod
    def add(self, game: Game):
        raise NotImplementedError

    @abstractmethod
    def add_guess(self, guess: Guess):
        raise NotImplementedError

    @abstractmethod
    def update(self, game: Game):
        raise NotImplementedError
