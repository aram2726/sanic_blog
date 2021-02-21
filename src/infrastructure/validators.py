import re

from abc import ABCMeta
from abc import abstractmethod
from string import punctuation
from typing import Optional

from .exceptions import InputValidationError


class AbstractBaseValidator(metaclass=ABCMeta):

    @abstractmethod
    def validate(self):
        raise NotImplementedError


class UserValidator(AbstractBaseValidator):

    MIN_PASSWORD_LENGTH = 8
    ERROR_CODE = 400
    EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    def __init__(
            self,
            username: Optional[str] = None,
            email: Optional[str] = None,
            password: Optional[str] = None):
        self.username = username
        self.email = email
        self.password = password

    def validate(self):
        self._validate_username()
        self._validate_password()
        self._validate_email()

    def _validate_username(self):
        if self.username and set(self.username) & set(punctuation):
            raise InputValidationError({
                "code": self.ERROR_CODE,
                "field": "username",
                "text": "Username should not contain punctuation."
            })

    def _validate_password(self):
        if self.password and len(self.password) < self.MIN_PASSWORD_LENGTH:
            raise InputValidationError({
                "code": self.ERROR_CODE,
                "field": "password",
                "text": f"Password should contain at last {self.MIN_PASSWORD_LENGTH} characters."
            })

    def _validate_email(self):
        if self.email and not re.search(self.EMAIL_REGEX, self.email):
            raise InputValidationError({
                "code": self.ERROR_CODE,
                "field": "email",
                "text": "Invalid email."
            })


class LoginValidator(UserValidator):

    def validate(self):
        conditions = (
            (self.username, self.password),
            (self.email, self.password),
        )
        if not any(conditions):
            raise InputValidationError(
                "Invalid data passed, waiting for either username or email and passord."
            )
        super().validate()
