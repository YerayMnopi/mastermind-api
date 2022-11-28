from dataclasses import dataclass

from src.domain.game import (Game, GameColor, GameUnitOfWork, Guess,
                             InvalidGuessValuesException)


@dataclass
class GuessCodeRequest:
    identifier: str
    guess: str


class GuessCodeHandler:
    def __init__(self, games_unit_of_work: GameUnitOfWork):
        self.games_uow = games_unit_of_work

    def handle(self, request: GuessCodeRequest) -> Game:
        for code_value in request.guess:
            if not code_value in [item.value for item in GameColor]:
                raise InvalidGuessValuesException()

        with self.games_uow:
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
            self.games_uow.games.add_guess(guess)
            self.games_uow.games.update(game)
            self.games_uow.commit()
            game_copy = Game(
                identifier=game.identifier,
                code=game.code,
                max_tries=game.max_tries,
            )
            game_copy.tries = game.tries
            game_copy.date_created = game.date_created
            game_copy.date_modified = game.date_modified
            game_copy.guesses = [
                Guess(
                    identifier=guess.identifier,
                    game_id=guess.game_id,
                    code=guess.code,
                    black_peqs=guess.black_peqs,
                    white_peqs=guess.white_peqs,
                    date_created=guess.date_created
                )
                for guess in game.guesses
            ]
            game_copy.guessed = game.guessed

        return game_copy
