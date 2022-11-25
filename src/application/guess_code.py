from dataclasses import dataclass

from src.domain.game import Game, GameUnitOfWork


@dataclass
class GuessCodeRequest:
    identifier: str
    guess: str


class GuessCodeHandler:
    def __init__(self, games_unit_of_work: GameUnitOfWork):
        self.games_uow = games_unit_of_work

    def handle(self, request: GuessCodeRequest) -> Game:
        game = self.games_uow.games.get(request.identifier)
        game.check_guess(request.guess)

        with self.games_uow:
            self.games_uow.games.update(game)
            self.games_uow.commit()
