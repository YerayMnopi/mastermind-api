from unittest.mock import MagicMock

import pytest

from src.application.guess_code import GuessCodeHandler, GuessCodeRequest
from src.domain.game import Game, GamesRepository, GameUnitOfWork


class TestGuessCodeHandler:
    games_uow: GameUnitOfWork
    game: Game

    @pytest.fixture
    def instance(self):
        self.games_uow = MagicMock(
            spec=GameUnitOfWork)

        self.games_uow.games = MagicMock(
            spec=GamesRepository
        )
        self.game = MagicMock(spec=Game)
        self.game.identifier = 'game_1'
        self.game.check_guess.return_value = 4, 0
        self.games_uow.games.get.return_value = self.game

        return GuessCodeHandler(
            self.games_uow,
        )

    def test_create(self, instance: GuessCodeHandler):
        assert bool(instance) is True

    def test_should_get_game(self, instance: GuessCodeHandler):
        request = GuessCodeRequest('game_1', 'RGBB')
        instance.handle(request)

        self.games_uow.games.get.assert_called_with(request.identifier)

    def test_should_call_guess_method(self, instance: GuessCodeHandler):
        request = GuessCodeRequest('game_1', 'RGBB')
        instance.handle(request)

        self.game.check_guess.assert_called_with(request.guess)

    def test_should_update_game(self, instance: GuessCodeHandler):
        request = GuessCodeRequest('game_1', 'RGBB')
        instance.handle(request)

        self.games_uow.games.update.assert_called_with(self.game)
