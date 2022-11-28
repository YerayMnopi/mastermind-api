import pytest
from fastapi.testclient import TestClient

from src.domain.game import Game
from src.infrastructure.data import PostgresGamesUnitOfWork

from .main import app

client = TestClient(app)


@pytest.mark.integration
class TestIntegration:
    uow = PostgresGamesUnitOfWork()

    def test_create(self):
        response = client.post("/games", json={'max_tries': 9})
        assert response.status_code == 201
        game_response = response.json()
        with self.uow:
            game = self.uow.games.get(game_response['identifier'])
            self.uow.games.session.delete(game)
            self.uow.commit()

    def test_get(self):
        game = Game()
        with self.uow:
            self.uow.games.add(game)
            self.uow.commit()

            response = client.get(f"/games/{game.identifier}")
            assert response.status_code == 200

            self.uow.games.session.delete(game)
            self.uow.commit()

    def test_guess_win(self):
        game = Game()
        with self.uow:
            self.uow.games.add(game)
            self.uow.commit()
            response = client.post(
                f"/games/{game.identifier}/guess",
                json={'code': game.code}
            )
            assert response.status_code == 201
            game_response = response.json()
            assert game_response['guessed'] is True
            self.uow.games.session.delete(game)
            self.uow.commit()

    def test_max_tries_reached(self):
        game = Game(
            max_tries=1,
            code='RRRR'
        )

        with self.uow:
            self.uow.games.add(game)
            self.uow.commit()
            response = client.post(
                f"/games/{game.identifier}/guess",
                json={'code': 'BBBB'}
            )
            assert response.status_code == 201

            response = client.post(
                f"/games/{game.identifier}/guess",
                json={'code': 'GGGG'}
            )
            assert response.status_code == 400

            self.uow.games.session.delete(game)
            self.uow.commit()

    def test_invalid_codes(self):
        game = Game(
            max_tries=1,
            code='RRRR'
        )

        with self.uow:
            self.uow.games.add(game)
            self.uow.commit()
            response = client.post(
                f"/games/{game.identifier}/guess",
                json={'code': 'JKHL'}
            )
            assert response.status_code == 400

            self.uow.games.session.delete(game)
            self.uow.commit()
