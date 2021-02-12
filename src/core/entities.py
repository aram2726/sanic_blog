from abc import ABCMeta
from datetime import datetime


class BaseEntity(metaclass=ABCMeta):

    def __init__(self, uuid: int):
        self._uuid = uuid

    @property
    def uuid(self):
        return self._uuid

    @uuid.setter
    def uuid(self, uuid: int):
        self._uuid = uuid


class BlogPostEntity(BaseEntity):

    def __init__(self, uuid: int, title: str, context: str):
        super().__init__(uuid)
        self._title = title
        self._context = context
        self._updated_at = datetime.now()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title: str):
        self._title = title

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context: str):
        self._context = context

    @property
    def updated_at(self):
        return self._updated_at
