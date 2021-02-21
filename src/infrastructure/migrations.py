from sqlite3.dbapi2 import Error as SQLiteError

from .databases import AbstractBaseDBClient


class Migration:

    def __init__(self, db: AbstractBaseDBClient):
        self._db = db

    BLOG_TABLE = "blog"
    USERS_TABLE = "users"

    @property
    def db(self):
        return self._db

    def create_blog_table(self):
        query = f"""CREATE TABLE IF NOT EXISTS {self.BLOG_TABLE} (
            uuid  INTEGER PRIMARY KEY,
            title TEXT NOT NULL, 
            context TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );"""
        try:
            self.db.cursor.execute(query)
            self.db.connection.commit()
        except SQLiteError:
            self.db.connection.rollback()

    def create_users_table(self):
        query = f"""CREATE TABLE IF NOT EXISTS {self.USERS_TABLE} (
            uuid  INTEGER PRIMARY KEY,
            email TEXT NOT NULL, 
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            is_superadmin BOOL NOT NULL
        );"""
        try:
            self.db.cursor.execute(query)
            self.db.connection.commit()
        except SQLiteError:
            self.db.connection.rollback()
