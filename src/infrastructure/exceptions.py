from src.core.exceptions import AppException


class APIException(AppException):
    pass


class AppDBConnectionError(AppException):
    pass


class InputValidationError(APIException):
    pass


class PermissionDeniedError(APIException):
    pass


class UnauthorizedError(APIException):
    pass
