from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from dataclasses import dataclass
from typing import Tuple

class GameColor(Enum):
    RED = 'R'
    BLUE = 'B'
    YELLOW = 'Y'
    GREEN = 'G'
    WHITE = 'W'
    ORANGE = 'O'


@dataclass
class GuessResult:
    black_peqs: int = 0
    white_peqs: int = 0

    def values(self) -> Tuple[int, int]:
        return self.black_peqs, self.white_peqs


class MaxTriesReachedException(Exception):
    """
    Raised when a game is not available anymore.
    """


class Game:
    """
    A mastermind game.
    """
    identifier: int
    code: str
    tries: int
    max_tries: int
    create_date: datetime
    modified_date: datetime

    def __init__(self,
        identifier: int,
        code: str,
        max_tries: int,
        tries: int
    ):
        self.identifier = identifier
        self.code = code
        self.max_tries = max_tries
        self.tries = tries

    def __repr__(self):
        return f'Game {self.identifier}'

    def check_guess(self, guess: str) -> GuessResult:
        if self.tries >= self.max_tries:
            raise MaxTriesReachedException()
        self.tries += 1
        result = GuessResult()
        remainings_codes = list(self.code)
        remaining_guess = []

        for guess_index, guess_value in enumerate(guess):
            code_value = self.code[guess_index]

            if code_value == guess_value:
                result.black_peqs += 1
                remainings_codes[guess_index] = None
            else:
                remaining_guess.append(guess_value)

        for guess_index, guess_value in enumerate(remaining_guess):
            if guess_value in remainings_codes:
                result.white_peqs += 1

        return result


class GamesRepository(ABC):
    """
    All games data operations.
    """

    @abstractmethod
    def get(self) -> Game:
        raise NotImplementedError()

    @abstractmethod
    def add(self, game: Game):
        raise NotImplementedError()

