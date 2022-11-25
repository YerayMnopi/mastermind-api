import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from src.settings import Settings, get_settings


class InitDBCommand:

    def __init__(self,
                 settings: Settings = get_settings(),
                 db_controller=psycopg2
                 ):
        self.settings = settings
        self.db_controller = db_controller

    def handle(self):
        con = self.db_controller.connect(
            host=self.settings.postgres_host,
            user=self.settings.postgres_username,
            password=self.settings.postgres_password
        )
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = con.cursor()
        try:
            cursor.execute(
                f"create database {self.settings.postgres_database};")
        except Exception:
            pass
