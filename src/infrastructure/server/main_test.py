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
        game_response = response.json()
        with self.uow:
            game = self.uow.games.get(game_response['identifier'])
            self.uow.games.session.delete(game)
            self.uow.commit()
        assert response.status_code == 201

    def test_get(self):
        game = Game()
        with self.uow:
            self.uow.games.add(game)
            self.uow.commit()

            response = client.get(f"/games/{game.identifier}")
            self.uow.games.session.delete(game)
            self.uow.commit()
            assert response.status_code == 200

    def test_guess_win(self):
        game = Game()
        with self.uow:
            self.uow.games.add(game)
            self.uow.commit()
            response = client.post(
                f"/games/{game.identifier}/guess",
                json={'code': game.code}
            )
            game_response = response.json()
            self.uow.games.session.delete(game)
            self.uow.commit()
            assert response.status_code == 201
            assert game_response['guessed'] is True

    def test_max_tries_reached(self):
        game = Game(
            max_tries=1,
            code='RRRR'
        )

        with self.uow:
            self.uow.games.add(game)
            self.uow.commit()
            response_1 = client.post(
                f"/games/{game.identifier}/guess",
                json={'code': 'BBBB'}
            )

            response_2 = client.post(
                f"/games/{game.identifier}/guess",
                json={'code': 'GGGG'}
            )

            self.uow.games.session.delete(game)
            self.uow.commit()
            assert response_1.status_code == 201
            assert response_2.status_code == 400

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
            self.uow.games.session.delete(game)
            self.uow.commit()
            assert response.status_code == 400
