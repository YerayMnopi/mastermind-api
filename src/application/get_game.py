from dataclasses import dataclass

from src.domain.game import Game, GamesRepository


@dataclass
class GetGameRequest:
    identifier: str


class GetGameHandler:
    def __init__(self, games_repository: GamesRepository):
        self.games_repository = games_repository

    def handle(self, request: GetGameRequest) -> Game:
        return self.games_repository.get(request.identifier)
