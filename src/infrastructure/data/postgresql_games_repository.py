from uuid import UUID

from sqlalchemy.orm import Session

from src.domain.game import Game, GamesRepository


class PostgresqlGamesRepository(GamesRepository):
    def __init__(self, session: Session):
        self.session = session

    def get(self, identifier: UUID) -> Game:
        self.session.query(Game).get(identifier)

    def add(self, game: Game):
        self.session.add(game)

    def update(self, game: Game):
        self.session.merge(game)
