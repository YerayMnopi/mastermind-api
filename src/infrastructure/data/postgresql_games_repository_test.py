from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from sqlalchemy.orm import Session

from src.domain.game import Game

from .postgresql_games_repository import PostgresqlGamesRepository


class TestPostgresqlGamesRepository:
    session: Session

    @pytest.fixture()
    def instance(self):
        self.session = MagicMock(spec=Session)

        return PostgresqlGamesRepository(self.session)

    def test_should_call_get(self, instance: PostgresqlGamesRepository):
        identifier = uuid4()
        instance.get(identifier)
        self.session.query.return_value.get.assert_called_with(identifier)

    def test_should_call_add(self, instance: PostgresqlGamesRepository):
        game = Game()
        instance.add(game)
        self.session.add.assert_called_with(game)

    def test_should_call_update(self, instance: PostgresqlGamesRepository):
        game = Game()
        instance.update(game)
        self.session.merge.assert_called_with(game)
