from unittest.mock import MagicMock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.settings import get_settings

from .postgresql_games_repository import PostgresqlGamesRepository
from .postgresql_games_unit_of_work import PostgresGamesUnitOfWork

get_session: Session = sessionmaker(bind=create_engine(
    get_settings().get_postgres_uri()))


class TestPostgresGamesUnitOfWork:
    session: Session
    games: PostgresqlGamesRepository

    @pytest.fixture()
    def instance(self):
        self.session = MagicMock(spec=Session)
        self.games = MagicMock(spec=PostgresqlGamesRepository)
        return PostgresGamesUnitOfWork(self.session)

    def test_should_call_commit(self, instance: PostgresqlGamesRepository):
        with instance:
            instance.commit()
            self.session.return_value.commit.assert_called_once()

    def test_should_call_rollback(self, instance: PostgresqlGamesRepository):
        with instance:
            instance.rollback()
            self.session.return_value.rollback.assert_called_once()

    def test_should_call_rollback_on_error(self, instance: PostgresqlGamesRepository):
        try:
            with instance:
                raise ValueError()
        except ValueError:
            pass

        self.session.return_value.rollback.assert_called_once()
