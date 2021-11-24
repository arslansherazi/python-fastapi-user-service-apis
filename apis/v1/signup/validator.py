from typing import Optional

from pydantic.main import BaseModel
from pydantic.types import FilePath


class SignupApiValidator(BaseModel):
    username: str
    email: str
    password: str
    name: str
    profile_image: Optional[FilePath] = None
