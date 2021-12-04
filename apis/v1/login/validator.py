from typing import Optional

from pydantic.main import BaseModel


class LoginApiValidator(BaseModel):
    username: str
    password: str
    encryption_disable_key: Optional[str] = None
