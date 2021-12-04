from fastapi.security import HTTPBasicCredentials, HTTPBasic, OAuth2PasswordBearer
from fastapi import Depends
from jose import jwt, JWTError

from app import get_settings

security = HTTPBasic()
settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def basic_auth_authentication(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Authenticates basic auth
    """
    is_authenticated = True
    if (
            not credentials.username == settings.basic_auth_username or
            not credentials.password == settings.basic_auth_password
    ):
        is_authenticated = False
    return is_authenticated


def jwt_authentication(token: str = Depends(oauth2_scheme)):
    """
    Authenticates jwt token
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload.get('__ud')
    except JWTError:
        return None
