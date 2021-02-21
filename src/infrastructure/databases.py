import functools
import sqlite3

from abc import ABCMeta
from abc import abstractmethod
from typing import Optional

from .exceptions import AppDBConnectionError


def lazy_connection(method):
    @functools.wraps(method)
    def wrapper(self):
        if not self._connection:
            self._connection = method(self)
        return self._connection

    return wrapper


class AbstractBaseDBClient(metaclass=ABCMeta):

    @property
    @abstractmethod
    def connection(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def cursor(self):
        raise NotImplementedError

    @abstractmethod
    def select_one(self, table: str, uuid: int):
        raise NotImplementedError

    @abstractmethod
    def select_all(self, table: str, limit: Optional[int] = None, after: Optional[int] = None):
        raise NotImplementedError

    @abstractmethod
    def filter(self, table: str, data: dict):
        raise NotImplementedError

    @abstractmethod
    def insert(self, table: str, data: dict):
        raise NotImplementedError

    @abstractmethod
    def update(self, table: str, uuid: int, data: dict):
        raise NotImplementedError

    @abstractmethod
    def delete(self, table: str, uuid: int):
        raise NotImplementedError


class SQLiteDBClient(AbstractBaseDBClient):

    def __init__(self, filename: str):
        self._filename = filename
        self._connection = None
        self._cursor = None

    @property  # type: ignore
    @lazy_connection
    def connection(self):
        try:
            connection = sqlite3.connect(self._filename)
            connection.row_factory = sqlite3.Row
            return connection
        except sqlite3.Error:
            raise AppDBConnectionError("Cant connect to db")

    @property
    def cursor(self):
        if self._cursor is None:
            self.cursor = self.connection.cursor()

        return self._cursor

    @cursor.setter
    def cursor(self, cursor):
        self._cursor = cursor

    async def select_one(self, table: str, uuid: int):
        query = f"SELECT * FROM {table} WHERE uuid = {uuid}"

        self.cursor.execute(query)
        data = self.cursor.fetcone()
        return data

    async def select_all(self, table: str, limit: Optional[int] = None, after: Optional[int] = None):
        query = f"SELECT * FROM {table}"

        if limit:
            query = f"{query} LIMIT {limit}"

        if after:
            query = f"{query} AFTER {after}"

        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

    async def filter(self, table: str, data: dict):
        keys = list(data.keys())
        where_statement = [f"{k}=:{k}" for k in keys]
        query = f"SELECT * FROM {table} WHERE {where_statement}"

        self.cursor.execute(query, data)
        data = self.cursor.fetchall()
        return data

    async def insert(self, table: str, data: dict):
        keys = list(data.keys())
        query = "INSERT INTO {table} ({keys}) VALUES ({vals})".format(
            table=table, keys=", ".join(keys), vals=", ".join([f":{k}" for k in keys])
        )
        self.cursor.execute(query, data)
        self.connection.commit()

    async def update(self, table: str, uuid: int, data: dict):
        keys = list(data.keys())
        to_update = [f"{k}=:{k}" for k in keys]
        query = "UPDATE {table} SET {to_update} WHERE uuid={uuid}".format(
            table=table, to_update=", ".join(to_update), uuid=uuid
        )
        self.cursor.execute(query, data)
        self.connection.commit()

    async def delete(self, table: str, uuid: int):
        query = "DELETE FROM {table} WHERE uuid={uuid}".format(
            table=table, uuid=uuid
        )
        print(query)
        self.cursor.execute(query)
        self.connection.commit()
