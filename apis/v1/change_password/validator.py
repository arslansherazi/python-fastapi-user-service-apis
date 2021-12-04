from typing import Optional

from pydantic.main import BaseModel


class ChangePasswordApiValidator(BaseModel):
    current_password: str
    new_password: str
    encryption_disable_key: Optional[str] = None
