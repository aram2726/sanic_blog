import hashlib
from abc import ABCMeta
from abc import abstractmethod
from datetime import datetime
from typing import Optional


class BaseEntity(metaclass=ABCMeta):

    def __init__(self, uuid: Optional[int] = None):
        self._uuid = uuid

    @property
    def uuid(self):
        return self._uuid

    @uuid.setter
    def uuid(self, uuid: int):
        self._uuid = uuid

    @abstractmethod
    def serialize(self):
        raise NotImplementedError


class UserEntity(BaseEntity):

    def __init__(
            self,
            username: Optional[str] = None,
            email: Optional[str] = None,
            password: Optional[str] = None,
            updated_at: Optional[str] = None,
            is_superadmin: Optional[bool] = None,
            uuid: Optional[int] = None):
        super().__init__(uuid)
        self._username = username
        self._email = email
        self._password = password
        self._is_superadmin = is_superadmin
        self._updated_at = updated_at

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username: str):
        self._username = username

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email: str):
        self._email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password: str):
        hashed_password = hashlib.sha256(password.encode("UTF-8")).hexdigest()
        self._password = hashed_password

    @property
    def updated_at(self):
        if not self._updated_at:
            self._updated_at = datetime.now()
        return self._updated_at

    @property
    def is_superadmin(self):
        return self._is_superadmin

    @is_superadmin.setter
    def is_superadmin(self, value: bool):
        self._is_superadmin = value

    def serialize(self):
        return {
            "uuid": self.uuid,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "is_superadmin": self.is_superadmin,
            "updated_at": str(self.updated_at)
        }


class BlogPostEntity(BaseEntity):

    def __init__(
            self,
            title: str,
            context: str,
            author: UserEntity,
            updated_at: Optional[str] = None,
            uuid: Optional[int] = None):
        super().__init__(uuid)
        self._title = title
        self._context = context
        self._author = author
        self._updated_at = updated_at if updated_at else datetime.now()

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
    def author(self) -> UserEntity:
        return self._author

    @author.setter
    def author(self, author: UserEntity):
        self._author = author

    @property
    def updated_at(self):
        return self._updated_at

    def serialize(self):
        return {
            "uuid": self.uuid,
            "title": self.title,
            "context": self.context,
            "author": self.author.uuid,
            "updated_at": str(self.updated_at)
        }
