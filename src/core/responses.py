from abc import ABCMeta
from abc import abstractmethod

CODE_OK = 200
CODE_DELETED = 204
CODE_CREATED = 201
CODE_BAD_REQUEST = 400
CODE_UNAUTHORIZED = 401
CODE_PERMISSION_DENIED = 403
CODE_NOT_FOUND = 404


class AbstractBaseResponse(metaclass=ABCMeta):

    @property
    def status(self):
        raise NotImplementedError

    @status.setter
    def status(self, status: str):
        raise NotImplementedError

    @property
    @abstractmethod
    def response(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def data(self):
        raise NotImplementedError

    @data.setter
    @abstractmethod
    def data(self, data):
        raise NotImplementedError

    @property
    @abstractmethod
    def headers(self):
        raise NotImplementedError
