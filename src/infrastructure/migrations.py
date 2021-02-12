from .databases import AbstractBaseDBClient


class Migration:

    def __init__(self, db: AbstractBaseDBClient):
        self._db = db

    BLOG_TABLE = "blog"

    @property
    def db(self):
        return self._db

    def create_table(self):
        query = f"""CREATE TABLE {self.BLOG_TABLE} (
            uuid  INTEGER PRIMARY KEY,
            title TEXT NOT NULL, 
            context TEXT NOT NULL
        );"""

        self.db.cursor.execute(query)
        self.db.connection.commit()
