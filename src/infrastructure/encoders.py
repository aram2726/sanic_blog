import json

from src.core.entities import BaseEntity


class ResponseEncoder(json.JSONEncoder):
    def default(self, instance):
        if issubclass(instance.__class__, BaseEntity):
            data = instance.serialize()
            return {**data}
        return super().default(instance)
