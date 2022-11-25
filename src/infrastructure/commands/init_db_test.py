from unittest.mock import MagicMock

import psycopg2
import pytest

from src.settings import Settings

from .init_db import InitDBCommand


class TestInitDBCommand:
    settings: Settings
    db_controller: psycopg2

    @pytest.fixture
    def instance(self):
        self.settings = MagicMock(spec=Settings)
        self.settings.postgres_host = 'postgres_host'
        self.settings.postgres_username = 'postgres_username'
        self.settings.postgres_password = 'postgres_password'
        self.settings.postgres_database = 'postgres_db'
        self.db_controller = MagicMock(spec=psycopg2)

        return InitDBCommand(self.settings, self.db_controller)

    def test_create(self, instance: InitDBCommand):
        assert bool(instance) is True

    def test_should_connect_to_db(self, instance: InitDBCommand):
        instance.handle()

        self.db_controller.connect.assert_called_with(
            host=self.settings.postgres_host,
            user=self.settings.postgres_username,
            password=self.settings.postgres_password,
        )

    def test_should_execute_create_query(self, instance: InitDBCommand):
        cursor_mock = self.db_controller.connect.return_value.cursor.return_value

        instance.handle()

        cursor_mock.execute.assert_called_with(
            f"create database {self.settings.postgres_database};")

    def test_should_continue_if_db_already_exist(self, instance: InitDBCommand):
        cursor_mock = self.db_controller.connect.return_value.cursor.return_value
        cursor_mock.execute.side_effect = True

        instance.handle()

        cursor_mock.execute.assert_called()
