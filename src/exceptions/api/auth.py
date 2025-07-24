from fastapi import status

from src.exceptions.api.base import BaseHTTPException


class IncorrectAuthCredsHTTPException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect email or password"


class InvalidAuthTokenHTTPException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid auth token"
