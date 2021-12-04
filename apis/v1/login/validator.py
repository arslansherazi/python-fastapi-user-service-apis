from pydantic.main import BaseModel


class LoginApiValidator(BaseModel):
    username: str
    password: str
