from dataclasses import dataclass

from src.domain.game import Game, GameUnitOfWork


@dataclass
class CreateGameRequest:
    max_tries: int = 3


class CreateGameHandler:
    def __init__(self, games_unit_of_work: GameUnitOfWork):
        self.games_uow = games_unit_of_work

    def handle(self, request: CreateGameRequest) -> Game:
        game = Game(max_tries=request.max_tries)

        with self.games_uow:
            self.games_uow.games.add(game)
            self.games_uow.commit()
