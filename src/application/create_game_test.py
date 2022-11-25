from unittest.mock import MagicMock

import pytest

from src.application.create_game import CreateGameHandler, CreateGameRequest
from src.domain.game import GamesRepository, GameUnitOfWork


class TestCreateGameHandler:
    games_uow: GameUnitOfWork

    @pytest.fixture
    def instance(self):
        self.games_uow = MagicMock(
            spec=GameUnitOfWork)

        self.games_uow.games = MagicMock(
            spec=GamesRepository
        )

        return CreateGameHandler(
            self.games_uow,
        )

    def test_create(self, instance: CreateGameHandler):
        assert bool(instance) is True

    def test_should_call_repo(self, instance: CreateGameHandler):
        request = CreateGameRequest('game_1')
        instance.handle(request)

        self.games_uow.games.add.assert_called_once()
