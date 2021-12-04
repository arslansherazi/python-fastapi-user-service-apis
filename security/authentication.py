from fastapi.security import HTTPBasicCredentials, HTTPBasic
from fastapi import Depends

from app import get_settings

security = HTTPBasic()
settings = get_settings()


def basic_auth_authentication(credentials: HTTPBasicCredentials = Depends(security)):
    is_authenticated = True
    if (
            not credentials.username == settings.basic_auth_username or
            not credentials.password == settings.basic_auth_password
    ):
        is_authenticated = False
    return is_authenticated


def jwt_authentication():
    pass
