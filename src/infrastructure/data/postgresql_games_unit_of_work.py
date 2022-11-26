from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.domain.game import GameUnitOfWork
from src.settings import get_settings

from .postgresql_games_repository import PostgresqlGamesRepository

get_session: Session = sessionmaker(bind=create_engine(
    get_settings().get_postgres_uri()))


class PostgresGamesUnitOfWork(GameUnitOfWork):
    session: Session
    games: PostgresqlGamesRepository

    def __init__(self, session_factory=get_session):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.games = PostgresqlGamesRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
