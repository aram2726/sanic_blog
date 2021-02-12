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

    @abstractmethod
    def select_one(self, table: str, uuid: int):
        raise NotImplementedError

    @abstractmethod
    def select_all(self, table: str, limit: Optional[int] = None, after: Optional[int] = None):
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

    def select_one(self, table: str, uuid: int):
        query = f"SELECT * FROM {table} WHERE uuid = {uuid}"

        self.cursor.execute(query)
        data = self.cursor.fetcone()
        return data

    def select_all(self, table: str, limit: Optional[int] = None, after: Optional[int] = None):
        query = f"SELECT * FROM {table}"

        if limit:
            query = f"{query} LIMIT {limit}"

        if after:
            query = f"{query} AFTER {after}"

        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

    def insert(self, table: str, data: dict):
        data_keys = list(data.keys())
        data_values = list(data.values())
        keys = " ,".join(data_keys)
        values = " ,".join(data_values)

        query = f"INSERT INTO {table} ({keys}) ({values})"
        self.cursor.execute(query)
        self.connection.commit()

    def update(self, table: str, uuid: int, data: dict):
        pass

    def delete(self, table: str, uuid: int):
        pass
