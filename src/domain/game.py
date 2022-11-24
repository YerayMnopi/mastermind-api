from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Tuple


class GameColor(Enum):
    RED = 'R'
    BLUE = 'B'
    YELLOW = 'Y'
    GREEN = 'G'
    WHITE = 'W'
    ORANGE = 'O'


class MaxTriesReachedException(Exception):
    """
    Raised when a game is not available anymore.
    """


class Game:
    """
    A mastermind game.
    """
    win_result = (4, 0)

    def __init__(self,
                 identifier: int,
                 code: str,
                 max_tries: int = 3
                 ):
        self.identifier = identifier
        self.code = code
        self.max_tries = max_tries
        self.tries = 0
        self.guessed = False

    def __repr__(self):
        return f'Game {self.identifier}'

    def check_guess(self, guess: str) -> Tuple[int, int]:
        self.__check_tries()
        black_peqs, remainings_codes, remaining_guess = self.__count_black_peqs(
            guess)

        white_peqs = self.__count_white_peqs(remaining_guess, remainings_codes)
        result = (black_peqs, white_peqs)
        self.__check_guessed(result)

        return result

    def __check_tries(self):
        if self.tries >= self.max_tries:
            raise MaxTriesReachedException()
        self.tries += 1

    def __count_black_peqs(self, guess: str) -> Tuple[int, List[str], List[str]]:
        black_peqs = 0
        remainings_codes = list(self.code)
        remaining_guess = []

        for guess_index, guess_value in enumerate(guess):
            code_value = self.code[guess_index]

            if code_value == guess_value:
                black_peqs += 1
                remainings_codes[guess_index] = None
            else:
                remaining_guess.append(guess_value)

        return black_peqs, remainings_codes, remaining_guess

    def __count_white_peqs(self, guess: List[str], code: List[str]):
        white_peqs = 0

        for guess_value in guess:
            if guess_value in code:
                white_peqs += 1

        return white_peqs

    def __check_guessed(self, result: Tuple[int, int]):
        self.guessed = result == self.win_result


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
