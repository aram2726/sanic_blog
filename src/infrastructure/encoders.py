import json

from src.core.entities import BaseEntity
from src.core.entities import UserEntity


class ResponseEncoder(json.JSONEncoder):
    def default(self, instance):
        if isinstance(instance, UserEntity):
            data = instance.serialize()
            data.pop("password")
            return {**data}
        if issubclass(instance.__class__, BaseEntity):
            data = instance.serialize()
            return {**data}
        return super().default(instance)
