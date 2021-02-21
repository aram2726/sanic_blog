from datetime import datetime
from datetime import timedelta

import jwt
from sanic.request import Request

from .exceptions import UnauthorizedError
from src.core.entities import UserEntity


class JWTManager:

    def __init__(self, request: Request, secret_key: str, token_lifetime: int):
        self._request = request
        self._secret_key = secret_key
        self._token_lifetime = token_lifetime
        self._algorithm = "HS256"

    def create(self, user: UserEntity):
        payload = {
            "user_id": user.uuid,
            "email": user.email,
            "name": user.username,
            "exp": datetime.utcnow() + timedelta(days=self._token_lifetime),
        }
        return jwt.encode(payload, self._secret_key, self._algorithm)

    def validate(self, token: str):
        try:
            token = jwt.decode(token, key=self._secret_key, algorithms=[self._algorithm])
        except jwt.exceptions.PyJWTError:
            raise UnauthorizedError("Invalid token.")
        # TODO: implement this.
