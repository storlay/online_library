from src.exceptions.service.base import BaseServiceException


class UserAlreadyExistsServiceException(BaseServiceException):
    detail = "User already exists"
