from unittest.mock import MagicMock

import pytest

from src.application.get_game import GetGameHandler, GetGameRequest
from src.domain.game import GamesRepository


class TestGetGameHandler:
    games_repository: GamesRepository

    @pytest.fixture
    def instance(self):
        self.games_repository = MagicMock(
            spec=GamesRepository)

        return GetGameHandler(
            self.games_repository,
        )

    def test_create(self, instance: GetGameHandler):
        assert bool(instance) is True

    def test_should_call_repo(self, instance: GetGameHandler):
        request = GetGameRequest('game_1')
        instance.handle(request)

        self.games_repository.get.assert_called_with(request.identifier)
