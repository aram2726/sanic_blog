from datetime import datetime
from datetime import timedelta
from typing import Optional

import jwt
from sanic.request import Request

from .exceptions import UnauthorizedError
from .repositories import UserRepository
from src.core.entities import UserEntity
from src.core.responses import CODE_UNAUTHORIZED


class JWTManager:

    def __init__(
            self,
            request: Request,
            secret_key: str,
            token_lifetime: int,
            users_repo: UserRepository):
        self._request = request
        self._secret_key = secret_key
        self._token_lifetime = token_lifetime
        self._algorithm = "HS256"
        self._users_repo = users_repo

    def create(self, user: UserEntity) -> str:
        payload = {
            "user_id": user.uuid,
            "email": user.email,
            "name": user.username,
            "exp": datetime.utcnow() + timedelta(days=self._token_lifetime),
        }
        return jwt.encode(payload, self._secret_key, self._algorithm)

    def validate(self, token: str):
        decoded_token = self._decode_token(token)

        exp = decoded_token["exp"]
        if exp >= datetime.now():
            raise UnauthorizedError("Token is expired.")

        uuid = decoded_token["user_id"]
        if not self._users_repo.get_one(uuid):
            raise UnauthorizedError("User does not exist.")

    async def get_user(self, token: str) -> Optional[UserEntity]:
        decoded_token = self._decode_token(token)
        return await self._users_repo.get_one(decoded_token["user_id"])

    def _decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, key=self._secret_key, algorithms=[self._algorithm])
        except jwt.exceptions.PyJWTError:
            raise UnauthorizedError({"message": "Invalid token.", "status": CODE_UNAUTHORIZED, "field": None})
