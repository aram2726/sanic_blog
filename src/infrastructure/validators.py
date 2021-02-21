import re

from abc import ABCMeta
from abc import abstractmethod
from string import punctuation

from .exceptions import InputValidationError


class AbstractBaseValidator(metaclass=ABCMeta):

    @abstractmethod
    def validate(self):
        raise NotImplementedError


class UserValidator(AbstractBaseValidator):

    MIN_PASSWORD_LENGTH = 8
    ERROR_CODE = 400
    EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = password

    def validate(self):
        self._validate_username()
        self._validate_password()
        self._validate_email()

    def _validate_username(self):
        if set(self.username) & set(punctuation):
            raise InputValidationError({
                "code": self.ERROR_CODE,
                "field": "username",
                "text": "Username should not contain punctuation."
            })

    def _validate_password(self):
        if len(self.password) < self.MIN_PASSWORD_LENGTH:
            raise InputValidationError({
                "code": self.ERROR_CODE,
                "field": "password",
                "text": f"Password should contain at last {self.MIN_PASSWORD_LENGTH} characters."
            })

    def _validate_email(self):
        if not re.search(self.EMAIL_REGEX, self.email):
            raise InputValidationError({
                "code": self.ERROR_CODE,
                "field": "email",
                "text": "Invalid email."
            })
