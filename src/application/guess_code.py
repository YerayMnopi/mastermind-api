from dataclasses import dataclass

from src.domain.game import Game, GameUnitOfWork, Guess


@dataclass
class GuessCodeRequest:
    identifier: str
    guess: str


class GuessCodeHandler:
    def __init__(self, games_unit_of_work: GameUnitOfWork):
        self.games_uow = games_unit_of_work

    def handle(self, request: GuessCodeRequest) -> Game:
        game = self.games_uow.games.get(request.identifier)
        black_peqs, white_peqs = game.check_guess(request.guess)
        guess = Guess(
            None,
            game_id=game.identifier,
            code=request.guess,
            black_peqs=black_peqs,
            white_peqs=white_peqs,
            date_created=None
        )

        with self.games_uow:
            self.games_uow.games.add_guess(guess)
            self.games_uow.games.update(game)
            self.games_uow.commit()
