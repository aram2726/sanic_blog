from abc import ABCMeta
from abc import abstractmethod


class AbstractBaseResponse(metaclass=ABCMeta):

    @property
    @abstractmethod
    def response(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def data(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def headers(self):
        raise NotImplementedError
